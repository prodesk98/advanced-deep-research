from pydantic import BaseModel


class RerankRequest(BaseModel):
    query: str
    documents: list[str]

class RerankedDocument(BaseModel):
    document: str
    score: float


class RerankResponse(BaseModel):
    reranked: list[RerankedDocument]
