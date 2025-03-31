from os import environ

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Set the OpenAI model to be used
OPENAI_MODEL = environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Set the OpenAI temperature for randomness in responses
OPENAI_TEMPERATURE = float(environ.get("OPENAI_TEMPERATURE", 0.2))

# Set the OpenAI max tokens for response length
OPENAI_MAX_TOKENS = int(environ.get("OPENAI_MAX_TOKENS", 1000))
