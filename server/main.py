from fastapi import FastAPI, HTTPException

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
    try:
        embeddings_result = await embed_texts(payload.texts)
        return EmbeddingsResponse(
            embeddings=embeddings_result
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during embedding: {str(e)}"
        )


@app.post("/rerank", response_model=RerankResponse)
async def rerank(
    payload: RerankRequest,
) -> RerankResponse:
    try:
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during reranking: {str(e)}"
        )

