from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.schemas.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
)
from src.services.chat import ChatService


router = APIRouter(
    prefix="/courses/{course_id}/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    course_id: str,
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
    answer = await chat_service.ask_question(
        question=request.message,
        user_id=current_user["id"],
        course_id=course_id,
    )

    return {
        "question": request.message,
        "answer": answer,
    }


@router.get(
    "",
    response_model=list[ChatMessage],
)
async def get_chat_history(
    course_id: str,
    current_user=Depends(get_current_user),
):
    return await chat_service.get_chat_history(
        user_id=current_user["id"],
        course_id=course_id,
    )