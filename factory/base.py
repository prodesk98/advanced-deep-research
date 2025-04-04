from typing import Optional, TypeVar, Type

from pydantic import BaseModel

from databases import MongoDB, get_db

_T = TypeVar("_T", bound=BaseModel)


class BaseFactory:
    def __init__(
        self,
        collection: str,
        namespace: Optional[str] = None,
        T: Optional[Type[_T]] = None,
        db: Optional[MongoDB] = None
    ):
        self.T: Optional[Type[_T]] = T
        self._collection = collection
        self._namespace = namespace
        self._db = db or get_db()

    def all(self, limit: int = 50) -> list[_T]:
        return self._db.find(
            collection=self._collection,
            filters={"namespace": self._namespace},
            T=self.T,
            limit=limit
        )

    def add(self, item: _T) -> None:
        if not getattr(item, "namespace", None):
            if self._namespace:
                item.namespace = self._namespace
            else:
                raise ValueError("Item must have a 'namespace' attribute or a factory with namespace set.")
        self._db.insertOne(collection=self._collection, T=self.T, payload=item)

    def delete(self) -> None:
        if self._namespace is None:
            raise ValueError("Namespace is not set")
        self._db.deleteOne(collection=self._collection, filters={"namespace": self._namespace})
