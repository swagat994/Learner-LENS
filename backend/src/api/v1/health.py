from fastapi import APIRouter

from src.database.collections import get_users_collection

router = APIRouter()


@router.get("/health", summary="Health Check")
async def health():
    users_collection = get_users_collection()

    await users_collection.count_documents({})

    return {
        "status": "healthy",
        "database": "connected",
    }