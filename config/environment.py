from os import environ
from typing import Optional, Literal

from dotenv import load_dotenv
from pydantic import MongoDsn

load_dotenv()

PROJECT_NAME = environ.get("PROJECT_NAME", "ResumidorLLM")
LANGUAGE = environ.get("LANGUAGE", "en") # language code
NATURAL_LANGUAGE = environ.get("NATURAL_LANGUAGE", "English") # natural language

OPENAI_API_KEY = environ.get("OPENAI_API_KEY", "default")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Backend configuration
LOCALLY_API_BASE = environ.get("LOCALLY_API_BASE", "http://localhost:8502")
LOCALLY_API_KEY = environ.get("LOCALLY_API_KEY", "default")
##

# Set the OpenAI API base URL
OPENAI_API_BASE = environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

# Set the OpenAI model to be used
OPENAI_MODEL = environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Set the OpenAI embedding model to be used
OPENAI_EMBEDDING_MODEL = environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Set the OpenAI temperature for randomness in responses
OPENAI_TEMPERATURE = float(environ.get("OPENAI_TEMPERATURE", .0))

# Set the OpenAI max tokens for response length
OPENAI_MAX_TOKENS = int(environ.get("OPENAI_MAX_TOKENS", 1000))

LLM_ENGINE: Literal['openai', 'ollama'] = environ.get("LLM_ENGINE", 'openai') # openai or ollama

if LLM_ENGINE not in ["openai", "ollama"]:
    raise ValueError("LLM_ENGINE must be 'openai' or 'ollama'.")

## Ollama configuration
OLLAMA_API_BASE = environ.get("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = environ.get("OLLAMA_MODEL", "llama3.2") # Set the Ollama model to be used
OLLAMA_MAX_TOKENS = int(environ.get("OPENAI_MAX_TOKENS", 1000))
# Set the Ollama model to be used

# MongoDB configuration
MONGODB_URI: Optional[MongoDsn] = environ.get("MONGODB_URI")
MONGODB_DATABASE: Optional[str] = environ.get("MONGODB_DATABASE", PROJECT_NAME)
if MONGODB_URI is None:
    raise ValueError("MONGODB_URI not found in environment variables.")
#

# Qdrant configuration
QDRANT_DSN: Optional[str] = environ.get("QDRANT_DSN", "http://localhost:6333")
QDRANT_COLLECTION: Optional[str] = environ.get("QDRANT_COLLECTION", PROJECT_NAME)
if QDRANT_DSN is None:
    raise ValueError("QDRANT_DSN not found in environment variables.")
#

USE_RERANKER = bool(environ.get("USE_RERANKER", "true") == "true")
USE_CHAT_MEMORY = bool(environ.get("USE_CHAT_MEMORY", "true") == "true")
USE_ARXIV = bool(environ.get("USE_ARXIV", "true") == "true")

SEARCH_ENGINE: Literal["local", "serpapi", "brave", "tavily"] = environ.get("SEARCH_ENGINE", "local") # local, serpapi, tavily or brave
if SEARCH_ENGINE not in ["local", "serpapi", "brave", "tavily"]:
    raise ValueError("SEARCH_ENGINE must be 'local', 'serpapi', 'tavily' or 'brave'.")

SERPAPI_API_KEY: Optional[str] = environ.get("SERPAPI_API_KEY")
BRAVE_API_KEY: Optional[str] = environ.get("BRAVE_API_KEY")
TAVILY_API_KEY: Optional[str] = environ.get("TAVILY_API_KEY")

if SEARCH_ENGINE == "serpapi" and SERPAPI_API_KEY is None:
    raise ValueError("SERPAPI_API_KEY not found in environment variables.")

if SEARCH_ENGINE == "brave" and BRAVE_API_KEY is None:
    raise ValueError("BRAVE_API_KEY not found in environment variables.")

if SEARCH_ENGINE == "tavily" and TAVILY_API_KEY is None:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

CRAWLER_ENGINE: Literal["local", "firecrawl"] = environ.get("CRAWLER_ENGINE", "local") # local, firecrawl

if CRAWLER_ENGINE not in ["local", "firecrawl"]:
    raise ValueError("CRAWLER_ENGINE must be 'local' or 'firecrawl'.")

FIRECRAWL_API_KEY: Optional[str] = environ.get("FIRECRAWL_API_KEY")
if CRAWLER_ENGINE == "firecrawl" and FIRECRAWL_API_KEY is None:
    raise ValueError("FIRECRAWL_API_KEY not found in environment variables.")

