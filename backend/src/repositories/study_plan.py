from bson import ObjectId

from src.database.collections import get_study_plans_collection


class StudyPlanRepository:

    async def create_plan(self, plan_data: dict):
        collection = get_study_plans_collection()

        result = await collection.insert_one(plan_data)

        return await collection.find_one(
            {"_id": result.inserted_id}
        )

    async def get_plan_by_id(
        self,
        plan_id: str,
        user_id: str,
    ):
        collection = get_study_plans_collection()

        return await collection.find_one(
            {
                "_id": ObjectId(plan_id),
                "user_id": user_id,
            }
        )

    async def get_plans_by_course(
        self,
        course_id: str,
        user_id: str,
    ):
        collection = get_study_plans_collection()

        cursor = collection.find(
            {
                "course_id": course_id,
                "user_id": user_id,
            }
        )

        return await cursor.to_list(length=None)