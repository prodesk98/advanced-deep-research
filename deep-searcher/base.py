from abc import ABC, abstractmethod

import tiktoken


class DeepSearch(ABC):
    """
    Base class for deep search algorithms.
    """

    def __init__(self, max_depth: int = 10, max_tokens: int = 4096):
        """
        Initialize the deep search algorithm.

        :param max_depth: The maximum depth to search.
        :param max_tokens: The maximum number of tokens to process.
        """
        if max_depth <= 0:
            raise ValueError("max_depth must be greater than 0.")
        if max_tokens <= 0:
            raise ValueError("max_tokens must be greater than 0.")
        self._max_depth = max_depth
        self._max_tokens = max_tokens
        self._tokenizer = tiktoken.get_encoding("cl100k_base")
        self._chunks: list[str] = []

    @abstractmethod
    def run(self) -> str:
        raise NotImplementedError(
            "The run method must be implemented in subclasses."
        )

    def calc_tokens(self) -> int:
        """
        Calculate the number of tokens in the text chunks.
        :return: The number of tokens in the text chunks.
        """
        return sum(len(self._tokenizer.encode(chunk)) for chunk in self._chunks)

    @property
    def chunks(self) -> list[str]:
        """
        Get the chunks of text.
        :return: The chunks of text.
        """
        return self._chunks

    @property
    def max_depth(self) -> int:
        """
        Get the maximum depth.
        :return: The maximum depth.
        """
        return self._max_depth

    @property
    def max_tokens(self) -> int:
        """
        Get the maximum number of tokens.
        :return: The maximum number of tokens.
        """
        return self._max_tokens