from datetime import datetime, timezone

from src.repositories.course import CourseRepository
from src.schemas.course import CourseCreate


class CourseService:

    def __init__(self):
        self.repository = CourseRepository()

    async def create_course(
        self,
        course: CourseCreate,
        user_id: str,
    ):
        now = datetime.now(timezone.utc)

        course_data = {
            "title": course.title,
            "description": course.description,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now,
        }

        created_course = await self.repository.create_course(
            course_data
        )

        created_course["id"] = str(created_course["_id"])
        del created_course["_id"]

        return created_course

    async def get_courses(self, user_id: str):
        courses = await self.repository.get_courses_by_user(
            user_id
        )

        for course in courses:
            course["id"] = str(course["_id"])
            del course["_id"]

        return courses

    async def get_course(
        self,
        course_id: str,
        user_id: str,
    ):
        course = await self.repository.get_course_by_id(
            course_id=course_id,
            user_id=user_id,
        )

        if course is None:
            return None

        course["id"] = str(course["_id"])
        del course["_id"]

        return course

    async def update_course(
        self,
        course_id: str,
        user_id: str,
        course,
    ):
        update_data = course.model_dump(
        exclude_unset=True,
        )

        if not update_data:
            return await self.get_course(
                course_id,
                user_id,
            )

        update_data["updated_at"] = datetime.now(timezone.utc)

        updated_course = await self.repository.update_course(
            course_id=course_id,
            user_id=user_id,
            update_data=update_data,
        )

        if updated_course is None:
            return None

        updated_course["id"] = str(updated_course["_id"])
        del updated_course["_id"]

        return updated_course


    async def delete_course(
        self,
        course_id: str,
        user_id: str,
    ):
        deleted_course = await self.repository.delete_course(
            course_id=course_id,
            user_id=user_id,
        )

        if deleted_course is None:
            return False

        return True

    async def course_belongs_to_user(
        self,
        course_id: str,
        user_id: str,
    ):
        return await self.repository.course_belongs_to_user(
            course_id=course_id,
            user_id=user_id,
        )
