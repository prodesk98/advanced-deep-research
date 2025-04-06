from abc import ABC, abstractmethod
from typing import TypeVar, Optional

from langchain_core.messages import BaseMessage
from streamlit.delta_generator import DeltaGenerator

from schemas import RerankResponse

T = TypeVar("T", bound=BaseMessage)


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
    def flashcard(self, prompt: str, quantities: int = 5) -> list[T]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
        :param quantities:
        :return:
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
        """
        raise NotImplementedError(
            "Subclasses must implement the 'generate_sub_queries' method to produce sub-queries based on the provided query."
        )


    @abstractmethod
    def reflection(self, query: str, sub_queries: list[str], chunks: list[str]) -> list[str]:
        """
        Generate a reflection based on the provided query, sub-queries, and chunks.
        :param query:
        :param sub_queries:
        :param chunks:
        :return:
        """
        raise NotImplementedError(
            "Subclasses must implement the 'reflection' method to produce a reflection based on the provided query, sub-queries, and chunks."
        )

    @abstractmethod
    def summarize(self, query: str, chunks: list[str]) -> str:
        """
        Generate a summary based on the provided text.
        :return:
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


class BaseSummarization(ABC):
    """
    Base class for all summarizers.
    """

    @abstractmethod
    def summarize(self, query: str, document: str) -> str:
        """
        Summarize the provided document based on the query.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'summarize' method to produce a summary based on the provided documents."
        )

