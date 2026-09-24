from langchain_ollama import ChatOllama

from src.config.settings import settings


llm = ChatOllama(
    model=settings.llm.model_name,
)