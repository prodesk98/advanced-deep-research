from abc import ABC
from typing import TypeVar, Optional, Type
from uuid import uuid4

from pydantic import BaseModel
from pymongo import MongoClient
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, FilterSelector, FieldCondition,
    MatchValue, Filter, VectorParams,
    PointStruct, PointsSelector
)

from config import QDRANT_DSN, QDRANT_COLLECTION
from config.environment import MONGODB_URI, MONGODB_DATABASE
from schemas import UpsertSchema, QueryResultSchema, MetadataSchema

_T = TypeVar("_T", bound=BaseModel)


class BaseMongoDB(ABC):
    def __init__(self):
        self._client = MongoClient(MONGODB_URI,  uuidRepresentation="standard")

    def initialize(self) -> None:
        conversations = self._client[MONGODB_DATABASE].get_collection("conversations")
        conversations.create_index("namespace")
        conversations.create_index("id", unique=True)

    def findOne(self, collection: str, filters: dict, T: Optional[Type[_T]] = None) -> Optional[_T | dict]:
        result = self._client[MONGODB_DATABASE].get_collection(collection).find_one(filters)
        if result is None:
            return None
        return T(**result) if T else result

    def find(self, collection: str, filters: dict, T: Optional[Type[_T]] = None, limit: int = 25) -> list[_T | dict]:
        result = self._client[MONGODB_DATABASE].get_collection(collection).find(filters).limit(limit)
        return [T(**r) for r in result] if T else list(result)

    def insertOne(self, collection: str, payload: _T | dict, T: Optional[Type[_T]] = None) -> None:
        if not isinstance(payload, dict):
            payload = payload.model_dump()
        self._client[MONGODB_DATABASE].get_collection(collection).insert_one(payload)

    def updateOne(self, collection: str, payload: Type[_T] | dict, filters: dict) -> None:
        if not isinstance(payload, dict):
            payload = payload.model_dump()
        self._client[MONGODB_DATABASE].get_collection(collection).update_one(filters, {"$set": payload})

    def deleteOne(self, collection: str, filters: dict) -> None:
        self._client[MONGODB_DATABASE].get_collection(collection).delete_one(filters)



class BaseQdrant(ABC):
    def __init__(self, namespace: Optional[str] = None):
        self._namespace = namespace or str(uuid4())
        self._client = QdrantClient(QDRANT_DSN)
        self._collection = QDRANT_COLLECTION

    def initialize(self) -> None:
        if self._client.collection_exists(self._collection):
            return # Collection already exists

        # Create a new collection
        self._client.create_collection(
            collection_name=self._collection,
            vectors_config=VectorParams(
                size=1024, # Dim size based jina-embeddings-v3
                distance=Distance.DOT,
            )
        )
        #
        # Create a payload index for the namespace
        self._client.create_payload_index(
            collection_name=self._collection,
            field_name="namespace",
            field_schema="keyword",
        )
        #

    def upsert(self, data: list[UpsertSchema]) -> None:
        self._client.upsert(
            collection_name=self._collection,
            points=[
                PointStruct(
                    id=d.id,
                    vector=d.vector,
                    payload=d.metadata.model_dump(),
                )
                for d in data
            ],
        )

    def query(self, vector: list[float], with_metadata: bool = True, limit: int = 10) -> list[QueryResultSchema]:
        return [
            QueryResultSchema(
                id=r.id,
                score=r.score,
                metadata=MetadataSchema(**r.payload),
            )
            for r in self._client.query_points(
                collection_name=self._collection,
                query=vector,
                query_filter=Filter(must=[FieldCondition(key="namespace", match=MatchValue(value=self._namespace))]),
                with_payload=with_metadata,
                limit=limit,
            ).points
        ]

    def delete(self, ids: Optional[list[int]] = None, key: Optional[str] = None, value: Optional[str] = None) -> None:
        """
        Delete points from the collection based on IDs or key-value pairs.
        :param ids:
        :param key:
        :param value:
        :return:
        """
        if ids is not None:
            self._client.delete(
                collection_name=self._collection,
                points_selector=PointsSelector(ids),
            )
        elif (
            key is not None and
            value is not None
        ):
            self._client.delete(
                collection_name=self._collection,
                points_selector=FilterSelector(
                    filter=Filter(
                        must=[
                            FieldCondition(
                                key=key,
                                match=MatchValue(value=value),
                            )
                        ],
                    )
                ),
            )

    @property
    def collection(self) -> str:
        return self._collection

    @property
    def namespace(self) -> str:
        return self._namespace
