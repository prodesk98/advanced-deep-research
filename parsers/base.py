from abc import ABC, abstractmethod
from typing import Optional


class BaseParser(ABC):
    """
    Base class for parsers.
    """

    @abstractmethod
    def parse(self, contents: str | bytes | dict) -> Optional[str | bytes | dict]:
        """
        Parse the content and return the parsed data.
        :param contents:
        :return:
        """
        raise NotImplementedError(
            "The parse method must be implemented in subclasses."
        )
