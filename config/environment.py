from os import environ
from typing import Optional

from dotenv import load_dotenv
from pydantic import MongoDsn

load_dotenv()

PROJECT_NAME = environ.get("PROJECT_NAME", "Resumidor")
LANGUAGE = environ.get("LANGUAGE", "pt")

OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Set the OpenAI model to be used
OPENAI_MODEL = environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Set the OpenAI embedding model to be used
OPENAI_EMBEDDING_MODEL = environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Set the OpenAI temperature for randomness in responses
OPENAI_TEMPERATURE = float(environ.get("OPENAI_TEMPERATURE", 0.2))

# Set the OpenAI max tokens for response length
OPENAI_MAX_TOKENS = int(environ.get("OPENAI_MAX_TOKENS", 1000))

# MongoDB configuration
MONGODB_URI: Optional[MongoDsn] = environ.get("MONGODB_URI")
MONGODB_DATABASE: Optional[str] = environ.get("MONGODB_DATABASE", "summarizer")
if MONGODB_URI is None:
    raise ValueError("MONGODB_URI not found in environment variables.")
#

# Qdrant configuration
QDRANT_DSN: Optional[str] = environ.get("QDRANT_DSN", "http://localhost:6333")
QDRANT_COLLECTION: Optional[str] = environ.get("QDRANT_COLLECTION", "summarizer")
if QDRANT_DSN is None:
    raise ValueError("QDRANT_DSN not found in environment variables.")
#
