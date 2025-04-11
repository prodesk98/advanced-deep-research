from abc import abstractmethod, ABC

from typing_extensions import TypeVar
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseEngine(ABC):
    @abstractmethod
    def perform(self, contents: str, **kwargs) -> str | list[T] | T:
        """
        Perform a search using the search engine.
        :param contents:
        :return:
            - str: The content of the document.
            - list[T]: The list of documents.
            - T: Class Object.
        """
        raise NotImplementedError("Subclasses should implement this method.")
