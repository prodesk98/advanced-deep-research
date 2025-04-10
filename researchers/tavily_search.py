from tavily import TavilyClient
from config import TAVILY_API_KEY
from schemas import TavilySearchResult, SearchResult
from .base import BaseSearchService
from exceptions import TavilySearchError


class TavilySearch(BaseSearchService):
    """
    TavilySearch is a class that provides a search interface using the Tavily API.
    """
    def __init__(self, **kwargs):
        self._params = kwargs
        self._client = TavilyClient(api_key=TAVILY_API_KEY)

        if isinstance(TAVILY_API_KEY, str) and not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not found in environment variables.")

    def search(self, query: str, limit: int = 5) -> list[TavilySearchResult]:
        """
        Perform a search using the Tavily API.
        :param query:
        :param limit:
        :return:
        """
        try:
            results = self._client.search(
                query,
                max_results=limit,
                **self._params,
            )

            if not "results" in results:
                raise TavilySearchError("No results found.")

            return [
                TavilySearchResult(
                    title=result.get("title"),
                    snippet=result.get("content"),
                    link=result.get("url"),
                )
                for result in results["results"]
            ]
        except Exception as e:
            raise TavilySearchError(f"Failed to fetch results from Tavily API: {e}")

    async def asearch(self, query: str, limit: int = 5) -> list["SearchResult"] | str:
        pass
