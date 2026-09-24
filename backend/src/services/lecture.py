from datetime import datetime, timezone

from src.ai.flashcards import generate_flashcards
from src.ai.quiz import generate_quiz
from src.ai.summarizer import summarize_text
from src.rag.embeddings import generate_embedding
from src.rag.vector_store import add_chunk
from src.repositories.course import CourseRepository
from src.repositories.lecture import LectureRepository
from src.schemas.lecture import LectureCreate
from src.utils.pdf import extract_text_from_pdf
from src.utils.text import chunk_text


class LectureService:

    def __init__(self):
        self.repository = LectureRepository()
        self.course_repository = CourseRepository()

    async def create_lecture(
        self,
        lecture: LectureCreate,
        course_id: str,
        user_id: str,
        file_name: str,
        file_path: str,
    ):
        # Verify that the course belongs to the current user
        course = await self.course_repository.course_belongs_to_user(
            course_id=course_id,
            user_id=user_id,
        )

        if course is None:
            return None

        now = datetime.now(timezone.utc)

        extracted_text = extract_text_from_pdf(
            file_path
        )

        lecture_data = {
            "course_id": course_id,
            "user_id": user_id,
            "title": lecture.title,
            "file_name": file_name,
            "file_path": file_path,
            "extracted_text": extracted_text,
            "summary": None,
            "created_at": now,
            "updated_at": now,
        }

        created_lecture = await self.repository.create_lecture(
            lecture_data
        )

        lecture_id = str(
            created_lecture["_id"]
        )

        # Split lecture text into chunks and store
        # their embeddings in ChromaDB
        chunks = chunk_text(
            extracted_text,
            chunk_size=1000,
        )

        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            add_chunk(
                chunk_id=f"{lecture_id}-{index}",
                text=chunk,
                embedding=embedding,
                metadata={
                    "lecture_id": lecture_id,
                    "course_id": course_id,
                    "user_id": user_id,
                    "chunk_index": index,
                },
            )

        created_lecture["id"] = lecture_id
        del created_lecture["_id"]

        return created_lecture

    async def get_lectures(
        self,
        course_id: str,
        user_id: str,
    ):
        # The repository only returns lectures belonging
        # to both this course and this user.
        lectures = await self.repository.get_lectures_by_course(
            course_id=course_id,
            user_id=user_id,
        )

        for lecture in lectures:
            lecture["id"] = str(
                lecture["_id"]
            )
            del lecture["_id"]

        return lectures

    async def get_lecture(
        self,
        lecture_id: str,
        user_id: str,
    ):
        lecture = await self.repository.get_lecture_by_id(
            lecture_id=lecture_id,
            user_id=user_id,
        )

        if lecture is None:
            return None

        lecture["id"] = str(
            lecture["_id"]
        )
        del lecture["_id"]

        return lecture

    async def delete_lecture(
        self,
        lecture_id: str,
        user_id: str,
    ):
        deleted = await self.repository.delete_lecture(
            lecture_id=lecture_id,
            user_id=user_id,
        )

        return deleted is not None

    async def summarize_lecture(
        self,
        lecture_id: str,
        user_id: str,
    ):
        lecture = await self.repository.get_lecture_by_id(
            lecture_id=lecture_id,
            user_id=user_id,
        )

        if lecture is None:
            return None

        extracted_text = lecture.get(
            "extracted_text"
        )

        if not extracted_text:
            raise ValueError(
                "Lecture does not contain extracted text"
            )

        summary = await summarize_text(
            extracted_text
        )

        updated_lecture = await self.repository.update_lecture(
            lecture_id=lecture_id,
            user_id=user_id,
            update_data={
                "summary": summary,
                "updated_at": datetime.now(timezone.utc),
            },
        )

        if updated_lecture is None:
            return None

        updated_lecture["id"] = str(
            updated_lecture["_id"]
        )

        del updated_lecture["_id"]

        return updated_lecture

    async def generate_quiz(
        self,
        lecture_id: str,
        user_id: str,
    ):
        lecture = await self.repository.get_lecture_by_id(
            lecture_id=lecture_id,
            user_id=user_id,
        )

        if lecture is None:
            return None

        text = lecture.get("summary")

        if not text:
            raise ValueError(
                "Lecture must be summarized before generating a quiz"
            )

        return await generate_quiz(text)

    async def generate_flashcards(
        self,
        lecture_id: str,
        user_id: str,
    ):
        lecture = await self.repository.get_lecture_by_id(
            lecture_id=lecture_id,
            user_id=user_id,
        )

        if lecture is None:
            return None

        text = lecture.get("summary")

        if not text:
            raise ValueError(
                "Lecture must be summarized before generating flashcards"
            )

        return await generate_flashcards(text)