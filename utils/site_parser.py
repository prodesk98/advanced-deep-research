from typing import Optional
from utils import HTTPRequest
from markdownify import markdownify as md


class SiteParser:
    def __init__(self, url: str):
        self._url = url

    def to_markdown(self) -> Optional[str]:
        """
        Convert the content of the URL to markdown format.
        :return: The content in markdown format.
        """
        response = HTTPRequest(self._url).send()
        if not response:
            return None
        if not response.status_code == 200: # Status: OK (200)
            raise RuntimeError(
                f"Failed to fetch the URL: {self._url}, "
                f"Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
        return md(response.text)
