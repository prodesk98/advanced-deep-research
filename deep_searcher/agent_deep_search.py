from typing import Optional

from streamlit.delta_generator import DeltaGenerator

from exceptions import (
    GenerativeError,
    SearchEngineError,
    BraveSearchError,
    SemanticSearchError,
    ArxivSearchError,
    SemanticUpsertError
)
from loggings import logger
from schemas import ReflectionResultSchema
from researchers import SemanticSearch, SearchEngine, ArxivSearch
from .base import DeepSearch
from llm.base import BaseLLM


class AgentDeepSearch(DeepSearch):
    FLAG = "**🧠🔍 Deep Research Agent**"

    def __init__(
        self,
        llm: BaseLLM,
        max_depth: int = 3,
        max_tokens: int = 4096,
        result_limit: int = 5,
        ui: Optional[DeltaGenerator] = None,
    ):
        super().__init__(max_depth, max_tokens)
        self._depth: int = 0
        self._result_limit = result_limit
        self._ui = ui
        self._namespace = "deep-searcher"
        self._semantic_search = SemanticSearch(namespace=self._namespace)
        self._arxiv_search = ArxivSearch()
        self._search_engine = SearchEngine()
        self._llm = llm

    def _upsert_documents(self, document: str) -> None:
        """
        Upsert documents to the vector store.
        :param document:
        :return:
        """
        try:
            self._semantic_search.upsert(document)
        except SemanticUpsertError as e:
            logger(
                f"{self.FLAG} Error upserting document: {e.message}",
                "error",
                self._ui,
            )

    def _generate_sub_queries(self, query: str) -> list[str]:
        """
        Generate sub-queries based on the provided query.
        :param query:
        :return:
        """
        logger(
            f"{self.FLAG} Generating sub-queries for the query: {query}",
            "info",
            self._ui,
        )
        try:
            sub_queries = self._llm.generate_sub_queries(query)
            result = sub_queries
            if not isinstance(result, list):
                logger(
                    f"{self.FLAG} Error generating sub-queries. Expected a list but got {type(result)}",
                    "error",
                    self._ui,
                )
                raise GenerativeError("Sub-queries must be a list.")
            if len(result) == 0:
                logger(
                    f"{self.FLAG} No sub-queries generated.",
                    "warning",
                    self._ui,
                )
                return []
            logger(
                f"{self.FLAG} Generated sub-queries: %s" % ", ".join(result),
                "info",
                self._ui,
            )
            return result
        except GenerativeError as e:
            logger(
                f"{self.FLAG} Error generating sub-queries: {e.message}",
                "error",
                self._ui,
            )
            raise e

    def _summarize_results(self, query: str, documents: list[str]) -> str:
        """
        Summarize the results based on the provided query.
        :param query:
        :param documents:
        :return:
        """
        logger(
            f"{self.FLAG} Summarizing results for the query: {query}\nchunks: %s" % "\n".join(documents),
            "info",
            self._ui,
        )
        try:
            summary = self._llm.summarize(query, documents)
            if not isinstance(summary, str):
                logger(
                    f"{self.FLAG} Error summarizing results. Expected a string but got {type(summary)}",
                    "error",
                    self._ui,
                )
                raise GenerativeError("Summary must be a string.")
            if len(summary) == 0:
                logger(
                    f"{self.FLAG} No summary generated.",
                    "warning",
                    self._ui,
                )
                return ""
            logger(
                f"{self.FLAG} Generated summary: {summary}",
                "info",
                self._ui,
            )
            return summary
        except GenerativeError as e:
            logger(
                f"{self.FLAG} Error generating summary: {e.message}",
                "error",
                self._ui,
            )
            raise e

    def _reflection(self, query: str, sub_queries: list[str], chunks: list[str]) -> ReflectionResultSchema:
        """
        Generate a reflection based on the provided query, sub-queries, and chunks.
        :param query:
        :param sub_queries:
        :param chunks:
        :return:
        """
        logger(
            f"{self.FLAG} Generating reflection for the query: {query}\nsub_queries: %s" % "\n".join(sub_queries),
            "info",
            self._ui,
        )
        try:
            reflection = self._llm.reflection(query, sub_queries, chunks)
            logger(
                f"{self.FLAG} Generated reflection: %s" % "\n".join(reflection.sub_queries),
                "info",
                self._ui,
            )
            return reflection
        except GenerativeError as e:
            logger(
                f"{self.FLAG} Error generating reflection: {e.message}",
                "error",
                self._ui,
            )
            raise e

    def _query_search_engine(self, query: str) -> str:
        """
        Perform a search engine query based on the provided query.
        :param query:
        :return:
        """
        logger(
            f"{self.FLAG} Performing Google search for the query: {query}",
            "info",
            self._ui,
        )
        try:
            result = self._search_engine.search(query, limit=self._result_limit)
            if not isinstance(result, str):
                logger(
                    f"{self.FLAG} Error performing Google search. Expected a string but got {type(result)}",
                    "error",
                    self._ui,
                )
                raise GenerativeError("Google search result must be a string.")
            if len(result) == 0:
                logger(
                    f"{self.FLAG} No Google search result found.",
                    "warning",
                    self._ui,
                )
                return ""
            logger(
                f"{self.FLAG} Google search result: {result}",
                "info",
                self._ui,
            )
            return result
        except SearchEngineError as e:
            logger(
                f"{self.FLAG} Error performing Google search: {e.message}",
                "error",
                self._ui,
            )
            raise e
        except BraveSearchError as e:
            logger(
                f"{self.FLAG} Error performing Brave search: {e.message}",
                "error",
                self._ui,
            )
            raise e

    def _query_arxiv(self, query: str) -> str:
        """
        Perform an Arxiv search based on the provided query.
        :param query:
        :return:
        """
        logger(
            f"{self.FLAG} Performing Arxiv search for the query: {query}",
            "info",
            self._ui,
        )

        try:
            result = self._arxiv_search.search(query, limit=self._result_limit)
            if not isinstance(result, str):
                logger(
                    f"{self.FLAG} Error performing Arxiv search. Expected a string but got {type(result)}",
                    "error",
                    self._ui,
                )
                raise GenerativeError("Arxiv search result must be a string.")
            if len(result) == 0:
                logger(
                    f"{self.FLAG} No Arxiv search result found.",
                    "warning",
                    self._ui,
                )
                return ""
            logger(
                f"{self.FLAG} Arxiv search result: {result}",
                "info",
                self._ui,
            )
            return result or ""
        except ArxivSearchError as e:
            logger(
                f"{self.FLAG} Error performing Arxiv search: {e.message}",
                "error",
                self._ui,
            )
            raise e

    def _query_documents(self, query: str) -> str:
        """
        Perform a Documents search based on the provided query.
        :param query:
        :return:
        """
        logger(
            f"{self.FLAG} Performing Document search for the query: {query}",
            "info",
            self._ui,
        )

        try:
            result = self._semantic_search.search(query, limit=self._result_limit)
            if not isinstance(result, list):
                logger(
                    f"{self.FLAG} Error performing Document search. Expected a list but got {type(result)}",
                    "error",
                    self._ui,
                )
                raise GenerativeError("Document search result must be a list.")
            if len(result) == 0:
                logger(
                    f"{self.FLAG} No Document search result found.",
                    "warning",
                    self._ui,
                )
                return ""
            logger(
                f"{self.FLAG} Document search result: %s" % "\n".join([r.text for r in result]),
                "info",
                self._ui,
            )
            return "\n".join([r.text for r in result])
        except SemanticSearchError as e:
            logger(
                f"{self.FLAG} Error performing Document search: {e.message}",
                "error",
                self._ui,
            )
            raise e

    def _len_tokens(self, documents: list[str]) -> int:
        return self.calc_tokens() + len(self._tokenizer.encode("\n".join(documents)))

    def _pipeline_search(self, query: str) -> list[str]:
        results = []
        functions = {
            # "documents": self._query_documents, # TODO: Enable this when the vector store is ready
            "search_engine": self._query_search_engine,
            "arxiv": self._query_arxiv,
        }
        for name, func in functions.items():
            try:
                result = func(query) # type: ignore
                if result and len(result) > 0:
                    results.append(result)
            except (SearchEngineError, BraveSearchError, ArxivSearchError, SemanticSearchError) as e:
                logger(
                    f"{self.FLAG} Error performing {name} search: {e.message}",
                    "error",
                    self._ui,
                )
            except Exception as e:
                logger(
                    f"{self.FLAG} Error performing {name} search: {e}",
                    "error",
                    self._ui,
                )
        return results

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
            self.calc_tokens() < self.max_tokens and
            self._depth < self.max_depth and
            len(sub_queries) > 0
        ):
            for sub_query in sub_queries:
                # Combine the results and return and summarize them
                combined_results = self._pipeline_search(sub_query)
                # Append the summary to the chunks
                self._chunks.append(self._summarize_results(sub_query, combined_results))

            # Reflect on the results and generate new sub-queries
            summary = self._summarize_results(query, self._chunks)
            self._upsert_documents(summary)
            reflection = self._reflection(query, sub_queries, [summary])
            # Increment depth
            self._depth += 1

            # Check if the reflection is empty or if the search is complete
            if (
                len(reflection.sub_queries) == 0 or
                reflection.complete_search
            ):
                break

            # Generate new sub-queries
            sub_queries = reflection.sub_queries

        return self._summarize_results(query, self._chunks)

