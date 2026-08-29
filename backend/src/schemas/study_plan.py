from datetime import datetime

from pydantic import BaseModel, Field


class StudyPlanCreate(BaseModel):
    duration_days: int = Field(
        ...,
        ge=1,
        le=30,
    )


class StudyDay(BaseModel):
    day: int
    topics: list[str]
    tasks: list[str]


class StudyPlanResponse(BaseModel):
    id: str
    course_id: str
    user_id: str
    duration_days: int
    plan: list[StudyDay]
    created_at: datetime
    updated_at: datetime