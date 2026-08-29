from datetime import datetime

from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )


class CourseResponse(BaseModel):
    id: str
    title: str
    description: str | None = None
    user_id: str
    created_at: datetime
    updated_at: datetime


class CourseUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )