from typing import Optional
from llm import get_reranker, get_summarization
from exceptions import ArxivSearchError
from llm.reranker import Reranker
from llm.summarization import Summarization
from .base import BaseSearchService

import arxiv


class ArxivSearch(BaseSearchService):
    def __init__(self, reranker: Optional[Reranker] = None, summarization: Optional[Summarization] = None) -> None:
        self._client = arxiv.Client()
        self._reranker = reranker or get_reranker()
        self._summarization = summarization or get_summarization()

    def search(self, query: str, limit: int = 3, parser: bool = False) -> str:
        """
        Search for papers on arXiv based on a query.
        :param query: str
            The search query.
        :param limit: int
            The maximum number of results to return.
        :param parser: bool
            Whether to parse the results or not.
        :return:
            str: The titles and summaries of the papers found.
        """
        try:
            # Search for papers
            search = arxiv.Search(
                query=query,
                max_results=limit,
                sort_by=arxiv.SortCriterion.Relevance,
            )

            # Get the results
            results = self._client.results(search)
            if not results:
                return "No results found."

            reranked_results = self._reranker.rerank(
                query, [
                    f"**{result.title}**\n---\n{result.summary}\n---\n"
                    for result in results
                ]
            )

            formatted_results = "\n".join(
                [
                    result.document
                    for result in reranked_results
                ]
            )
            return self._summarization.summarize(query, formatted_results)
        except Exception as e:
            raise ArxivSearchError(f"Failed to fetch papers from arXiv: {e}")
