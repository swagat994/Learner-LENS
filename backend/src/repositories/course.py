from pymongo import ReturnDocument

from src.database.collections import get_courses_collection
from src.utils.object_id import validate_object_id


class CourseRepository:

    async def create_course(self, course_data: dict):
        collection = get_courses_collection()

        result = await collection.insert_one(course_data)

        return await collection.find_one(
            {"_id": result.inserted_id}
        )

    async def get_courses_by_user(self, user_id: str):
        collection = get_courses_collection()

        cursor = collection.find(
            {"user_id": user_id}
        )

        return await cursor.to_list(length=None)

    async def get_course_by_id(self, course_id: str, user_id: str):
        collection = get_courses_collection()

        return await collection.find_one(
            {
                "_id": validate_object_id(course_id),
                "user_id": user_id,
            }
        )

    async def update_course(
        self,
        course_id: str,
        user_id: str,
        update_data: dict,
    ):
        collection = get_courses_collection()

        return await collection.find_one_and_update(
            {
                "_id": validate_object_id(course_id),
                "user_id": user_id,
            },
            {
                "$set": update_data,
            },
            return_document=ReturnDocument.AFTER,
        )


    async def delete_course(
        self,
        course_id: str,
        user_id: str,
    ):
        collection = get_courses_collection()

        return await collection.find_one_and_delete(
            {
                "_id": validate_object_id(course_id),
                "user_id": user_id,
            }
        )


    async def course_belongs_to_user(
        self,
        course_id: str,
        user_id: str,
    ):
        collection = get_courses_collection()

        return await collection.find_one(
            {
                "_id": validate_object_id(course_id),
                "user_id": user_id,
            }
        )