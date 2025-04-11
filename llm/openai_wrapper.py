from datetime import datetime
from typing import Optional, TypeVar

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
)
from pydantic import BaseModel
from streamlit.delta_generator import DeltaGenerator

from config import NATURAL_LANGUAGE
from loggings import logger
from prompt_engineering import (
    AGENT_PROMPT,
    FLASHCARD_PROMPT,
    SUB_QUERY_PROMPT,
    REFLECT_PROMPT,
    SUMMARIZER_PROMPT
)
from schemas import (
    FlashCardSchema,
    FlashCardSchemaRequest,
    SubQueriesResultSchema,
    ReflectionResultSchema
)
from exceptions import (
    SearchEngineError, SemanticSearchError,
    ArxivSearchError, CrawlerParserError,
    YoutubeParserError, GenerativeError
)
from .base import BaseLLM
from .callbacks import AgentCallbackHandler
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from langchain_openai import ChatOpenAI
from config import (
    OPENAI_API_BASE,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_MAX_TOKENS,
)


T = TypeVar("T", bound=BaseModel)


class OpenAILLM(BaseLLM):
    """
    OpenAI wrapper for the OpenAI API.
    """
    def __init__(self, namespace: Optional[str] = None, ui: Optional[DeltaGenerator] = None):
        super().__init__(namespace, ui)
        self._chat_llm = ChatOpenAI(
            base_url=OPENAI_API_BASE,
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        )

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate(self, chat_history: list[BaseMessage]) -> str:
        """
        Generate a response based on the provided chat history.
        :param chat_history:
        :return:
        """
        logger(
            f"[{self._namespace}] Starting agent generation...",
            level="info",
            ui=self._ui,
        )
        # System template
        template = (
            AGENT_PROMPT
            .replace("{{current_time}}", datetime.now().strftime("%m-%d-%Y %H:%M:%S")) # Replace current time if have it.
            .replace("{{natural_language}}", NATURAL_LANGUAGE) # Replace natural language if have it.
        )
        # Generate messages structure
        messages = [
            SystemMessage(template),
            MessagesPlaceholder(variable_name="chat_history"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
        #
        # Construct the prompt for the agent
        prompt = ChatPromptTemplate.from_messages(messages=messages)
        #

        # Create Agent Executor
        agent = create_tool_calling_agent(self._chat_llm, self._tools.get(), prompt)
        #

        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self._tools.get(),
            verbose=True,
            max_iterations=15,
            early_stopping_method="force",
            handle_parsing_errors=True,
            return_intermediate_steps=True,
            callbacks=[AgentCallbackHandler(self._ui)],
        )
        #

        try:
            result: dict = agent_executor.invoke(
                {
                    "chat_history": chat_history,
                    "agent_scratchpad": [],
                }
            )
            return result.get("output", "")
        except SearchEngineError as e:
            return e.message
        except SemanticSearchError as e:
            return e.message
        except ArxivSearchError as e:
            return e.message
        except CrawlerParserError as e:
            return e.message
        except YoutubeParserError as e:
            return e.message
        except Exception as e:
            return f"An error occurred: {e}"

    def _generate_structured_output(self, template: str, prompt: str, schema: type[T], inputs: dict) -> T:
        system_prompt = ChatPromptTemplate.from_messages(
            messages=[
                SystemMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template=template,
                        input_variables=[k for k in inputs.keys()],
                    )
                ),
                HumanMessage(
                    content=prompt,
                ),
            ]
        )

        structured_schema = self._chat_llm.with_structured_output(schema, method="json_schema")

        chain = (
            system_prompt |
            structured_schema
        )

        try:
            output: schema = chain.invoke(inputs)
            return output
        except Exception as e:
            raise GenerativeError(
                f"Failed to generate structured output: {e}"
            ) from e

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def flashcard(self, prompt: str, quantities: int = 5) -> list[FlashCardSchema]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
        :param quantities:
        :return:
            list[FlashCardSchema]: List of generated flashcards.
        """
        logger(
            f"Generating {quantities} flashcards for prompt: {prompt}",
            level="info",
            ui=self._ui,
        )

        template = (
            FLASHCARD_PROMPT.replace("{{natural_language}}", NATURAL_LANGUAGE)  # Replace natural language if have it.
        )

        output = self._generate_structured_output(
            template=template,
            prompt=prompt,
            schema=FlashCardSchemaRequest,
            inputs={
                "quantities": quantities,
            },
        )

        if not output.flashcards:
            logger(
                f"No flashcards generated for prompt: {prompt}",
                level="error",
                ui=self._ui,
            )
            raise GenerativeError("No flashcards generated.")

        return output.flashcards

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate_sub_queries(self, query: str) -> list[str]:
        """
        Generate sub-queries based on the provided query.
        :param query:
        :return:
        """
        logger(
            f"Generating sub-queries for query: {query}",
            level="info",
            ui=self._ui,
        )

        template = SUB_QUERY_PROMPT

        output = self._generate_structured_output(
            template=template,
            prompt=query,
            schema=SubQueriesResultSchema,
            inputs={
                "current_date": datetime.now().strftime("%Y"),
                "original_query": query,
            },
        )

        if not output.queries:
            logger(
                f"No sub-queries generated for query: {query}",
                level="error",
                ui=self._ui,
            )
            raise GenerativeError("No sub-queries generated.")

        return output.queries

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def reflection(self, query: str, sub_queries: list[str], chunks: list[str]) -> ReflectionResultSchema:
        """
        Generate a reflection based on the provided query, sub-queries, and chunks.
        :param query:
        :param sub_queries:
        :param chunks:
        :return:
        """
        template = REFLECT_PROMPT

        output = self._generate_structured_output(
            template=template,
            prompt=query,
            schema=ReflectionResultSchema,
            inputs={
                "original_query": query,
                "previous_queries": sub_queries,
                "previous_documents": "\n".join(chunks),
            },
        )

        if not output.sub_queries:
            logger(
                f"No reflection generated for query: {query}",
                level="error",
                ui=self._ui,
            )
            raise GenerativeError("No reflection generated.")

        return output

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def summarize(self, query: str, chunks: list[str]) -> str:
        template = SUMMARIZER_PROMPT

        prompt_system = ChatPromptTemplate.from_messages(
            messages=[
                SystemMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template=template,
                        input_variables=[
                            "query",
                            "chunks"
                        ],
                    )
                ),
            ]
        )

        chain = (
            prompt_system |
            self._chat_llm
        )

        try:
            result = chain.invoke(
                {
                    "original_query": query,
                    "chunks": "\n\n".join(chunks),
                }
            )

            if not result:
                logger(
                    f"No summary generated for query: {query}",
                    level="error",
                    ui=self._ui,
                )
                raise GenerativeError("No summary generated.")

            return result.content
        except Exception as e:
            raise GenerativeError(
                f"Failed to generate summary: {e}"
            ) from e
