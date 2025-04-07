from typing import Optional

from firecrawl import FirecrawlApp

from config import FIRECRAWL_API_KEY
from exceptions import CrawlerParserError
from .base import BaseParser


class FirecrawlParser(BaseParser):
    BASE_URL = "https://api.firecrawl.dev"

    def __init__(self, **kwargs):
        if not FIRECRAWL_API_KEY:
            raise ValueError("FIRECRAWL_API_KEY is not set.")
        self._firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY, api_url=self.BASE_URL)
        self.params = {
            "formats": kwargs.get("formats", ['markdown']),
            "excludeTags": kwargs.get("exclude_tags", [
                "script",
                "style",
                "head",
                "title",
                "meta",
                "a",
                "img",
                "link"
            ]),
        }

    def parse(self, url: str) -> Optional[str]:
        """
        Get the Markdown content of the URL.
        :param url:
        :return:
        """
        if not url:
            raise ValueError("URL cannot be empty.")
        if not isinstance(url, str):
            raise ValueError("URL must be a string.")
        if not url.startswith("http"):
            raise ValueError("URL must start with http or https.")

        try:
            result = self._firecrawl.scrape_url(url, params=self.params)
            metadata: dict = result.get("metadata", {})
            if metadata.get("statusCode", 200) != 200:
                raise CrawlerParserError(url, f"Error fetching the URL: {result['message']}")
            content = result.get("markdown", '')
            if not content:
                raise CrawlerParserError(url, "No content found in the response.")
            return content
        except Exception as e:
            raise CrawlerParserError(
                url,
                f"Error occurred while fetching the URL. {e}",
            )
