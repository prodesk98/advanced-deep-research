from fastapi import FastAPI

from server.schemas import (
    EmbeddingsRequest,
    RerankRequest,
    EmbeddingsResponse,
    RerankResponse,
    RerankedDocument
)
from server.core import (
    embed_texts,
    rerank_documents
)

app = FastAPI(
    title="Rerank And Embedding API",
    description="Utility API for embedding and reranking.",
    version="0.1.0",
)


@app.post("/embeddings", response_model=EmbeddingsResponse)
async def embeddings(
    payload: EmbeddingsRequest,
) -> EmbeddingsResponse:
    embeddings_result = await embed_texts(payload.texts)
    print(len(embeddings_result[0]))
    return EmbeddingsResponse(
        embeddings=embeddings_result
    )


@app.post("/rerank", response_model=RerankResponse)
async def rerank(
    payload: RerankRequest,
) -> RerankResponse:
    rerank_result = await rerank_documents(payload.query, payload.documents)
    documents, scores = rerank_result
    return RerankResponse(
        reranked=[
            RerankedDocument(
                document=doc,
                score=score
            )
            for doc, score in zip(documents, scores)
        ]
    )

