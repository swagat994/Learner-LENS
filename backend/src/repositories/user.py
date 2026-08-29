from bson import ObjectId

from src.database.collections import get_users_collection
from src.models.user import User


class UserRepository:
    def __init__(self):
        self.collection = get_users_collection()

    async def create_user(self, user: User):
        result = await self.collection.insert_one(user.to_dict())

        created_user = await self.collection.find_one(
            {"_id": result.inserted_id}
        )

        return created_user

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one(
            {"email": email}
        )

    async def get_user_by_id(self, user_id: str):
        return await self.collection.find_one(
            {"_id": ObjectId(user_id)}
        )

    async def get_user_by_id(self, user_id: str):
        return await self.collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )