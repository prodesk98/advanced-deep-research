from typing import Optional
import asyncio

from crawl4ai.browser_manager import BrowserManager

from exceptions import WebParserParserError
from crawl4ai import AsyncWebCrawler, BrowserConfig


class WebParser:
    def __init__(self, **kwargs):
        self.browser_config: BrowserConfig = kwargs.get('browser_config', BrowserConfig(
            browser_type="firefox",
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
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
        if self._crawler is None:
            self._lazy_init()

        async with self._crawler as crawler:
            try:
                result = await crawler.arun(url)
            except Exception as e:
                raise WebParserParserError(url, str(e))

            content = result.markdown or ""
            # https://github.com/unclecode/crawl4ai/issues/842
            # Bug Fix: Close the browser instance after use
            BrowserManager._playwright_instance = None
            #
            return content

    async def aget_markdown(self, url: str) -> Optional[str]:
        """
        Get the Markdown content of the URL.
        :return: The content in Markdown format.
        """
        return await self._run_web_crawler(url)

    def get_markdown(self, url: str) -> Optional[str]:
        """
        Get the Markdown content of the URL.
        :return: The content in Markdown format.
        """
        return asyncio.run(self._run_web_crawler(url))
