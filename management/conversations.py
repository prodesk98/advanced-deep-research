from config import USE_CHAT_MEMORY
from factory import ConversationFactory
from schemas import Message
from researchers import SemanticSearch


class ConversationsManager:
    def __init__(self, chat_id: str):
        self._chat_id = chat_id
        self._conversations_factory = ConversationFactory(namespace=self._chat_id)
        self._semantic_search = SemanticSearch(namespace=self._chat_id)

    def get_messages(self, limit: int = 50) -> list[Message]:
        return self._conversations_factory.all(limit)

    def add_message(self, message: Message) -> None:
        if not USE_CHAT_MEMORY:
            return
        self._conversations_factory.add(message)

    def favorite(self, summary: str) -> None:
        self._semantic_search.upsert(summary)
