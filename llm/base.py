from abc import ABC, abstractmethod
from typing import TypeVar, Optional

from langchain_core.messages import BaseMessage
from streamlit.delta_generator import DeltaGenerator

from schemas import RerankResponse, ReflectionResultSchema
from .tools import Tools

T = TypeVar("T", bound=BaseMessage)


class BaseLLM(ABC):
    """
    Base class for all LLMs.
    """
    def __init__(self, namespace: Optional[str] = None, ui: Optional[DeltaGenerator] = None):
        """
        Initialize the LLM with optional namespace and UI.
        :param namespace:
        :param ui:
        """
        self._namespace = namespace or "default"
        self._ui = ui
        self._tools = Tools(
            namespace=self._namespace,
            ui=self._ui,
            llm=self
        )


    @abstractmethod
    def generate(self, chat_history: list[BaseMessage]) -> str:
        """
        Generate text based on the provided prompt.
        :param chat_history:
        :return:
            - str: The generated text.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'generate' method to produce text based on the provided prompt."
        )


    @abstractmethod
    def flashcard(self, prompt: str, quantities: int = 5) -> list[T]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
        :param quantities:
        :return:
            - list[FlashCardSchema]: The generated flashcards.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'flashcard' method to produce flashcards based on the provided prompt."
        )


    @abstractmethod
    def generate_sub_queries(self, query: str) -> list[str]:
        """
        Generate sub-queries based on the provided query.
        :param query:
        :return:
            - list[str]: The generated sub-queries.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'generate_sub_queries' method to produce sub-queries based on the provided query."
        )


    @abstractmethod
    def reflection(self, query: str, sub_queries: list[str], chunks: list[str]) -> ReflectionResultSchema:
        """
        Generate a reflection based on the provided query, sub-queries, and chunks.
        :param query:
        :param sub_queries:
        :param chunks:
        :return:
            - ReflectionResultSchema: The generated reflection.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'reflection' method to produce a reflection based on the provided query, sub-queries, and chunks."
        )

    @abstractmethod
    def summarize(self, query: str, chunks: list[str]) -> str:
        """
        Generate a summary based on the provided text.
        :return:
            - str: The generated summary.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'summarize' method to produce a summary based on the provided text."
        )


class BaseEmbedding(ABC):
    """
    Base class for all embeddings.
    """

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings based on the provided text.
        :param texts:
        :return:
            - list[list[float]]: The generated embeddings.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'embed' method to produce embeddings based on the provided text."
        )


class BaseReranker(ABC):
    """
    Base class for all rerankers.
    """

    @abstractmethod
    def rerank(self, query: str, documents: list[str]) -> list[RerankResponse]:
        """
        Rerank the provided documents based on the query.
        :param query:
        :param documents:
        :return:
            - list[RerankResponse]: The reranked documents.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'rerank' method to reorder documents based on the provided query."
        )


class BaseSummarization(ABC):
    """
    Base class for all summarizers.
    """

    @abstractmethod
    def summarize(self, query: str, document: str) -> str:
        """
        Summarize the provided document based on the query.
        :param query:
        :param document:
        :return:
            - str: The generated summary.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'summarize' method to produce a summary based on the provided documents."
        )

