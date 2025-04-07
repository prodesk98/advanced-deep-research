from dotenv import load_dotenv
from os import environ

load_dotenv()

RERANKER_MODEL = environ.get("RERANKER_MODEL", "jinaai/jina-reranker-v2-base-multilingual")
EMBEDDING_MODEL = environ.get("EMBEDDING_MODEL", "jinaai/jina-embeddings-v3")
SUMMARIZATION_MODEL = environ.get("SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
