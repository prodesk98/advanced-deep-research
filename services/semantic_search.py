from typing import Optional
from uuid import uuid4

from langchain_text_splitters import CharacterTextSplitter

from databases import Qdrant
from llm import get_embeddings, get_reranker
from llm.embeddings import Embeddings
from llm.reranker import Reranker
from schemas import MetadataSchema, UpsertSchema
from .base import BaseSearchService
from exceptions import SemanticSearchError, SemanticUpsertError, InvalidRerankValue, RerankError


class SemanticSearch(BaseSearchService):
    def __init__(
        self,
        namespace: str,
        qdrant: Optional[Qdrant] = None,
        reranker: Optional[Reranker] = None,
        embeddings: Optional[Embeddings] = None
    ):
        self._namespace = namespace
        self._splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base", chunk_size=512, chunk_overlap=0
        )
        self._vectorstore = qdrant or Qdrant(self._namespace)
        self._embedding = embeddings or get_embeddings()
        self._reranker = reranker or get_reranker()

    def search(self, query: str, limit: int = 10, parser: bool = False) -> list[dict]:
        """
        Search for the most relevant documents based on the query.
        :param query: The query string to search for.
        :param limit: The maximum number of results to return.
        :param parser: Whether to parse the results or not.
        :return: A list of dictionaries containing the search results.
        """
        try:
            vectors = self._embedding.embed([query])
            results = self._vectorstore.query(vectors[0], limit=limit)
            reranked_results = self._reranker.rerank(query, [result.metadata.text for result in results])
            return [
                {
                    "score": result.score,
                    **result.metadata,
                }
                for result in reranked_results
            ]
        except InvalidRerankValue as e:
            raise SemanticSearchError(
                f"Invalid rerank value: {e.message}"
            )
        except RerankError as e:
            raise SemanticSearchError(
                f"Failed to rerank documents: {e.message}"
            )
        except Exception as e:
            raise SemanticSearchError(
                f"Failed to perform semantic search: {e}"
            )

    def upsert(self, document: str) -> None:
        """
        Upsert a document into the vector database.
        :param document:
        :return:
        """
        try:
            document_id = str(uuid4())                      # Generate a unique document ID
            texts = self._splitter.split_text(document)     # Split the document into chunks
            vectors = self._embedding.embed(texts)          # Embed the chunks
            metadata = [
                MetadataSchema(
                    text=text,
                    document_id=document_id,
                    namespace=self._namespace,
                )
                for text in texts
            ]
            payload = [
                UpsertSchema(
                    vector=v,
                    metadata=m,
                )
                for v, m in zip(vectors, metadata)
            ]
            self._vectorstore.upsert(payload)
        except Exception as e:
            raise SemanticUpsertError(
                f"Failed to upsert document into vector database: {e}"
            )
