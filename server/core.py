import asyncio
from typing import Optional, Literal

import torch
from transformers import AutoModel, AutoModelForSequenceClassification, pipeline, AutoTokenizer

from .env import RERANKER_MODEL, EMBEDDING_MODEL, SUMMARIZATION_MODEL
from loggings import logger


class Instance:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_singleton()
        return cls._instance

    def _init_singleton(self):
        self.services = {
            "embeddings": Embeddings(),
            "reranker": Reranker(),
            "summarization": Summarization(),
        }

    def get(self, name: Literal["embeddings", "reranker", "summarization"]):
        return self.services.get(name)


class Embeddings:
    def __init__(self, model_name: Optional[str] = None) -> None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._model_name = model_name or EMBEDDING_MODEL
        logger(f"Loading embedding model on {device}...", "info")

        self.device = device
        self._model = AutoModel.from_pretrained(
            self._model_name,
            trust_remote_code=True,
        ).to(device)
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts or not all(isinstance(t, str) and t.strip() for t in texts):
            raise ValueError("Input texts must be a non-empty list of non-empty strings.")

        logger(f"Generating embeddings for {len(texts)} texts.", "info")
        return [
            self._model.encode(text, task="text-matching", max_length=2048)
            for text in texts
        ]


class Reranker:
    def __init__(self, model_name: Optional[str] = None) -> None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._model_name = model_name or RERANKER_MODEL
        logger(f"Loading reranker model on {device}...", "info")

        self.device = device
        self._model = AutoModelForSequenceClassification.from_pretrained(
            self._model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True,
        ).to(device)

    def rerank(self, query: str, documents: list[str]) -> tuple[list[str], list[float]]:
        if not query or not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")
        if not documents:
            logger("Received empty documents list for reranking.", "warning")
            return [], []

        if len(documents) < 2:
            logger("No documents provided for reranking.", "warning")
            return [], []

        logger(f"Reranking {len(documents)} documents for query: {query}", "info")

        sentence_pairs = [[query, doc] for doc in documents]
        scores: list[float] = self._model.compute_score(sentence_pairs, max_length=1024)

        if len(documents) == 1:
            return [documents[0]], [scores[0]]

        reranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        reranked_documents, rerank_scores = zip(*reranked)

        return list(reranked_documents), list(rerank_scores)


class Summarization:
    def __init__(self, model_name: Optional[str] = None) -> None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._model_name = model_name or SUMMARIZATION_MODEL
        self._model = pipeline(
            "summarization",
            model=self._model_name,
            device=device,
            trust_remote_code=True
        )
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)

    def summarize(self, query: str, text: str) -> str:
        if not text or not isinstance(text, str) or not text.strip():
            raise ValueError("Input text must be a non-empty string.")
        if not query or not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        full_text = f"**Query: {query}\n\n**{text}"
        logger(f"Summarizing text of length {len(full_text)}.", "info")

        max_input_length = 1024
        tokenized_input = self._tokenizer(
            full_text,
            truncation=True,
            max_length=max_input_length,
            return_tensors="pt"
        )
        truncated_text = self._tokenizer.decode(
            tokenized_input["input_ids"][0],
            skip_special_tokens=True
        )

        summaries: list[dict] = self._model(truncated_text, max_length=150, min_length=30, do_sample=False)
        return summaries[0]['summary_text']


# Singleton instance of the Instance class
instance = Instance()
#


async def embed_texts(texts: list[str]) -> list[list[float]]:
    return await asyncio.to_thread(instance.get("embeddings").embed, texts)


async def rerank_documents(query: str, documents: list[str]) -> tuple[list[str], list[float]]:
    return await asyncio.to_thread(instance.get("reranker").rerank, query, documents)


async def summarization_text(query: str, text: str) -> str:
    return await asyncio.to_thread(instance.get("summarization").summarize, query, text)
