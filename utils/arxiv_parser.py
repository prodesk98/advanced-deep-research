from typing import Optional
from llm import get_reranker
from exceptions import ArxivParserError

import arxiv


class ArxivParser:
    def __init__(self):
        self._client = arxiv.Client()
        self._reranker = get_reranker()

    def search(self, query: str, max_results: int = 3) -> Optional[str]:
        """
        Search for papers on arXiv based on a query.
        :param query: str
            The search query.
        :param max_results: int
            The maximum number of results to return.
        :return:
            str: The titles and summaries of the papers found.
        """
        try:
            # Search for papers
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
            )

            # Get the results
            results = self._client.results(search)
            if not results:
                return "No results found."

            reranked_results = self._reranker.rerank(
                query, [f"**{result.title}**\n---{result.summary}---\n" for result in results])

            # Format the results
            formatted_results = "\n".join(
                [
                    result.document
                    for result in reranked_results
                ]
            )
            return formatted_results
        except Exception as e:
            raise ArxivParserError(f"Failed to fetch papers from arXiv: {e}")
