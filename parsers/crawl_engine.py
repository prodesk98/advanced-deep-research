from config import CRAWLER_ENGINE
from exceptions import CrawlerParserError
from bases import BaseEngine
from .firecrawl_parser import FirecrawlParser
from .crawl4ai_parser import WebBrowserCrawlerParser


class CrawlEngine(BaseEngine):
    """
    CrawlEngine is a performer for web crawling tasks.
    """

    def perform(self, contents: str, **kwargs) -> str:
        """
        Perform a web crawling task using the specified crawler engine.
        :param contents:
        :return:
        """
        if CRAWLER_ENGINE == "local":
            return WebBrowserCrawlerParser().parse(contents)
        elif CRAWLER_ENGINE == "firecrawl":
            return FirecrawlParser().parse(contents)
        raise CrawlerParserError(contents, "Crawler engine not configured.")
