from pymongo import AsyncMongoClient

from src.config.settings import settings

client: AsyncMongoClient | None = None


def connect_to_mongo() -> AsyncMongoClient:
    global client

    if client is None:
        client = AsyncMongoClient(settings.database.mongodb_uri)

    return client


def get_database():
    return connect_to_mongo()[settings.database.database_name]


async def close_mongo_connection():
    global client

    if client is not None:
        client.close()
        client = None