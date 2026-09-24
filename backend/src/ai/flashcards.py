from pydantic import BaseModel

from src.ai.langchain_llm import llm


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardSet(BaseModel):
    flashcards: list[Flashcard]


flashcard_llm = llm.with_structured_output(
    FlashcardSet
)


async def generate_flashcards(text: str):

    prompt = f"""
You are an expert academic study assistant.

Create exactly 10 useful flashcards based ONLY
on the lecture material.

Focus on:
- important concepts
- definitions
- key facts
- technical terminology
- exam-relevant concepts

Lecture material:

{text}
"""

    result = await flashcard_llm.ainvoke(prompt)

    return result.model_dump()