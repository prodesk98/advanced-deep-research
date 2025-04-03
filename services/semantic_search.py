from databases import Qdrant
from llm import get_embeddings, get_reranker
from exceptions import SemanticSearchError


class SemanticSearch:
    def __init__(self, namespace: str = "default"):
        self._namespace = namespace
        self._vectordb = Qdrant(namespace)
        self._embedding = get_embeddings()
        self._reranker = get_reranker()

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """
        Search for the most relevant documents based on the query.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :return: A list of dictionaries containing the search results.
        """
        try:
            vectors = self._embedding.embed([query])
            results = self._vectordb.query(vectors[0], limit=limit)
            reranked_results = self._reranker.rerank(query, [result.metadata['text'] for result in results])
            return [
                {
                    "score": result.score,
                    **result.metadata,
                }
                for result in reranked_results
            ]
        except Exception as e:
            raise SemanticSearchError(
                f"Failed to perform semantic search: {e}"
            )
