import json
from typing import Optional

from langchain_core.tools import StructuredTool

from loggings import logger
from schemas import (
    TranscriptYoutubeVideoSchema,
    ScrappingWebSiteSchema,
    ArxivPaperSearchSchema,
    SearchDocumentsSchema,
    SearchGoogleEngineSchema,
)
from utils import (
    SiteParser,
    ArxivParser,
    YoutubeParser
)
from services import SemanticSearch, GoogleSearch


class Tools:
    def __init__(self, namespace: str):
        self._namespace = namespace

    @staticmethod
    def TranscriptYoutubeVideo(video_url: str) -> Optional[str]:
        """
        Fetch the transcript of a YouTube video.
        :param video_url: Str
            YouTube Video URL to fetch the transcript from.
        :return:
        """

        try:
            youtube_parser = YoutubeParser()
            return youtube_parser.fetch(video_url)
        except Exception as e:
            logger(e, level="error")


    @staticmethod
    def ScrappingWebSite(url: str) -> Optional[str]:
        """
        Scrape a website and convert its content to markdown.
        :param url: str
            URL of the website to scrape.
        :return:
            Optional[str]: The content of the website in Markdown format.
        """
        try:
            # Parse Website Constructor
            site_parser = SiteParser(url)
            # Convert the content to markdown
            return site_parser.to_markdown()
        except Exception as e:
            logger(e, level="error")


    @staticmethod
    def ArxivPaperSearch(query: str, max_results: int = 3) -> Optional[str]:
        """
        Search for papers on arXiv based on a query.
        :param query: Str
            The search query.
        :param max_results: Int
            The maximum number of results to return.
        :return:
            Optional[str]: The titles and abstracts of the papers found.
        """

        try:
            arXiv_parser = ArxivParser()
            return arXiv_parser.search(query, max_results)
        except Exception as e:
            logger(e, level="error")


    def SearchDocuments(self, query: str, max_results: int = 10) -> Optional[str]:
        """
        Search for a query using a search documents.
        :param query: Str
            The search query.
        :param max_results: Int
            The maximum number of results to return.
        :return:
            Optional[str]: The titles and abstracts of the papers found.
        """

        try:
            # Search Engine Constructor
            semantic_search = SemanticSearch(self._namespace)
            return json.dumps(semantic_search.search(query, max_results))
        except Exception as e:
            logger(e, level="error")


    @staticmethod
    def SearchGoogleEngine(query: str, max_results: int = 10) -> Optional[str]:
        """
        Search for a query using Google search engine.
        :param query: Str
            The search query.
        :param max_results: Int
            The maximum number of results to return.
        :return:
            Optional[str]: The titles and abstracts of the papers found.
        """

        try:
            # Search Engine Constructor
            google_search = GoogleSearch()
            return json.dumps(google_search.search(query, max_results))
        except Exception as e:
            logger(e, level="error")


    def get(self) -> list[StructuredTool]:
        """
        Get the tools for the LLM.
        :return:
            list[Tool]: List of tools for the LLM.
        """
        return [
            StructuredTool.from_function(
                func=self.TranscriptYoutubeVideo,
                name="TranscriptYoutubeVideo",
                description="Fetch the transcript of a YouTube video.",
                args_schema=TranscriptYoutubeVideoSchema,
            ),
            StructuredTool.from_function(
                func=self.ScrappingWebSite,
                name="ScrappingWebSite",
                description="Scrape a website and convert its content to markdown.",
                args_schema=ScrappingWebSiteSchema,
            ),
            StructuredTool.from_function(
                func=self.ArxivPaperSearch,
                name="ArxivPaperSearch",
                description="Search for papers on arXiv based on a query.",
                args_schema=ArxivPaperSearchSchema,
            ),
            StructuredTool.from_function(
                func=self.SearchDocuments,
                name="SearchDocuments",
                description="Search for a query using a search documents.",
                args_schema=SearchDocumentsSchema,
            ),
            StructuredTool.from_function(
                func=self.SearchGoogleEngine,
                name="SearchGoogleEngine",
                description="Search for a query using Google search engine.",
                args_schema=SearchGoogleEngineSchema,
            ),
        ]
