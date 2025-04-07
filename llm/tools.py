import json
from typing import Optional

from langchain_core.tools import StructuredTool
from streamlit.delta_generator import DeltaGenerator

from exceptions import ToolsError
from loggings import logger
from schemas import (
    TranscriptYoutubeVideoSchema,
    ScrappingWebSiteSchema,
    ArxivPaperSearchSchema,
    SearchDocumentsSchema,
    SearchGoogleEngineSchema, SearchDeepResearcherSchema,
)
from parsers import (
    WebBrowserCrawlerParser,
    YoutubeParser
)
from researchers import (
    SemanticSearch,
    SearchEngine,
    ArxivSearch,
)
from .base import BaseLLM
from deep_searcher import AgentDeepSearch


class Tools:
    def __init__(self, namespace: str, ui: Optional[DeltaGenerator] = None, llm: Optional[BaseLLM] = None):
        self._namespace = namespace
        self._ui = ui
        self._llm = llm

    def TranscriptYoutubeVideo(self, video_url: str) -> Optional[str]:
        """
        Fetch the transcript of a YouTube video.
        :param video_url: Str
            YouTube Video URL to fetch the transcript from.
        :return:
        """
        if not video_url:
            raise ValueError("Video URL cannot be empty.")
        if not isinstance(video_url, str):
            raise ValueError("Video URL must be a string.")
        if len(video_url) > 2048:
            raise ValueError("Video URL is too long. Please provide a shorter URL.")
        if not video_url.startswith("https://www.youtube.com/watch?v="):
            raise ValueError("Invalid YouTube URL. Please provide a valid YouTube video URL.")

        logger(
            f"Fetching transcript from YouTube video: {video_url}",
            level="info",
            ui=self._ui
        )

        try:
            youtube_parser = YoutubeParser()
            result = youtube_parser.fetch(video_url)
            if not result:
                raise ToolsError("No transcript found for the provided YouTube video URL.")
            logger(
                "Transcript fetched successfully.",
                level="success",
                ui=self._ui
            )
            return result
        except Exception as e:
            logger(
                f"Error fetching transcript: {e}",
                level="error",
                ui=self._ui
            )
            raise ToolsError(f"Failed to fetch transcript from YouTube: {e}")

    def ScrappingWebSite(self, url: str) -> Optional[str]:
        """
        Scrape a website and convert its content to markdown.
        :param url: str
            URL of the website to scrape.
        :return:
            Optional[str]: The content of the website in Markdown format.
        """
        if not url.startswith("http"):
            raise ValueError("Invalid URL. Please provide a valid URL starting with http or https.")
        if not isinstance(url, str):
            raise ValueError("URL must be a string.")
        if not url:
            raise ValueError("URL cannot be empty.")
        if len(url) > 2048:
            raise ValueError("URL is too long. Please provide a shorter URL.")

        logger(
            f"Fetching website content from: {url}",
            level="info",
            ui=self._ui
        )

        try:
            # Parse Website Constructor
            web_parser = WebCrawler()
            # Convert the content to markdown
            result = web_parser.get_markdown(url)
            if not result:
                raise ToolsError("No content found for the provided URL.")
            logger(
                "Website content fetched successfully.",
                level="success",
                ui=self._ui
            )
            return result
        except Exception as e:
            logger(
                f"Error fetching website content: {e}",
                level="error",
                ui=self._ui
            )
            raise ToolsError(f"Failed to fetch website: {e}")

    def ArxivPaperSearch(self, query: str, max_results: int = 3) -> Optional[str]:
        """
        Search for papers on arXiv based on a query.
        :param query: Str
            The search query.
        :param max_results: Int
            The maximum number of results to return.
        :return:
            Optional[str]: The titles and abstracts of the papers found.
        """
        if not query:
            raise ValueError("Query cannot be empty.")
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if not isinstance(max_results, int):
            raise ValueError("max_results must be an integer.")
        if max_results < 1:
            raise ValueError("max_results must be greater than 0.")
        if max_results > 100:
            raise ValueError("max_results must be less than or equal to 100.")

        logger(
            f"Searching for papers on arXiv with query: {query}",
            level="info",
            ui=self._ui
        )

        try:
            arXiv_parser = ArxivSearch()
            result = arXiv_parser.search(query, max_results)
            if not result:
                raise ToolsError("No papers found for the provided query.")
            logger(
                "Papers fetched successfully.",
                level="success",
                ui=self._ui
            )
            return result
        except Exception as e:
            raise ToolsError(f"Failed to fetch papers from ArXiv: {e}")

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
        if not query:
            raise ValueError("Query cannot be empty.")
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if not isinstance(max_results, int):
            raise ValueError("max_results must be an integer.")
        if max_results < 1:
            raise ValueError("max_results must be greater than 0.")
        if max_results > 100:
            raise ValueError("max_results must be less than or equal to 100.")

        logger(
            f"Searching for papers with query: {query}",
            level="info",
            ui=self._ui
        )

        if not query:
            raise ToolsError("Query cannot be empty.")
        if not isinstance(query, str):
            raise ToolsError("Query must be a string.")
        if not isinstance(max_results, int):
            raise ToolsError("max_results must be an integer.")
        if max_results < 1:
            raise ToolsError("max_results must be greater than 0.")
        if max_results > 100:
            raise ToolsError("max_results must be less than or equal to 100.")

        try:
            # Search Engine Constructor
            semantic_search = SemanticSearch(self._namespace)
            return json.dumps(semantic_search.search(query, max_results))
        except Exception as e:
            raise ToolsError(
                f"Failed to fetch documents from semantic search: {e}"
            )

    def SearchGoogleEngine(self, query: str, max_results: int = 10) -> Optional[str]:
        """
        Search for a query using Google search engine.
        :param query: Str
            The search query.
        :param max_results: Int
            The maximum number of results to return.
        :return:
            Optional[str]: The titles and abstracts of the papers found.
        """
        if not query:
            raise ValueError("Query cannot be empty.")
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if not isinstance(max_results, int):
            raise ValueError("max_results must be an integer.")
        if max_results < 1:
            raise ValueError("max_results must be greater than 0.")
        if max_results > 100:
            raise ValueError("max_results must be less than or equal to 100.")

        logger(
            f"Searching for papers on Google with query: {query}",
            level="info",
            ui=self._ui
        )

        try:
            # Search Engine Constructor
            search_engine = SearchEngine()
            result = json.dumps(google_search.search(query, max_results))
            if not result:
                raise ToolsError("No results found for the provided query.")
            logger(
                "Google search results fetched successfully.",
                level="success",
                ui=self._ui
            )
            return result
        except Exception as e:
            raise ToolsError(
                f"Failed to fetch documents from Google: {e}"
            )

    def DeepResearcherEngine(self, query: str) -> Optional[str]:
        """
        Perform a deep search based on the provided query.
        :param query: Str
            The search query.
        :param query:
        :return:
        """
        if not query:
            raise ValueError("Query cannot be empty.")
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if len(query) > 2048:
            raise ValueError("Query is too long. Please provide a shorter query.")

        logger(
            f"Initialized Deep Research Engine with query: {query}...",
            level="info",
            ui=self._ui
        )

        try:
            agent_deep_search = AgentDeepSearch(
                max_depth=3,
                max_tokens=4096,
                result_limit=5,
                ui=self._ui,
                llm=self._llm,
            )
            result = agent_deep_search.run(query)
            if not result:
                logger(
                    "No results found for the provided query.",
                    level="error",
                    ui=self._ui
                )
                raise ToolsError("No results found for the provided query.")
            logger(
                "Deep Research Engine results fetched successfully.",
                level="success",
                ui=self._ui
            )
            return result
        except Exception as e:
            logger(
                f"Error initializing Deep Research Engine: {e}",
                level="error",
                ui=self._ui
            )
            raise ToolsError(f"Failed to initialize Deep Research Engine: {e}")

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
                description="Fetch the transcript of a YouTube video."
                            "Use when you need to obtain the transcription of a YouTube video.",
                args_schema=TranscriptYoutubeVideoSchema,
            ),
            StructuredTool.from_function(
                func=self.ScrappingWebSite,
                name="ScrappingWebSite",
                description="Scrape a website and convert its content to markdown."
                            "Use when you need to scrape a website and convert its content to markdown.",
                args_schema=ScrappingWebSiteSchema,
            ),
            StructuredTool.from_function(
                func=self.ArxivPaperSearch,
                name="ArxivPaperSearch",
                description="Search for papers on arXiv based on a query."
                            "Use when you need to search for papers on arXiv based on a query."
                            "English Only.",
                args_schema=ArxivPaperSearchSchema,
            ),
            StructuredTool.from_function(
                func=self.SearchDocuments,
                name="SearchDocuments",
                description="Search for a query using a search documents."
                            "Use this tool to get more information about a topic.",
                args_schema=SearchDocumentsSchema,
            ),
            StructuredTool.from_function(
                func=self.SearchGoogleEngine,
                name="SearchGoogleEngine",
                description="Search for a query using Google search engine."
                            "Use this tool to get more information about a topic on the internet."
                            "English Only.",
                args_schema=SearchGoogleEngineSchema,
            ),
            StructuredTool.from_function(
                func=self.DeepResearcherEngine,
                name="DeepResearcherEngine",
                description="Perform a deep search based on the provided query."
                            "Use this tool to get more information about a topic."
                            "To use this tool the user needs to be explicit: do in-depth research on the topic: ...",
                args_schema=SearchDeepResearcherSchema,
            )
        ]
