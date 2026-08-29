from .base import BaseConfig


class LLMSettings(BaseConfig):

    model_name: str = "llama3.2:3b"

    temperature: float = 0.2

    max_tokens: int = 2048