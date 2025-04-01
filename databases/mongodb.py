from typing import Optional, TypeVar, Type

from pydantic import BaseModel

from .base import BaseMongoDB

_T = TypeVar("_T", bound=BaseModel)


class MongoDB(BaseMongoDB):
    def __init__(self):
        super().__init__()

    def findOne(self, collection: str, filters: Optional[dict] = None, T: Optional[Type[_T]] = None) -> Optional[_T | dict]:
        return super().findOne(collection, filters or {}, T)

    def find(self, collection: str, filters: Optional[dict] = None, T: Optional[Type[_T]] = None, limit: int = 25) -> list[_T | dict]:
        return super().find(collection, filters or {}, T)

    def insertOne(self, collection: str, payload: _T | dict, T: Optional[Type[_T]] = None) -> None:
        super().insertOne(collection, payload, T)

    def updateOne(self, collection: str, payload: Type[_T] | dict, filters: Optional[dict] = None) -> None:
        super().updateOne(collection, filters or {}, payload)

    def deleteOne(self, collection: str, filters: Optional[dict] = None) -> None:
        super().deleteOne(collection, filters or {})
