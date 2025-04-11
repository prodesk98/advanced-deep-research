from abc import ABC, abstractmethod
from schemas import SearchResult
from typing import Optional


class BaseSearchService(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    async def asearch(self, query: str, limit: int = 5) -> list[SearchResult]:
        raise NotImplementedError("Subclasses should implement this method.")

    def query(self, query: str, limit: int = 5) -> list[SearchResult]:
        raise NotImplementedError("Subclasses should implement this method.")

    def upsert(self, document, document_id: Optional[str] = None) -> None:
        raise NotImplementedError("Subclasses should implement this method.")
