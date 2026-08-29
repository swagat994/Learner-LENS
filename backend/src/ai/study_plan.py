import json

from src.ai.ollama_client import generate_response


async def generate_study_plan(
    text: str,
    duration_days: int,
):
    prompt = f"""
You are an expert academic study planner.

Create a {duration_days}-day study plan based ONLY
on the lecture material below.

For each day provide:
- day number
- topics to study
- specific study tasks

Make the plan realistic for a college student.

Return ONLY valid JSON.

Use exactly this format:

{{
    "plan": [
        {{
            "day": 1,
            "topics": [
                "Topic 1",
                "Topic 2"
            ],
            "tasks": [
                "Task 1",
                "Task 2"
            ]
        }}
    ]
}}

Lecture material:

{text}
"""

    response = await generate_response(prompt)

    return json.loads(response)