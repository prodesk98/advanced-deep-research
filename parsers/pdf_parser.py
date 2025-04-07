import os
from typing import Optional
from exceptions import PDFParserError

import pymupdf4llm
import tempfile

from .base import BaseParser


class PDFParser(BaseParser):
    @staticmethod
    def _temporary_file(values: bytes) -> str:
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as f:
            f.write(values)
            return f.name

    def parse(self, values: bytes) -> Optional[str]:
        """
        Parse the PDF content and convert it to text.
        Using pymupdf4llm to convert PDF to text.
        :param values:
        :return:
        """
        try:
            path = self._temporary_file(values)
        except Exception:
            raise PDFParserError("Failed to create temporary file for PDF parsing")
        try:
            content = pymupdf4llm.to_markdown(path)
            return content
        except Exception as e:
            raise PDFParserError(f"Failed to convert PDF to text: {e}")
        finally:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
