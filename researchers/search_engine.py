from typing import Optional

import googlesearch
from serpapi import GoogleSearch as SerpapiGoogleSearch

from parsers import CrawlEngine
from .brave_search import BraveSearch

from config import (
    LANGUAGE,
    SEARCH_ENGINE,
    SERPAPI_API_KEY
)
from exceptions import (
    SearchEngineError,
    CrawlerParserError,
    SummarizationError, BraveSearchError
)
from llm import get_reranker, get_summarization
from llm.reranker import Reranker
from llm.summarization import Summarization
from loggings import logger
from schemas import SearchResult
from .base import BaseSearchService


class SearchEngine(BaseSearchService):
    def __init__(self, reranker: Optional[Reranker] = None, summarization: Optional[Summarization] = None) -> None:
        self._reranker = reranker or get_reranker()
        self._summarization = summarization or get_summarization()

    @staticmethod
    def _perform(query: str, limit: int = 10) -> Optional[list[SearchResult]]:
        if SEARCH_ENGINE == "local":
            advanced_query = " ".join(
                [
                    query,
                    "-site:google.com",
                    "-ads",
                    "-youtube",
                    "-news",
                    "-shopping",
                    "-maps",
                    "-images",
                    "-filetype:pdf",
                    "lang:en",
                ]
            )
            results = googlesearch.search(advanced_query, num_results=limit, lang=LANGUAGE, advanced=True)
            return [
                SearchResult(
                    title=result.title,
                    description=result.description,
                    link=result.url,
                )
                for result in results
            ]
        elif SEARCH_ENGINE == "serpapi":
            params = {
                "q": query,
                "hl": "en",
                "gl": "us",
                "google_domain": "google.com",
                "api_key": SERPAPI_API_KEY
            }
            searcher = SerpapiGoogleSearch(params)
            data = searcher.get_dict()
            results = data.get("organic_results", [])
            return [
                SearchResult(
                    title=result.get("title"),
                    description=result.get("snippet"),
                    link=result.get("link"),
                )
                for result in results
            ]
        elif SEARCH_ENGINE == "brave":
            params = {
                "country": "US",
                "search_lang": "en",
                "ui_lang": "en-US",
            }
            searcher = BraveSearch(**params)
            results = searcher.search(query, limit)
            return [
                SearchResult(
                    title=result.title,
                    description=result.snippet,
                    link=result.link,
                )
                for result in results
            ]
        else:
            raise SearchEngineError("Google Search Engine not configured.")

    def search(self, query: str, limit: int = 10, parser: bool = True) -> str:
        """
        Search for the most relevant documents based on the query using researchers.
        :param parser: Whether to parse the results or not. Get Content from the URL return markdown.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :return:
            str: The titles and snippets of the documents found.
        """
        try:
            results = self._perform(query, limit)

            if not results:
                raise SearchEngineError("Google Search Engine returned no results.")

            chunks: list[str] = []

            if not isinstance(results, list):
                results = [
                    SearchResult(
                        title=result.title,
                        description=result.description,
                        link=result.link,
                    )
                    for result in results
                ]

            if parser:
                for result in results:
                    try:
                        contents = CrawlEngine.perform(result.link)
                        summarized = self._summarization.summarize(
                            query,
                            contents
                        )
                        chunks.append(summarized)
                    except CrawlerParserError as e:
                        logger(
                            f"Failed to parse the content from {e.url}"
                        )
                    except SummarizationError as e:
                        logger(
                            f"Failed to summarize the content from {e.message}"
                        )

            reranked_results = self._reranker.rerank(query, chunks)

            formatted_results = "\n".join(
                [
                    result.document
                    for result in reranked_results
                ]
            )
            return self._summarization.summarize(query, formatted_results)
        except SearchEngineError as e:
            raise SearchEngineError(f"Failed to fetch documents from Google: {e.message}")
        except BraveSearchError as e:
            raise SearchEngineError(f"Failed to fetch documents from Brave: {e.message}")
        except Exception as e:
            raise SearchEngineError(f"An unexpected error occurred: {str(e)}")
