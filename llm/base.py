from abc import ABC, abstractmethod
from typing import TypeVar, Optional

from langchain_core.messages import BaseMessage
from streamlit.delta_generator import DeltaGenerator

from schemas import RerankResponse

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
        raise NotImplementedError(
            "Subclasses must implement the 'generate' method to produce text based on the provided prompt."
        )

    @abstractmethod
    def flashcard(self, prompt: str, quantities: int = 5) -> list[_T]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
        :param quantities:
        :return:
        """
        raise NotImplementedError(
            "Subclasses must implement the 'flashcard' method to produce flashcards based on the provided prompt."
        )


class BaseEmbedding(ABC):
    """
    Base class for all embeddings.
    """

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings based on the provided text.
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
        """
        raise NotImplementedError(
            "Subclasses must implement the 'rerank' method to reorder documents based on the provided query."
        )
