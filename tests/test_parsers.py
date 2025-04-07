import pytest


def test_pdf_parser():
    from parsers.pdf_parser import PDFParser

    with open("./resources/sample.pdf", "rb") as pdf_file:
        values = pdf_file.read()
        pdf_file.close()
        contents = PDFParser().parse(values)
        assert contents is not None, "PDF parsing failed"
        assert "# Sample PDF" in contents, "PDF content does not match expected value"


def test_youtube_parser():
    from parsers.youtube_parser import YoutubeParser

    url = "https://www.youtube.com/watch?v=GPRwA9BG-m4"
    youtube_parser = YoutubeParser()
    contents = youtube_parser.parse(url)
    assert contents is not None, "YouTube parsing failed"
    assert "say the word" in contents, "YouTube content does not match expected value"


def test_web_parser():
    from parsers.crawl4ai_parser import WebBrowserCrawlerParser

    for url in [
        "https://example.com",
        "https://www.python.org",
        "https://en.wikipedia.org/wiki/Reinforcement_learning",
    ]:
        contents = WebBrowserCrawlerParser().parse(url)
        assert contents is not None, f"Web parsing failed for {url}"
        assert ("Example Domain" in contents or
                "Python" in contents or
                "reinforcement" in contents), f"Web content does not match expected value for {url}"


def test_firecrawl_parser():
    from parsers.firecrawl_parser import FirecrawlParser

    url = "https://www.example.com"
    contents = FirecrawlParser().parse(url)
    assert contents is not None, "Firecrawl parsing failed"
    assert "Example Domain" in contents, "Firecrawl content does not match expected value"

