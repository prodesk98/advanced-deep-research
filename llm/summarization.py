from typing import Optional

import tiktoken
from langchain_text_splitters import CharacterTextSplitter

from exceptions import SummarizationError, APIRequestError
from schemas import SummarizeRequest
from .base import BaseSummarization
from ._locally_call_api import LocallyCallAPI


class Summarization(BaseSummarization):
    def __init__(self):
        self._client = LocallyCallAPI()
        self._chunks: list[str] = []
        self._tokenizer = tiktoken.get_encoding("cl100k_base")
        self._splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base", chunk_size=1000, chunk_overlap=100
        )

    def _split_text(self, document: str) -> list[str]:
        if self._calc_tokens(document) < 1000:
            # If the document is less than 1000 tokens, return it as is
            return [document]
        return self._splitter.split_text(document)

    def _calc_tokens(self, document: str) -> int:
        """
        Calculate the number of tokens in the provided text.
        :param document:
        :return:
        """
        return len(self._tokenizer.encode(document))

    def _perform(self, query: str, doc: str) -> str:
        """
        Perform the summarization on the provided text.
        :param query:
        :param doc:
        :return:
        """
        return self._client.request(
            "summarize",
            SummarizeRequest(
                query=query,
                document=doc,
            ),
        ).summary

    def summarize(self, query: str, document: str) -> str:
        """
        Generate a summary based on the provided text.
        :param query:
        :param document:
        :return:
        """
        if not isinstance(query, str):
            raise SummarizationError("Query must be a string.")
        if not isinstance(document, str):
            raise SummarizationError("Document must be a string.")

        documents = self._split_text(document)

        if len(documents) == 0:
            raise SummarizationError("No documents provided for summarization.")

        for doc in documents:
            try:
                self._chunks.append(self._perform(query, doc))
            except APIRequestError as e:
                raise SummarizationError(
                    f"Failed to get summary: {e}" +
                    f"Status code: {e.status_code}" if e.status_code else "",
                ) from e

        return "\n".join(self._chunks)
