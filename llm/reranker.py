from tenacity import retry, wait_random_exponential, stop_after_attempt

from schemas import RerankRequest, RerankedDocument
from exceptions import (
    APIRequestError,
    RerankError,
    InvalidRerankValue
)
from ._locally_call_api import LocallyCallAPI
from .base import BaseReranker


class Reranker(BaseReranker):
    """
    Locally reranker class.
    """
    THRESHOLD = 0.1

    def __init__(self):
        self._client = LocallyCallAPI()


    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def rerank(self, query: str, documents: list[str]) -> list[RerankedDocument]:
        """
        Rerank the provided documents based on the query.
        :param query:
        :param documents:
        :return:
        """
        if len(documents) == 0 or len(documents) > 100:
            raise InvalidRerankValue("Number of documents must be between 1 and 100.")
        if not isinstance(query, str):
            raise InvalidRerankValue("Query must be a string.")

        try:
            response = self._client.request(
                "rerank",
                RerankRequest(query=query, documents=documents),
            )
            result = response.reranked
            if len(result) == 0:
                return []
            # Filter out documents with score less than the threshold
            # 0.1 is parcial
            # 0.7 is relevant
            return [
                RerankedDocument(
                    document=document.document,
                    score=document.score,
                )
                for document in result
                if document.score >= self.THRESHOLD
            ]
            #
        except APIRequestError as e:
            raise RerankError(
                f"Failed to get reranked documents: {e}" +
                f"Status code: {e.status_code}" if e.status_code else "",
            )
