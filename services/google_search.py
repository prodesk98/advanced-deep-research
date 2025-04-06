from typing import Optional

import googlesearch
from pydantic import BaseModel

from config import LANGUAGE
from exceptions import GoogleSearchError, WebParserParserError
from llm import get_reranker, get_summarization
from llm.reranker import Reranker
from llm.summarization import Summarization
from utils import WebParser
from .base import BaseSearchService


class SearchResult(BaseModel):
    title: str
    description: str
    content: Optional[str] = ""
    url: str


class GoogleSearch(BaseSearchService):
    def __init__(self, reranker: Optional[Reranker] = None, summarization: Optional[Summarization] = None) -> None:
        self._reranker = reranker or get_reranker()
        self._summarization = summarization or get_summarization()

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
            # Generate the advanced search query
            advanced_search = " ".join(
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
            #
            results = googlesearch.search(advanced_search, num_results=limit, lang=LANGUAGE, advanced=True)
            chunks: list[str] = []

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
                        contents = WebParser().get_markdown(result.url)
                        summarized = self._summarization.summarize(
                            query,
                            contents
                        )
                        chunks.append(summarized)
                    except WebParserParserError:
                        pass

            reranked_results = self._reranker.rerank(query, chunks)

            formatted_results = "\n".join(
                [
                    result.document
                    for result in reranked_results
                ]
            )
            return self._summarization.summarize(query, formatted_results)
        except GoogleSearchError as e:
            raise GoogleSearchError(f"Failed to fetch documents from Google: {e.message}")
        except Exception as e:
            raise GoogleSearchError(f"An unexpected error occurred: {str(e)}")
