from datetime import datetime

from pydantic import BaseModel, Field


class LectureCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )


class LectureResponse(BaseModel):
    id: str
    course_id: str
    user_id: str
    title: str
    file_name: str
    file_path: str
    extracted_text: str | None = None
    summary: str | None = None
    created_at: datetime
    updated_at: datetime


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str


class QuizResponse(BaseModel):
    lecture_id: str
    questions: list[QuizQuestion]


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardResponse(BaseModel):
    lecture_id: str
    flashcards: list[Flashcard]