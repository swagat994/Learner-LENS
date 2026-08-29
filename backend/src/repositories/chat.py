from datetime import datetime, timezone

from src.database.collections import get_chats_collection


class ChatRepository:

    async def create_message(
        self,
        user_id: str,
        course_id: str,
        question: str,
        answer: str,
    ):
        collection = get_chats_collection()

        chat_data = {
            "user_id": user_id,
            "course_id": course_id,
            "question": question,
            "answer": answer,
            "created_at": datetime.now(timezone.utc),
        }

        result = await collection.insert_one(chat_data)

        chat_data["id"] = str(result.inserted_id)
        del chat_data["_id"]

        return chat_data

    async def get_messages(
        self,
        user_id: str,
        course_id: str,
    ):
        collection = get_chats_collection()

        cursor = collection.find(
            {
                "user_id": user_id,
                "course_id": course_id,
            }
        ).sort(
            "created_at",
            1,
        )

        messages = await cursor.to_list(
            length=None
        )

        for message in messages:
            message["id"] = str(
                message["_id"]
            )
            del message["_id"]

        return messages