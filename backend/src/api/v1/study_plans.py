from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import get_current_user
from src.schemas.study_plan import (
    StudyPlanCreate,
    StudyPlanResponse,
)
from src.services.study_plan import StudyPlanService
from src.services.course import CourseService
from src.services.lecture import LectureService


router = APIRouter(
    prefix="/courses/{course_id}/study-plans",
    tags=["Study Plans"],
)

study_plan_service = StudyPlanService()
course_service = CourseService()
lecture_service = LectureService()


@router.post(
    "",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_study_plan(
    course_id: str,
    request: StudyPlanCreate,
    current_user=Depends(get_current_user),
):
    user_id = current_user["id"]

    course = await course_service.course_belongs_to_user(
        course_id=course_id,
        user_id=user_id,
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    lectures = await lecture_service.get_lectures(
        course_id=course_id,
        user_id=user_id,
    )

    if not lectures:
        raise HTTPException(
            status_code=400,
            detail="Course has no lectures",
        )

    lecture_text = "\n\n".join(
        lecture.get("extracted_text", "")
        for lecture in lectures
    )

    if not lecture_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Lectures do not contain extracted text",
        )

    return await study_plan_service.create_plan(
        course_id=course_id,
        user_id=user_id,
        duration_days=request.duration_days,
        lecture_text=lecture_text,
    )