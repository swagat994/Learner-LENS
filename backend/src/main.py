from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.router import router as api_router
from src.config.settings import settings
from src.core.lifespan import lifespan
from src.exceptions.handlers import register_exception_handlers


app = FastAPI(
    title=settings.app.app_name,
    version=settings.app.api_version,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allowed_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)


register_exception_handlers(app)


app.include_router(
    api_router,
    prefix="/api/v1",
)