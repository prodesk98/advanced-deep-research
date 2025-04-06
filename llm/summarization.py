from langchain_text_splitters import CharacterTextSplitter

from .base import BaseSummarization
from ._locally_call_api import LocallyCallAPI


class Summarization(BaseSummarization):
    def __init__(self):
        self._client = LocallyCallAPI()
        self._splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base", chunk_size=1000, chunk_overlap=100
        )

    def _split_text(self, text: str) -> list[str]:
        ...

    def summarize(self, query: str, document: str) -> str:
        pass
