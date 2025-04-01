import os
from typing import Optional

import pymupdf4llm
import tempfile


class PDFParser:
    def __init__(self, values: bytes):
        self._path: str = self._temporary_file(values)

    @staticmethod
    def _temporary_file(values: bytes) -> str:
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as f:
            f.write(values)
            f.seek(0)
            return f.name

    def to_text(self) -> Optional[str]:
        try:
            content = pymupdf4llm.to_markdown(self._path)
            return content
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to text: {e}")
        finally:
            os.remove(self._path)  # Remove the temporary file after reading

    @property
    def path(self) -> os.PathLike | str:
        return self._path
