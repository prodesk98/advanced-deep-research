from typing import Optional

from schemas import Conversation
from .base import BaseFactory


class ConversationFactory(BaseFactory):
    def __init__(self, namespace: Optional[str] = None):
        super().__init__(
            collection="conversations",
            namespace=namespace,
            T=Conversation
        )

    def all(self, limit: int = 50) -> list[Conversation]:
        return super().all(limit=limit)

    def add(self, conversation: Conversation) -> None:
        conversation.namespace = self._namespace  # Add namespace to conversation
        super().add(conversation)

    def delete(self) -> None:
        super().delete()
