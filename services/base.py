from abc import ABC, abstractmethod


class BaseSearchService(ABC):
    @abstractmethod
    def search(self, query: str, limit: int = 5, parser: bool = True):
        raise NotImplementedError("Subclasses should implement this method.")

    def upsert(self, document):
        raise NotImplementedError("Subclasses should implement this method.")
