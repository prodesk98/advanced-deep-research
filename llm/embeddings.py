from tenacity import (
    wait_random_exponential,
    stop_after_attempt,
    retry
)

from schemas import EmbeddingsRequest
from .base import BaseEmbedding
from ._locally_call_api import LocallyCallAPI
from exceptions import (
    APIRequestError,
    EmbedError,
    InvalidEmbedValue
)


class Embeddings(BaseEmbedding):
    """
    Locally embedding class.
    """
    def __init__(self):
        self._client = LocallyCallAPI()


    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts.
        :param texts:
        :return:
        """
        if len(texts) == 0 or len(texts) > 100:
            raise InvalidEmbedValue("Number of texts must be between 1 and 100.")

        try:
            response = self._client.request(
                "embeddings",
                EmbeddingsRequest(texts=texts),
            )
            result = response.embeddings
            if len(result) == 0:
                raise EmbedError("No embeddings were returned.")
            return result
        except APIRequestError as e:
            raise EmbedError(
                f"Failed to get embeddings: {e}" +
                f"Status code: {e.status_code}" if e.status_code else "",
            )
