from src.ai.ollama_client import generate_response


async def answer_question(
    question: str,
    context: str,
) -> str:

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

{context}

Student question:

{question}
"""

    return await generate_response(prompt)