from typing import List

from openai import OpenAI, OpenAIError
from tenacity import (
    wait_random_exponential,
    stop_after_attempt,
    retry
)

from config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL
from loggings import logger
from .base import BaseEmbedding


class EmbeddingOpenAI(BaseEmbedding):
    """
    OpenAI LLM wrapper for the OpenAI API.
    """

    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def embed(self, text: str) -> List[float]:
        """
        Generate embeddings for the provided text using the OpenAI API.
        :param text:
        :return:
        """
        try:
            return self._client.embeddings.create(
                input=text,
                model=OPENAI_EMBEDDING_MODEL,
            ).data[0].embedding
        except OpenAIError as e:
            logger(e, level="error")
            raise e
        except Exception as e:
            logger(e, level="error")
            raise e
