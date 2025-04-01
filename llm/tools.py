from typing import Optional

from loggings import logger
from utils import (
    SiteParser,
    ArxivParser,
    YoutubeParser
)


def TranscriptYoutubeVideo(video_url: str) -> Optional[str]:
    """
    Fetch the transcript of a YouTube video.
    :param video_url: Str
        YouTube Video URL to fetch the transcript from.
    :return:
    """

    try:
        youtube_parser = YoutubeParser()
        return youtube_parser.fetch(video_url)
    except Exception as e:
        logger(e, level="error")


def ScrappingWebSite(url: str) -> Optional[str]:
    """
    Scrape a website and convert its content to markdown.
    :param url: str
        URL of the website to scrape.
    :return:
        Optional[str]: The content of the website in Markdown format.
    """
    try:
        # Parse Website Constructor
        site_parser = SiteParser(url)
        # Convert the content to markdown
        return site_parser.to_markdown()
    except Exception as e:
        logger(e, level="error")


def ArxivPaperSearch(query: str, max_results: int = 3) -> Optional[str]:
    """
    Search for papers on arXiv based on a query.
    :param query: Str
        The search query.
    :param max_results: Int
        The maximum number of results to return.
    :return:
        Optional[str]: The titles and abstracts of the papers found.
    """

    try:
        arXiv_parser = ArxivParser()
        return arXiv_parser.search(query, max_results)
    except Exception as e:
        logger(e, level="error")
