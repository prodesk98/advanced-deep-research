from config import CRAWLER_ENGINE
from exceptions import CrawlerParserError
from researchers.base import BasePerformer
from .firecrawl_parser import FirecrawlParser
from .crawl4ai_parser import WebBrowserCrawlerParser


class CrawlEngine(BasePerformer):
    """
    CrawlEngine is a performer for web crawling tasks.
    """

    def perform(self, contents: str) -> str:
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
