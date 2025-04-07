from typing import Optional

from config import CRAWLER_ENGINE
from exceptions import CrawlerParserError
from .firecrawl_parser import FirecrawlParser
from .crawl4ai_parser import WebBrowserCrawlerParser


class CrawlEngine:
    """
    CrawlEngine is a performer for web crawling tasks.
    """

    @staticmethod
    def perform(url: str) -> Optional[str]:
        if CRAWLER_ENGINE == "local":
            return WebBrowserCrawlerParser().parse(url)
        elif CRAWLER_ENGINE == "firecrawl":
            return FirecrawlParser().parse(url)
        raise CrawlerParserError(url, "Crawler engine not configured.")
