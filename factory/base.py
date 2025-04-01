from typing import Optional, TypeVar, Type

from pydantic import BaseModel

from databases import db

_T = TypeVar("_T", bound=BaseModel)


class BaseFactory:
    def __init__(self, collection: str, namespace: Optional[str] = None, T: Optional[Type[_T]] = None):
        self.T: Optional[Type[_T]] = T
        self._collection = collection
        self._namespace = namespace
        self._db = db

    def all(self, limit: int = 50) -> list[_T]:
        return self.db.find(filters={"namespace": self._namespace}, T=self.T, limit=limit)

    def add(self, item: _T) -> None:
        if not getattr(item, "namespace", None):
            if self._namespace:
                item.namespace = self._namespace
            else:
                raise ValueError("Item must have a 'namespace' attribute or a factory with namespace set.")
        self.db.insertOne(payload=item, T=self.T)

    def delete(self) -> None:
        if self._namespace is None:
            raise ValueError("Namespace is not set")
        self.db.deleteOne(filters={"namespace": self._namespace})

    @property
    def db(self):
        return self._db
