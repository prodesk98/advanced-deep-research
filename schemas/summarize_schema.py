from pydantic import BaseModel, Field


class SummarizeResponse(BaseModel):
    summary: str = Field(
        ...,
        description="Summary of the document."
    )


class SummarizeRequest(BaseModel):
    query: str = Field(
        ...,
        description="Query to summarize documents."
    )
    document: str = Field(
        ...,
        description="Document to summarize.",
    )
