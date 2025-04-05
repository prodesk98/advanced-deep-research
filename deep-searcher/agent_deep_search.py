from schemas import SubQueriesResultSchema
from services import SemanticSearch, GoogleSearch
from .base import DeepSearch


class AgentDeepSearch(DeepSearch):
    def __init__(self):
        super().__init__()
        self._namespace = "deep-searcher"
        self._semantic_search = SemanticSearch(namespace=self._namespace)
        self._google_search = GoogleSearch()


    def _generate_sub_queries(self, query: str) -> SubQueriesResultSchema:
        ...


    def run(self) -> str:
        pass

