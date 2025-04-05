from abc import ABC, abstractmethod
from typing import Optional


class BaseSearchService(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 5, parser: bool = True):
        raise NotImplementedError("Subclasses should implement this method.")

    def upsert(self, document, document_id: Optional[str] = None):
        raise NotImplementedError("Subclasses should implement this method.")
