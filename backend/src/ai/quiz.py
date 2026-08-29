import json

from src.ai.ollama_client import generate_response


async def generate_quiz(text: str):
    prompt = f"""
You are an expert college-level quiz creator.

Create 5 multiple-choice questions based ONLY on the
lecture material below.

For every question provide:
- question
- exactly 4 options
- correct answer
- short explanation

Return ONLY valid JSON.

Use exactly this format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option A",
            "explanation": "Why this is correct"
        }}
    ]
}}

Lecture material:

{text}
"""

    response = await generate_response(prompt)

    return json.loads(response)