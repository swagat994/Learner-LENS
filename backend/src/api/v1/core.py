from fastapi import APIRouter

from src.config.settings import settings

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app.app_name}!",
        "version": settings.app.api_version,
        "environment": settings.app.environment,
    }