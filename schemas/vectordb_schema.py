from uuid import uuid4

from pydantic import BaseModel, Field


class UpsertSchema(BaseModel):
    id: int = Field(
        default_factory=lambda: (uuid4().int >> 64) & ((1 << 64) - 1),
        title="ID",
        description="The ID of the vector. It must be unique.",
    )
    vector: list[float]
    metadata: dict


class QueryResultSchema(BaseModel):
    id: int = Field(
        ...,
        title="ID",
        description="The ID of the vector. It must be unique.",
    )
    score: float = Field(
        ...,
        title="Score",
        description="The score of the vector.",
    )
    metadata: dict = Field(
        ...,
        title="Metadata",
        description="The metadata of the vector.",
    )
