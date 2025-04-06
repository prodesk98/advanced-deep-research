from exceptions import GenerativeError, GoogleSearchError, SemanticSearchError, ArxivSearchError
from llm.openai_llm import OpenAILLM
from loggings import logger
from services import SemanticSearch, GoogleSearch, ArxivSearch
from .base import DeepSearch


class AgentDeepSearch(DeepSearch):
    def __init__(self):
        super().__init__()
        self.depth: int = 0
        self._namespace = "deep-searcher"
        self._semantic_search = SemanticSearch(namespace=self._namespace)
        self._arxiv_search = ArxivSearch()
        self._google_search = GoogleSearch()
        self._llm = OpenAILLM(namespace=self._namespace)

    def _generate_sub_queries(self, query: str) -> list[str]:
        """
        Generate sub-queries based on the provided query.
        :param query:
        :return:
        """
        try:
            sub_queries = self._llm.generate_sub_queries(query)
            return sub_queries
        except GenerativeError as e:
            raise e

    def _summarize_results(self, query: str, documents: list[str], terminate: bool = False) -> str:
        """
        Summarize the results based on the provided query.
        :param query:
        :param documents:
        :return:
        """
        try:
            summary = self._llm.summarize(query, documents)
            if terminate:
                self._semantic_search.upsert(summary) # Save the summary to the semantic search (Vector DB)
            return summary
        except GenerativeError as e:
            raise e

    def _reflection(self, query: str, sub_queries: list[str], chunks: list[str]) -> list[str]:
        """
        Generate a reflection based on the provided query, sub-queries, and chunks.
        :param query:
        :param sub_queries:
        :param chunks:
        :return:
        """
        try:
            reflection = self._llm.reflection(query, sub_queries, chunks)
            return reflection
        except GenerativeError as e:
            raise e

    def _query_google(self, query: str) -> str:
        """
        Perform a Google search based on the provided query.
        :param query:
        :return:
        """
        try:
            result = self._google_search.search(query)
            return result
        except GoogleSearchError as e:
            raise e

    def _query_arxiv(self, query: str) -> str:
        """
        Perform an Arxiv search based on the provided query.
        :param query:
        :return:
        """
        try:
            result = self._arxiv_search.search(query)
            return result or ""
        except ArxivSearchError as e:
            raise e

    def _query_documents(self, query: str) -> str:
        """
        Perform a Documents search based on the provided query.
        :param query:
        :return:
        """
        try:
            result = self._semantic_search.search(query)
            return "\n".join([r.text for r in result])
        except SemanticSearchError as e:
            raise e

    def _len_tokens(self, documents: list[str]) -> int:
        return self.calc_tokens() + len(self._tokenizer.encode("\n".join(documents)))

    def run(self, query: str) -> str:
        # 1. Submit a research query
        # 2. Generate sub-queries
        # 3. Search for documents using Semantic search and Google search
        # 4. Combine the results and return and summarize them
        # 5. Reflect on the results and generate new sub-queries
        # 6. Repeat the process until a stopping condition is met
        # 7. Return the final results

        sub_queries = self._generate_sub_queries(query)

        while (
            self.calc_tokens() < self.max_tokens * 2 and
            self.depth < self.max_depth and
            len(sub_queries) > 0
        ):
            for sub_query in sub_queries:
                try:
                    # Search for documents using Semantic search and Google search
                    documents_results = self._query_documents(sub_query)
                    google_results = self._query_google(sub_query)
                    arxiv_results = self._query_arxiv(sub_query)
                except GoogleSearchError as e:
                    logger(e.message, "error")
                    continue
                except ArxivSearchError as e:
                    logger(e.message, "error")
                    continue
                except SemanticSearchError as e:
                    logger(e.message, "error")
                    continue

                # Combine the results and return and summarize them
                combined_results = [documents_results, google_results, arxiv_results]
                if self._len_tokens(combined_results) > self.max_tokens:
                    break
                summary = self._summarize_results(sub_query, combined_results)
                # Append the summary to the chunks
                self._chunks.append(summary)

            # Reflect on the results and generate new sub-queries
            reflection = self._reflection(query, sub_queries, self._chunks)
            # Increment depth
            self.depth += 1

            # Check if the reflection is empty
            if len(reflection) == 0:
                break

            # Generate new sub-queries
            sub_queries = reflection

        return self._summarize_results(query, self._chunks, True)

