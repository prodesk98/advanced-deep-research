import googlesearch

from llm import get_reranker
from config import LANGUAGE
from exceptions import GoogleSearchError


class GoogleSearch:
    def __init__(self):
        self._reranker = get_reranker()

    def search(self, query: str, limit: int = 10) -> str:
        """
        Search for the most relevant documents based on the query.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :return:
            str: The titles and snippets of the documents found.
        """
        try:
            results = googlesearch.search(query, num_results=limit, lang=LANGUAGE, advanced=True)
            reranked_results = self._reranker.rerank(
                query, [
                    f"**{result.title}**\n---{result.description}---\nsource: {result.url}\n"
                    for result in results
                ]
            )
            return "\n".join([
                result.document
                for result in reranked_results
            ])
        except Exception as e:
            raise GoogleSearchError(f"Failed to fetch documents from Google: {e}")
