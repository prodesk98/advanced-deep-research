import asyncio

import torch
from tenacity import wait_random_exponential, retry, stop_after_attempt
from transformers import AutoModel, AutoModelForSequenceClassification

from .env import RERANKER_MODEL, EMBEDDING_MODEL
from loguru import logger


class Embedding:
    def __init__(self) -> None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Loading embedding model on {device}...")

        self.device = device
        self._model = AutoModel.from_pretrained(
            EMBEDDING_MODEL,
            trust_remote_code=True,
        ).to(device)
        self._model.eval()

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts or not all(isinstance(t, str) and t.strip() for t in texts):
            raise ValueError("Input texts must be a non-empty list of non-empty strings.")

        logger.info(f"Generating embeddings for {len(texts)} texts.")
        return [
            self._model.encode(text, task="text-matching", max_length=2048)
            for text in texts
        ]


class Reranker:
    def __init__(self) -> None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Loading reranker model on {device}...")

        self.device = device
        self._model = AutoModelForSequenceClassification.from_pretrained(
            RERANKER_MODEL,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True,
        ).to(device)
        self._model.eval()

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def rerank(self, query: str, documents: list[str]) -> tuple[list[str], list[float]]:
        if not query or not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")
        if not documents:
            logger.warning("Received empty documents list for reranking.")
            return [], []

        logger.info(f"Reranking {len(documents)} documents for query: {query}")

        sentence_pairs = [[query, doc] for doc in documents]
        scores = self._model.compute_score(sentence_pairs, max_length=1024)

        reranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        reranked_documents, rerank_scores = zip(*reranked)

        return list(reranked_documents), list(rerank_scores)


_embedding = Embedding()
_reranker = Reranker()


async def embed_texts(texts: list[str]) -> list[list[float]]:
    return await asyncio.to_thread(_embedding.embed, texts)


async def rerank_documents(query: str, documents: list[str]) -> tuple[list[str], list[float]]:
    return await asyncio.to_thread(_reranker.rerank, query, documents)
