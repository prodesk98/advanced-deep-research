from typing import Optional
from utils import HTTPRequest
from markdownify import markdownify as md
from exceptions import SiteParserError


class SiteParser:
    def __init__(self, url: str):
        self._url = url

    def to_markdown(self) -> Optional[str]:
        """
        Convert the content of the URL to Markdown format.
        :return: The content in Markdown format.
        """
        try:
            response = HTTPRequest(self._url).send()
        except Exception as e:
            raise SiteParserError(
                self._url,
                None,
                str(e),
            )
        if not response:
            return None
        if not response.status_code == 200: # Status: OK (200)
            raise SiteParserError(
                self._url,
                response.status_code,
                response.text,
            )
        return md(response.text)
