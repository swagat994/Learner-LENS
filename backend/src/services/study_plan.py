from datetime import datetime, timezone

from src.ai.study_plan import generate_study_plan
from src.repositories.study_plan import StudyPlanRepository


class StudyPlanService:

    def __init__(self):
        self.repository = StudyPlanRepository()

    async def create_plan(
        self,
        course_id: str,
        user_id: str,
        duration_days: int,
        lecture_text: str,
    ):
        plan = await generate_study_plan(
            text=lecture_text,
            duration_days=duration_days,
        )

        now = datetime.now(timezone.utc)

        plan_data = {
            "course_id": course_id,
            "user_id": user_id,
            "duration_days": duration_days,
            "plan": plan["plan"],
            "created_at": now,
            "updated_at": now,
        }

        created_plan = await self.repository.create_plan(
            plan_data
        )

        created_plan["id"] = str(
            created_plan["_id"]
        )

        del created_plan["_id"]

        return created_plan