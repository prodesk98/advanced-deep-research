from typing import Optional

from schemas import SearchResult


def parser_search_result(title: str, description: str, link: str, content: Optional[str] = None) -> SearchResult:
    """
    Parse the search result into a structured format.
    :param title:
    :param description:
    :param link:
    :param content:
    :return:
    """
    return SearchResult(
        title=title,
        snippet=description,
        link=link,
        content=content
    )
