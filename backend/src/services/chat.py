from src.ai.langgraph_chat import answer_with_graph
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

        answer = await answer_with_graph(
            question=question,
            user_id=user_id,
            course_id=course_id,
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