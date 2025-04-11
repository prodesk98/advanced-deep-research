from typing import Literal

from bases import BaseEngine
from config import LLM_ENGINE
from schemas import FlashCardSchema, ReflectionResultSchema
from .ollama_wrapper import OllamaLLM
from .openai_wrapper import OpenAILLM

CommandType = Literal[
    "generate",
    "flashcard",
    "generate_sub_queries",
    "reflection",
    "summarize",
]

class LLMEngine(BaseEngine):
    """
    A class that represents a large language model (LLM) performer.
    """
    def perform(
        self,
        contents: str,
        **kwargs
    ) -> str | list[FlashCardSchema] | ReflectionResultSchema | list[str]:

        command: str = kwargs.get("command")
        if LLM_ENGINE == "openai":
           engine = OpenAILLM()
        elif LLM_ENGINE == "ollama":
           engine = OllamaLLM()
        else:
            raise Exception("Unknown LLM engine.")

        if command == "generate":
            return engine.generate(
                kwargs.get("chat_history", []),
            )
        elif command == "flashcard":
            return engine.flashcard(
                kwargs.get("prompt"),
                kwargs.get("quantities", 5),
            )
        elif command == "generate_sub_queries":
            return engine.generate_sub_queries(contents)
        elif command == "reflection":
            return engine.reflection(contents)
        elif command == "summarize":
            return engine.summarize(contents)
        else:
            raise Exception("Unknown command.")
