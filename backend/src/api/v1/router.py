from fastapi import APIRouter

from .auth import router as auth_router
from .core import router as core_router
from .health import router as health_router
from .users import router as users_router
from .courses import router as courses_router
from .lectures import router as lectures_router
from .study_plans import router as study_plans_router
from .chat import router as chat_router

router = APIRouter()

router.include_router(core_router)
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(courses_router)
router.include_router(lectures_router)
router.include_router(study_plans_router)
router.include_router(chat_router)