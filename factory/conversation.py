from typing import Optional

from pydantic import UUID4

from schemas import Message
from .base import BaseFactory


class ConversationFactory(BaseFactory):
    def __init__(self, namespace: Optional[str] = None):
        super().__init__(
            collection="conversations",
            namespace=namespace,
            T=Message
        )

    def all(self, limit: int = 50) -> list[Message]:
        return super().all(limit=limit)

    def add(self, message: Message) -> None:
        message.namespace = UUID4(self._namespace)  # Add namespace to message
        super().add(message)

    def delete(self) -> None:
        super().delete()
