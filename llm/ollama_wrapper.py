from typing import Optional

from langchain_ollama import ChatOllama
from streamlit.delta_generator import DeltaGenerator

from config import OLLAMA_API_BASE, OPENAI_API_BASE
from schemas import ReflectionResultSchema
from .base import BaseLLM, T



class OllamaLLM(BaseLLM):
    """
    Ollama LLM wrapper.
    """
    def __init__(self, namespace: Optional[str] = None, ui: Optional[DeltaGenerator] = None):
        super().__init__(namespace, ui)
        self._chat_llm = ChatOllama(
            base_url=OLLAMA_API_BASE,
            model=OPENAI_API_BASE,
            temperature=.0,
        )

    def flashcard(self, prompt: str, quantities: int = 5) -> list[T]:
        pass

    def generate_sub_queries(self, query: str) -> list[str]:
        pass

    def reflection(self, query: str, sub_queries: list[str], chunks: list[str]) -> ReflectionResultSchema:
        pass

    def summarize(self, query: str, chunks: list[str]) -> str:
        pass

    def generate(self, prompt: str) -> str:
        # Placeholder for actual generation logic
        return f"Generated text from {self.model_name} with prompt: {prompt}"