from pydantic import BaseModel, Field


class TranscriptYoutubeVideoSchema(BaseModel):
    video_url: str = Field(
        ...,
        title="Video URL",
        description="URL of the YouTube video to be transcribed",
    )


class ScrappingWebSiteSchema(BaseModel):
    url: str = Field(
        ...,
        title="URL",
        description="URL of the website to be scraped",
    )


class ArxivPaperSearchSchema(BaseModel):
    query: str = Field(
        ...,
        title="Search Query",
        description="The search query to find papers on arXiv",
    )
    max_results: int = Field(
        5,
        title="Max Results",
        description="The maximum number of results to return",
    )


class SearchDocumentsSchema(BaseModel):
    query: str = Field(
        ...,
        title="Search Query",
        description="The search query to find documents in the database",
    )
    max_results: int = Field(
        10,
        title="Max Results",
        description="The maximum number of results to return",
    )


class SearchGoogleEngineSchema(BaseModel):
    query: str = Field(
        ...,
        title="Search Query",
        description="The search query to find documents in the database",
    )
    max_results: int = Field(
        10,
        title="Max Results",
        description="The maximum number of results to return",
    )