from typing import Optional
import asyncio

from crawl4ai.browser_manager import BrowserManager

from config import PROJECT_NAME
from exceptions import CrawlerParserError
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator, CacheMode
from .base import BaseParser


class WebBrowserCrawlerParser(BaseParser):
    def __init__(self, **kwargs):
        self.run_config = CrawlerRunConfig(
            markdown_generator = DefaultMarkdownGenerator(
                options={"ignore_links": True, "escape_html": False, "body_width": 80}
            ),
            cache_mode = CacheMode.BYPASS,
            excluded_tags = [
                "script",
                "style",
                "head",
                "title",
                "meta",
                "a",
                "img",
                "link"
            ],
        )
        self.browser_config: BrowserConfig = kwargs.get('browser_config', BrowserConfig(
            browser_type = "firefox",
            headless = True,
            viewport_width = 1280,
            viewport_height = 720,
            user_agent=f"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; {PROJECT_NAME}/1.0; "
                       f"+https://github.com/prodesk98/advanced-deep-research)",
        ))
        self._crawler: Optional[AsyncWebCrawler] = None # Lazy initialization

    def _lazy_init(self):
        """
        Lazy initialization of the AsyncWebCrawler.
        """
        if self._crawler is None:
            self._crawler = AsyncWebCrawler(config=self.browser_config)

    async def _run_web_crawler(self, url: str) -> Optional[str]:
        """
        Fetch the content of the URLs using AsyncWebCrawler.
        :return: The content of the URLs.
        """
        if not url:
            raise ValueError("URL cannot be empty.")
        if not isinstance(url, str):
            raise ValueError("URL must be a string.")
        if not url.startswith("http"):
            raise ValueError("URL must start with http or https.")

        if self._crawler is None:
            self._lazy_init()

        async with self._crawler as crawler:
            try:
                result = await crawler.arun(url, config=self.run_config)
            except Exception as e:
                raise CrawlerParserError(url, str(e))

            content = result.markdown or ""
            # https://github.com/unclecode/crawl4ai/issues/842
            # Bug Fix: Close the browser instance after use
            BrowserManager._playwright_instance = None
            #
            return content

    def parse(self, url: str) -> Optional[str]:
        """
        Get the Markdown content of the URL.
        Use the synchronous method to fetch the content of the URL.
        :return: The content in Markdown format.
        """
        return asyncio.run(self._run_web_crawler(url))
