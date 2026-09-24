from pydantic import BaseModel, Field

from src.ai.langchain_llm import llm


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(
        min_length=4,
        max_length=4,
    )
    answer: str
    explanation: str


class Quiz(BaseModel):
    questions: list[QuizQuestion]


quiz_llm = llm.with_structured_output(Quiz)


async def generate_quiz(text: str):

    prompt = f"""
You are an expert college-level quiz creator.

Create exactly 5 multiple-choice questions based ONLY
on the lecture material below.

Each question must have:
- exactly 4 options
- one correct answer
- a short explanation

Lecture material:

{text}
"""

    result = await quiz_llm.ainvoke(prompt)

    return result.model_dump()