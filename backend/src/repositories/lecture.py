from pymongo import ReturnDocument

from src.database.collections import get_documents_collection
from src.utils.object_id import validate_object_id


class LectureRepository:

    async def create_lecture(self, lecture_data: dict):
        collection = get_documents_collection()

        result = await collection.insert_one(lecture_data)

        return await collection.find_one(
            {"_id": result.inserted_id}
        )

    async def get_lectures_by_course(
        self,
        course_id: str,
        user_id: str,
    ):
        collection = get_documents_collection()

        cursor = collection.find(
            {
                "course_id": course_id,
                "user_id": user_id,
            }
        )

        return await cursor.to_list(length=None)

    async def get_lecture_by_id(
        self,
        lecture_id: str,
        user_id: str,
    ):
        collection = get_documents_collection()

        return await collection.find_one(
            {
                "_id": validate_object_id(lecture_id),
                "user_id": user_id,
            }
        )

    async def delete_lecture(
        self,
        lecture_id: str,
        user_id: str,
    ):
        collection = get_documents_collection()

        return await collection.find_one_and_delete(
            {
                "_id": validate_object_id(lecture_id),
                "user_id": user_id,
            }
        )


    async def update_lecture(
        self,
        lecture_id: str,
        user_id: str,
        update_data: dict,
    ):
        collection = get_documents_collection()

        return await collection.find_one_and_update(
            {
                "_id": validate_object_id(lecture_id),
                "user_id": user_id,
            },
            {
                "$set": update_data,
            },
            return_document=ReturnDocument.AFTER,
        )