from asyncio import to_thread
from typing import Optional

import requests
from requests import HTTPError

from config import BRAVE_API_KEY
from exceptions import BraveSearchError
from researchers.base import BaseSearchService
from schemas import BraveSearchResult
from markdownify import markdownify as md


class BraveSearch(BaseSearchService):
    BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self, **kwargs):
        self._params = kwargs
        if not BRAVE_API_KEY:
            raise ValueError("BRAVE_API_KEY not found in environment variables.")

    def search(self, query: str, limit: int = 10) -> Optional[list["BraveSearchResult"]]:
        """
        Perform a search using the Brave Search API.
        :param limit:
        :param query: The search query.
        :return: A BraveSearchResult object containing the search results.
        """
        headers = {
            "X-Subscription-Token": BRAVE_API_KEY,
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params={"q": query, "count": limit, **self._params},
                headers=headers
            )
            response.raise_for_status()

            results = response.json()

            if "web" not in results:
                raise BraveSearchError("No web results found.")

            results = results["web"]["results"]

            return [
                BraveSearchResult(
                    title=result["title"],
                    snippet=md(result["description"]),
                    link=result["url"],
                ) for result in results
            ]

        except HTTPError as e:
            BraveSearchError(
                f"Failed to fetch results from Brave Search API: {e}"
            )
        except Exception as e:
            raise BraveSearchError(
                f"An unexpected error occurred: {e}"
            )

    async def asearch(self, query: str, limit: int = 5) -> Optional[list["BraveSearchResult"]]:
        """
        Perform an asynchronous search using the Brave Search API.
        :param query:
        :param limit:
        :return:
        """
        return to_thread(self.search, query, limit)
