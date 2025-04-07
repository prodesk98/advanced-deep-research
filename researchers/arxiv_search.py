from typing import Optional

import requests
from requests import RequestException

from llm import get_reranker, get_summarization
from exceptions import ArxivSearchError, ArxivDownloadError
from llm.reranker import Reranker
from llm.summarization import Summarization
from loggings import logger
from parsers import PDFParser
from schemas import SearchResult
from .base import BaseSearchService

import arxiv


class ArxivSearch(BaseSearchService):
    def __init__(self, reranker: Optional[Reranker] = None, summarization: Optional[Summarization] = None) -> None:
        self._client = arxiv.Client()
        self._reranker = reranker or get_reranker()
        self._summarization = summarization or get_summarization()

    @staticmethod
    def _download_pdf(pdf_url: Optional[str]) -> Optional[bytes]:
        """
        Download the PDF of a paper from arXiv.
        :param pdf_url:
        :return:
        """
        if not pdf_url:
            raise ValueError("PDF URL is empty.")
        if not pdf_url.startswith("http"):
            raise ValueError("Invalid PDF URL.")
        try:
            headers = {
                "Accept": "application/pdf",
            }
            response = requests.get(pdf_url, headers=headers)
            if not response.ok:
                raise ArxivDownloadError(f"Failed to download paper: {response.status_code}")
            return response.content
        except RequestException as e:
            raise ArxivDownloadError(f"RequestException Failed to download paper: {e}")
        except Exception as e:
            raise ArxivDownloadError(f"Failed to download paper: {e}")

    def search(self, query: str, limit: int = 3, parser: bool = True) -> str:
        """
        Search for papers on arXiv based on a query.
        :param parser:
        :param query: str
            The search query.
        :param limit: int
            The maximum number of results to return.
        :return:
            str: The titles and summaries of the papers found.
        """
        try:
            # Search for papers
            search = arxiv.Search(
                query=query,
                max_results=limit,
                sort_by=arxiv.SortCriterion.Relevance,
            )

            # Get the results
            results = [
                SearchResult(
                    title=result.title,
                    description=result.summary,
                    link=result.pdf_url,
                ) for result in self._client.results(search)
            ]

            if parser:
                pdf_parser = PDFParser()
                for result in results:
                    try:
                        pdf_content = self._download_pdf(result.link)
                        if not pdf_content:
                            raise ArxivDownloadError("PDF content is empty.")
                        if pdf_content:
                            result.content = self._summarization.summarize(
                                query,
                                pdf_parser.parse(values=pdf_content)
                            )
                    except ValueError as e:
                        logger(
                            f"Failed to parse the content from {result.entry_id}: {e}"
                        )
                    except ArxivDownloadError:
                        logger(
                            f"Failed to download the content from {result.entry_id}"
                            "error"
                        )

            reranked_results = self._reranker.rerank(
                query, [
                    f"**{result.title}**\n\n{result.description + result.content}"
                    for result in results
                ]
            )

            formatted_results = "\n".join(
                [
                    result.document
                    for result in reranked_results
                ]
            )
            return self._summarization.summarize(query, formatted_results)
        except Exception as e:
            raise ArxivSearchError(f"Failed to fetch papers from arXiv: {e}")
