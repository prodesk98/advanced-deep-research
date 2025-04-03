from pydantic import BaseModel


class EmbeddingsRequest(BaseModel):
    texts: list[str] = []


class EmbeddingsResponse(BaseModel):
    embeddings: list[list[float]] = []
