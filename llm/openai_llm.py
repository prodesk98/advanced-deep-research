from openai import OpenAI, Stream
from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE,
)
from prompts import SUMMARIZER_PROMPT
from .base import BaseLLM

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


class OpenAILLM(BaseLLM):
    """
    OpenAI LLM wrapper for the OpenAI API.
    """

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate(self, prompt: str) -> Stream:
        return self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "developer", "content": SUMMARIZER_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=OPENAI_MAX_TOKENS,
            temperature=OPENAI_TEMPERATURE,
            stream=True,
        )

client = OpenAI(api_key=OPENAI_API_KEY)
