from fastapi import APIRouter, status

from src.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from src.services.user import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

user_service = UserService()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(user: UserCreate):
    return await user_service.create_user(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(credentials: UserLogin):
    return await user_service.login_user(credentials)