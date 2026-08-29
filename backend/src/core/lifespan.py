from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.client import close_mongo_connection, connect_to_mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()

    yield

    await close_mongo_connection()