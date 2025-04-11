from fastapi import FastAPI, HTTPException
from server.schemas import (
    EmbeddingsRequest,
    RerankRequest,
    EmbeddingsResponse,
    RerankResponse,
    RerankedDocument,
    SummarizeRequest,
    SummarizeResponse,
)
from server.core import (
    embed_texts,
    rerank_documents,
    summarization_text
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
    """
    Generate embeddings for the provided texts.
    :param payload:
    :return:
    """
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
    """
    Rerank the provided documents based on the query.
    :param payload:
    :return:
    """
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

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(
    payload: SummarizeRequest
) -> SummarizeResponse:
    """
    Summarize the provided document based on the query.
    Contents English recommended
    :param payload:
    :return:
    """
    try:
        summary = await summarization_text(payload.query, payload.document)
        return SummarizeResponse(
            summary=summary
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during summarization: {str(e)}"
        )
