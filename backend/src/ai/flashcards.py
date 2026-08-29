import json

from src.ai.ollama_client import generate_response


async def generate_flashcards(text: str):
    prompt = f"""
You are an expert academic study assistant.

Create 10 useful flashcards based ONLY on the lecture
material below.

Each flashcard must contain:
- question
- answer

Focus on:
- important concepts
- definitions
- key facts
- technical terminology
- concepts useful for exams

Return ONLY valid JSON.

Use exactly this format:

{{
    "flashcards": [
        {{
            "question": "What is ...?",
            "answer": "..."
        }}
    ]
}}

Lecture material:

{text}
"""

    response = await generate_response(prompt)

    return json.loads(response)