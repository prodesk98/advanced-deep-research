from typing import Optional, Literal

import requests
from requests.exceptions import RequestException, JSONDecodeError, Timeout

from config import LOCALLY_API_BASE, LOCALLY_API_KEY
from schemas import (
    RerankResponse,
    EmbeddingsResponse,
    EmbeddingsRequest,
    RerankRequest
)
from exceptions import APIRequestError
from loggings import logger


class LocallyCallAPI:
    def __init__(self, api_key: str = LOCALLY_API_KEY, api_base: str = LOCALLY_API_BASE):
        self._api_key = api_key
        self._api_base = api_base
        self._session = requests.Session()

    def request(
        self,
        uri: Literal["embeddings", "rerank"],
        payload: EmbeddingsRequest | RerankRequest,
    ) -> Optional[RerankResponse | EmbeddingsResponse]:
        """
        Make a request to the local API.
        :param uri: The endpoint to call (embeddings or rerank).
        :param payload: The payload to send in the request.
        :return: The response from the API as a dictionary.
        """
        if uri == "embeddings" and not isinstance(payload, EmbeddingsRequest):
            raise ValueError("Payload must be an instance of EmbeddingsRequest.")
        if uri == "rerank" and not isinstance(payload, RerankRequest):
            raise ValueError("Payload must be an instance of RerankRequest.")

        try:
            response = self._session.post(
                "/".join([self._api_base, uri]),
                timeout=60,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=payload.model_dump(),
            )
            if not response.ok:
                raise APIRequestError(
                    f"API request failed with status code {response.status_code}",
                    status_code=response.status_code,
                )
            data = response.json()
            return EmbeddingsResponse(**data) if uri == "embeddings" else RerankResponse(**data)
        except Timeout:
            logger(
                "Request timed out. Please check your connection and try again.",
                "error"
            )
            raise APIRequestError("Request timed out")
        except JSONDecodeError:
            logger(
                "Failed to decode JSON response from the API.",
                "error"
            )
            raise APIRequestError("Failed to decode JSON response")
        except RequestException as e:
            logger(
                f"An error occurred while making the request: {e}",
                "error"

            )
            raise APIRequestError(
                f"An error occurred while making the request: {e}",
                status_code=e.response.status_code if e.response else None,
            )
        except Exception as e:
            logger(
                f"An error occurred while making the request: {e}",
                "error"

            )
            raise APIRequestError(
                f"An error occurred while making the request: {e}"
            )
