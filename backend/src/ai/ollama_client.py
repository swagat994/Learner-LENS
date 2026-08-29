import ollama

from src.config.settings import settings


async def generate_response(prompt: str) -> str:
    client = ollama.AsyncClient()

    response = await client.chat(
        model=settings.llm.model_name,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]