from databases import Qdrant
from llm import EmbeddingOpenAI


class SemanticSearch:
    def __init__(self, namespace: str):
        self._namespace = namespace
        self._vectordb = Qdrant(namespace)
        self._embedding = EmbeddingOpenAI()

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """
        Search for the most relevant documents based on the query.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :return: A list of dictionaries containing the search results.
        """
        vector = self._embedding.embed(query)
        results = self._vectordb.query(vector, limit=limit)
        return [
            {
                "score": result.score,
                **result.metadata,
            }
            for result in results
        ]