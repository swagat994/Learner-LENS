from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    question: str
    answer: str


class ChatMessage(BaseModel):
    id: str
    user_id: str
    course_id: str
    question: str
    answer: str
    created_at: datetime