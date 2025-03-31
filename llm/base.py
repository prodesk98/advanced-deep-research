from abc import ABC
from typing import TypeVar, Generic, List

from schemas import FlashCardSchema

_T = TypeVar("_T")

class BaseLLM(ABC):
    """
    Base class for all LLMs.
    """

    def generate(self, prompt: str) -> Generic[_T]:
        """
        Generate text based on the provided prompt.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def flashcard(self, prompt: str) -> List[FlashCardSchema]:
        """
        Generate flashcards based on the provided prompt.
        :param prompt:
        :return:
        """
        raise NotImplementedError("Subclasses must implement this method.")
