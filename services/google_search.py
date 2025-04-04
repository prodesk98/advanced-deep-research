from typing import Optional

import googlesearch
from pydantic import BaseModel

from llm import get_reranker
from config import LANGUAGE
from exceptions import GoogleSearchError, SiteParserError
from llm.reranker import Reranker
from utils import SiteParser
from .base import BaseSearchService


class SearchResult(BaseModel):
    title: str
    description: str
    content: Optional[str] = ""
    url: str


class GoogleSearch(BaseSearchService):
    def __init__(self, reranker: Optional[Reranker] = None):
        self._reranker = reranker or get_reranker()

    def search(self, query: str, limit: int = 10, parser: bool = True) -> str:
        """
        Search for the most relevant documents based on the query.
        :param parser: Whether to parse the results or not.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :return:
            str: The titles and snippets of the documents found.
        """
        try:
            results = googlesearch.search(query, num_results=limit, lang=LANGUAGE, advanced=True)

            if not isinstance(results, list):
                results = [
                    SearchResult(
                        title=result.title,
                        description=result.description,
                        url=result.url,
                    )
                    for result in results
                ]

            if len(results) == 0:
                raise GoogleSearchError(
                    f"No results found for query: {query}"
                )

            if parser:
                for result in results:
                    try:
                        result.content = SiteParser(result.url).to_markdown()
                    except SiteParserError:
                        pass

            reranked_results = self._reranker.rerank(
                query, [
                    f"**{result.title}**\n---\n{result.description} {result.content}\n---\nsource: {result.url}\n"
                    for result in results
                ]
            )

            formatted_results = "\n".join(
                [
                    result.document
                    for result in reranked_results
                ]
            )
            return formatted_results
        except GoogleSearchError as e:
            raise GoogleSearchError(f"Failed to fetch documents from Google: {e.message}")
        except Exception as e:
            raise GoogleSearchError(f"An unexpected error occurred: {str(e)}")
