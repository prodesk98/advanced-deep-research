from typing import Optional

from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    snippet: str
    link: Optional[str] = None


class BraveSearchResult(SearchResult):
    title: str
    snippet: str
    link: str


class TavilySearchResult(SearchResult):
    title: str
    snippet: str
    link: str


