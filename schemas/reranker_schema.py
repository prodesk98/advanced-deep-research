from typing import Optional

from pydantic import BaseModel


class RerankRequest(BaseModel):
    query: str
    documents: list[str]


class RerankedDocument(BaseModel):
    document: str
    score: Optional[float] = None


class RerankResponse(BaseModel):
    reranked: list[RerankedDocument]
