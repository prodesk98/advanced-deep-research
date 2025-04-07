import tiktoken
from langchain_text_splitters import CharacterTextSplitter

from exceptions import SummarizationError, APIRequestError
from loggings import logger
from schemas import SummarizeRequest
from .base import BaseSummarization
from ._locally_call_api import LocallyCallAPI


class Summarization(BaseSummarization):
    def __init__(self):
        self._client = LocallyCallAPI()
        self._tokenizer = tiktoken.get_encoding("cl100k_base")
        self._splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=1024,
            chunk_overlap=0,
        )

    def _split_text(self, document: str) -> list[str]:
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
        chunks: list[str] = []

        for doc in documents:
            try:
                chunks.append(self._perform(query, doc))
            except SummarizationError as e:
                logger(e)
            except APIRequestError as e:
                logger(e)
            except Exception as e:
                raise SummarizationError(
                    f"An error occurred during summarization: {str(e)}"
                )

        return "\n".join(chunks)
