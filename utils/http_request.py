from typing import Literal, Optional
import requests

from config import PROJECT_NAME
from loggings import logger


class HTTPRequest:
    def __init__(
        self,
        url: str,
        method: Literal["GET", "POST"] = "GET",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: Optional[dict] = None
    ):
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or {}

    def _build_request(self) -> requests.Request:
        self.headers.setdefault("Accept", "application/json, text/plain, text/html")
        self.headers.setdefault("User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 "
            f"[({PROJECT_NAME}) MySemanticTool/1.0]"
        )

        return requests.Request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            json=self.data
        )

    def send(self) -> Optional[requests.Response]:
        """
        Send the request and return the response.
        """
        try:
            session = requests.Session()
            prepared_request = self._build_request().prepare()
            response = session.send(prepared_request)
            return response
        except Exception as e:
            logger(f"Failed to send request: {e}", level="error")
