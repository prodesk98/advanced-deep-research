from typing import Optional

from schemas import QueryResultSchema, UpsertSchema
from .base import BaseQdrant


class Qdrant(BaseQdrant):
    def __init__(self, namespace: Optional[str] = None):
        super().__init__(namespace)

    def upsert(self, data: list[UpsertSchema]) -> None:
        super().upsert(data)

    def query(self, vector: list[float], with_metadata: bool = True, limit: int = 10) -> list[QueryResultSchema]:
        return super().query(vector, with_metadata=with_metadata, limit=limit)

    def delete(self, ids: Optional[list[int]] = None, key: Optional[str] = None, value: Optional[str] = None) -> None:
        super().delete(ids, key, value)
