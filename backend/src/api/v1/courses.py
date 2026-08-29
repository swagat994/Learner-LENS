from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import get_current_user
from src.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
)
from src.services.course import CourseService


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)

course_service = CourseService()


@router.post(
    "",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    course: CourseCreate,
    current_user=Depends(get_current_user),
):
    return await course_service.create_course(
        course=course,
        user_id=current_user["id"],
    )


@router.get(
    "",
    response_model=list[CourseResponse],
)
async def get_courses(
    current_user=Depends(get_current_user),
):
    return await course_service.get_courses(
        user_id=current_user["id"],
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
async def get_course(
    course_id: str,
    current_user=Depends(get_current_user),
):
    course = await course_service.get_course(
        course_id=course_id,
        user_id=current_user["id"],
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course

@router.put(
    "/{course_id}",
    response_model=CourseResponse,
)
async def update_course(
    course_id: str,
    course: CourseUpdate,
    current_user=Depends(get_current_user),
):
    updated_course = await course_service.update_course(
        course_id=course_id,
        user_id=current_user["id"],
        course=course,
    )

    if updated_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return updated_course


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course(
    course_id: str,
    current_user=Depends(get_current_user),
):
    deleted = await course_service.delete_course(
        course_id=course_id,
        user_id=current_user["id"],
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return None

