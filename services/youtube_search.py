from typing import Optional

from pydantic import BaseModel

from exceptions import YoutubeSearchError
from llm import get_summarization
from llm.summarization import Summarization
from loggings import logger
from utils import YoutubeParser
from .base import BaseSearchService
from youtube_search import YoutubeSearch as YoutubeSearchAPI


class SearchResult(BaseModel):
    video_id: str
    content: Optional[str] = None


class YoutubeSearch(BaseSearchService):
    def __init__(self, summarization: Optional[Summarization] = None):
        self._youtube_parser = YoutubeParser()
        self._summarization = summarization or get_summarization()

    def search(self, query: str, limit: int = 5, parser: bool = True) -> list[SearchResult]:
        """
        Search Videos on YouTube based on the query.
        :param query:
        :param limit:
        :param parser:
        :return:
        """
        try:
            results: list[dict] = []
            youtube_search_api = YoutubeSearchAPI(query, max_results=limit).to_dict()
            if parser:
                for result in youtube_search_api:
                    data = {"video_id": result["id"]}
                    try:
                        contents = self._youtube_parser.fetch(result["url_suffix"])
                        data["content"] = self._summarization.summarize(query, contents)
                    except Exception as e:
                        logger(e, "error")
                        pass
                    results.append(data)
            else:
                results = [{"video_id": result["id"]} for result in youtube_search_api]
            return [SearchResult(**result) for result in results]
        except YoutubeSearchError as e:
            raise YoutubeSearchError(f"Failed to fetch documents from YouTube: {e.message}")
        except Exception as e:
            raise YoutubeSearchError(f"An unexpected error occurred: {str(e)}")
