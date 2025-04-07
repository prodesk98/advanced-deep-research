from loggings import logger
from typing import Optional


class SearchEngineError(Exception):
    """Custom exception for search engine errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class YoutubeSearchError(Exception):
    """Custom exception for YouTube search errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        logger(self.message, level="error")


class SemanticSearchError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SemanticUpsertError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ArxivSearchError(Exception):
    """Custom exception for arXiv search errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        logger(self.message, level="error")


class ArxivDownloadError(Exception):
    """Custom exception for arXiv download errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        logger(self.message, level="error")


class CrawlerParserError(Exception):
    """Custom exception for site parser errors."""
    def __init__(self, url: str, content: str):
        self.message = f"Web parser error for url {url}: {content}"
        self.url = url
        self.content = content
        super().__init__(self.message)
        logger(self.message, level="error")


class YoutubeParserError(Exception):
    """Custom exception for YouTube parser errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        logger(message, level="error")


class PDFParserError(Exception):
    """Custom exception for PDF parser errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class LLMException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EmbedError(LLMException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidEmbedError(LLMException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidEmbedValue(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class RerankError(LLMException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidRerankValue(ValueError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class GenerativeError(LLMException):
    def __init__(self, message: str):
        super().__init__(message)


class SummarizationError(Exception):
    """Custom exception for summarization errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        logger(self.message, level="error")


class APIRequestError(Exception):
    """Custom exception for API request failures."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)

class ToolsError(Exception):
    """Custom exception for tools errors."""
    def __init__(self, message: str):
        super().__init__(message)

class BraveSearchError(Exception):
    """Custom exception for Brave Search errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

