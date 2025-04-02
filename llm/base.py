from abc import ABC, abstractmethod
from typing import TypeVar, List, Optional

from langchain_core.messages import BaseMessage
from streamlit.delta_generator import DeltaGenerator

_T = TypeVar("_T")


class BaseLLM(ABC):
    """
    Base class for all LLMs.
    """

    @abstractmethod
    def generate(self, chat_history: list[BaseMessage], placeholder: Optional[DeltaGenerator]) -> str:
        """
        Generate text based on the provided prompt.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def flashcard(self, prompt: str, quantities: int = 5) -> List[_T]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
        :param quantities:
        :return:
        """
        raise NotImplementedError("Subclasses must implement this method.")


class BaseEmbedding(ABC):
    """
    Base class for all embeddings.
    """

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """
        Generate embeddings based on the provided text.
        """
        raise NotImplementedError("Subclasses must implement this method.")
