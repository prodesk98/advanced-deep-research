from uuid import uuid4

from pydantic import BaseModel, Field


class MetadataSchema(BaseModel):
    text: str = Field(
        ...,
        title="Text",
        description="The text of the vector.",
    )
    document_id: str = Field(
        default_factory=lambda: str(uuid4()),
        title="Document ID",
        description="The ID of the document.",
    )
    namespace: str = Field(
        default="default",
        title="Namespace",
        description="The namespace of the vector.",
    )


class UpsertSchema(BaseModel):
    id: int = Field(
        default_factory=lambda: (uuid4().int >> 64) & ((1 << 64) - 1),
        title="ID",
        description="The ID of the vector. It must be unique.",
    )
    vector: list[float]
    metadata: MetadataSchema


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
    metadata: MetadataSchema = Field(
        ...,
        title="Metadata",
        description="The metadata of the vector.",
    )


class SearchResultSchema(BaseModel):
    score: float
    text: str
