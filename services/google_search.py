import googlesearch

from config import LANGUAGE


class GoogleSearch:
    @staticmethod
    def search(query: str, limit: int = 10) -> list[dict]:
        """
        Search for the most relevant documents based on the query.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :return: A list of dictionaries containing the search results.
        """
        results = googlesearch.search(query, num_results=limit, lang=LANGUAGE, advanced=True)
        return [
            {
                "title": result.title,
                "link": result.url,
                "description": result.description.strip(),
            }
            for result in results
        ]
