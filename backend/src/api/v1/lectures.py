import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from src.auth.dependencies import get_current_user
from src.schemas.lecture import (
    LectureCreate,
    LectureResponse,
)
from src.services.lecture import LectureService


router = APIRouter(
    prefix="/courses/{course_id}/lectures",
    tags=["Lectures"],
)

lecture_service = LectureService()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


@router.post(
    "",
    response_model=LectureResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_lecture(
    course_id: str,
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    # Only PDF files are accepted
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    # Generate a unique filename
    extension = os.path.splitext(
        file.filename
    )[1]

    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename,
    )

    # Save uploaded PDF
    with open(
        file_path,
        "wb",
    ) as buffer:
        buffer.write(
            await file.read()
        )

    lecture = LectureCreate(
        title=title,
    )

    created_lecture = await lecture_service.create_lecture(
        lecture=lecture,
        course_id=course_id,
        user_id=current_user["id"],
        file_name=file.filename,
        file_path=file_path,
    )

    # Course does not belong to the authenticated user
    if created_lecture is None:
        # Remove the uploaded file because the lecture
        # was not created.
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return created_lecture


@router.post(
    "/{lecture_id}/summarize",
    response_model=LectureResponse,
)
async def summarize_lecture(
    lecture_id: str,
    current_user=Depends(get_current_user),
):
    lecture = await lecture_service.summarize_lecture(
        lecture_id=lecture_id,
        user_id=current_user["id"],
    )

    if lecture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found",
        )

    return lecture


@router.get(
    "",
    response_model=list[LectureResponse],
)
async def get_lectures(
    course_id: str,
    current_user=Depends(get_current_user),
):
    return await lecture_service.get_lectures(
        course_id=course_id,
        user_id=current_user["id"],
    )


@router.get(
    "/{lecture_id}",
    response_model=LectureResponse,
)
async def get_lecture(
    course_id: str,
    lecture_id: str,
    current_user=Depends(get_current_user),
):
    lecture = await lecture_service.get_lecture(
        lecture_id=lecture_id,
        user_id=current_user["id"],
    )

    if lecture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found",
        )

    return lecture


@router.post(
    "/{lecture_id}/quiz",
)
async def generate_quiz(
    lecture_id: str,
    current_user=Depends(get_current_user),
):
    quiz = await lecture_service.generate_quiz(
        lecture_id=lecture_id,
        user_id=current_user["id"],
    )

    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found",
        )

    return quiz


@router.post(
    "/{lecture_id}/flashcards",
)
async def generate_flashcards(
    lecture_id: str,
    current_user=Depends(get_current_user),
):
    flashcards = await lecture_service.generate_flashcards(
        lecture_id=lecture_id,
        user_id=current_user["id"],
    )

    if flashcards is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecture not found",
        )

    return flashcards