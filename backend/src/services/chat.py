from src.ai.chat import answer_question
from src.rag.retriever import retrieve_relevant_chunks
from src.repositories.chat import ChatRepository


class ChatService:

    def __init__(self):
        self.repository = ChatRepository()

    async def ask_question(
        self,
        question: str,
        user_id: str,
        course_id: str,
    ):
        chunks = retrieve_relevant_chunks(
            question=question,
            user_id=user_id,
            course_id=course_id,
            n_results=5,
        )

        if not chunks:
            answer = (
                "I couldn't find relevant information "
                "in your lectures."
            )
        else:
            context = "\n\n".join(
                chunk["text"]
                for chunk in chunks
            )

            answer = await answer_question(
                question=question,
                context=context,
            )

        await self.repository.create_message(
            user_id=user_id,
            course_id=course_id,
            question=question,
            answer=answer,
        )

        return answer

    async def get_chat_history(
        self,
        user_id: str,
        course_id: str,
    ):
        return await self.repository.get_messages(
            user_id=user_id,
            course_id=course_id,
        )