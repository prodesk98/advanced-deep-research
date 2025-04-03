from typing import Literal

from pydantic import BaseModel, Field

## Embedding Models Base
class EmbeddingsRequest(BaseModel):
    model: Literal[
        "jinaai/jina-embeddings-v3",
    ] = Field(
        "jinaai/jina-embeddings-v3",
        description="Model to use for generating embeddings."
    )
    texts: list[str] = Field(
        ...,
        description="List of texts to generate embeddings for.",
        max_length=10,
    )


class EmbeddingsResponse(BaseModel):
    embeddings: list[list[float]]
##

## Rerank Models Base
class RerankRequest(BaseModel):
    model: Literal[
        "jinaai/jina-reranker-v2-base-multilingual",
    ] = Field(
        "jinaai/jina-reranker-v2-base-multilingual",
        description="Model to use for reranking."
    )
    query: str = Field(
        ...,
        description="Query to rerank documents."
    )
    documents: list[str] = Field(
        ...,
        description="List of documents to rerank.",
        max_length=10,
    )

class RerankedDocument(BaseModel):
    document: str
    score: float

class RerankResponse(BaseModel):
    reranked: list[RerankedDocument]
#
