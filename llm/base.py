from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

_T = TypeVar("_T")

class BaseLLM(ABC):
    """
    Base class for all LLMs.
    """

    @abstractmethod
    def generate(self, prompt: str) -> Generic[_T]:
        """
        Generate text based on the provided prompt.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def flashcard(self, prompt: str) -> List[_T]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
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
