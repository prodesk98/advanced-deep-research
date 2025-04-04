from factory import ConversationFactory
from schemas import Message
from services import SemanticSearch


class ConversationsManager:
    def __init__(self, namespace: str):
        self._namespace = namespace
        self._conversations_factory = ConversationFactory(namespace=self._namespace)
        self._semantic_search = SemanticSearch(namespace=self._namespace)

    def get_messages(self, limit: int = 50) -> list[Message]:
        return self._conversations_factory.all(limit)

    def add_message(self, message: Message) -> None:
        self._conversations_factory.add(message)

    def favorite(self, summary: str) -> None:
        self._semantic_search.upsert(summary)
