from abc import ABC
from typing import TypeVar, Generic

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
