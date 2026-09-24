from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from src.ai.langchain_llm import llm
from src.rag.langchain_retriever import get_retriever


class ChatState(TypedDict):
    question: str
    user_id: str
    course_id: str
    context: str
    answer: str


async def retrieve_node(state: ChatState):

    retriever = get_retriever(
        user_id=state["user_id"],
        course_id=state["course_id"],
        n_results=5,
    )

    documents = await retriever.ainvoke(
        state["question"]
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return {
        "context": context
    }


async def generate_node(state: ChatState):

    if not state["context"]:
        return {
            "answer": (
                "I couldn't find relevant information "
                "in your lectures."
            )
        }

    prompt = f"""
You are LectureLens, an academic assistant.

Answer the student's question using ONLY the
provided lecture context.

Rules:
- Do not invent information.
- If the answer is not present in the context,
  say that the lecture material does not contain
  enough information to answer.
- Explain the answer clearly.
- Use examples from the lecture when useful.

Lecture context:

{state["context"]}

Student question:

{state["question"]}
"""

    response = await llm.ainvoke(prompt)

    return {
        "answer": response.content
    }


graph_builder = StateGraph(ChatState)

graph_builder.add_node(
    "retrieve",
    retrieve_node,
)

graph_builder.add_node(
    "generate",
    generate_node,
)

graph_builder.add_edge(
    START,
    "retrieve",
)

graph_builder.add_edge(
    "retrieve",
    "generate",
)

graph_builder.add_edge(
    "generate",
    END,
)

chat_graph = graph_builder.compile()


async def answer_with_graph(
    question: str,
    user_id: str,
    course_id: str,
) -> str:

    result = await chat_graph.ainvoke(
        {
            "question": question,
            "user_id": user_id,
            "course_id": course_id,
            "context": "",
            "answer": "",
        }
    )

    return result["answer"]