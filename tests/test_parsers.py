import pytest


def test_pdf_parser():
    from utils.pdf_parser import PDFParser

    with open("./resources/sample.pdf", "rb") as pdf_file:
        values = pdf_file.read()
        pdf_file.close()
        pdf_parser = PDFParser(values)
        contents = pdf_parser.to_text()
        assert contents is not None, "PDF parsing failed"
        assert "# Sample PDF" in contents, "PDF content does not match expected value"


def test_youtube_parser():
    from utils.youtube_parser import YoutubeParser

    url = "https://www.youtube.com/watch?v=GPRwA9BG-m4"
    youtube_parser = YoutubeParser()
    contents = youtube_parser.fetch(url)
    assert contents is not None, "YouTube parsing failed"
    assert "say the word" in contents, "YouTube content does not match expected value"


@pytest.mark.asyncio
async def test_web_parser():
    from utils.web_parser import WebParser

    for url in [
        "https://example.com",
        "https://www.python.org",
    ]:
        web_parser = WebParser()
        contents = await web_parser.aget_markdown(url)
        assert contents is not None, f"Web parsing failed for {url}"
        assert "Example Domain" in contents or "Python" in contents, f"Web content does not match expected value for {url}"
