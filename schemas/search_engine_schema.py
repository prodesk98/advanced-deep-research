from typing import Optional

from pydantic import BaseModel


class BraveSearchResult(BaseModel):
    title: str
    snippet: str
    link: str


class SearchResult(BaseModel):
    title: str
    description: str
    content: Optional[str] = ""
    link: str


