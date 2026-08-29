from src.ai.ollama_client import generate_response
from src.utils.text import chunk_text


async def summarize_text(text: str) -> str:
    chunks = chunk_text(text)

    summaries = []

    for chunk in chunks:
        prompt = f"""
You are an expert academic assistant.

Summarize the following lecture material.

Requirements:
- Identify the main concepts.
- Explain important ideas clearly.
- Keep important technical terms.
- Use headings and bullet points.
- Do not invent information.

Lecture material:

{chunk}
"""

        summary = await generate_response(prompt)

        summaries.append(summary)

    if len(summaries) == 1:
        return summaries[0]

    combined = "\n\n".join(summaries)

    final_prompt = f"""
You are an expert academic assistant.

The following are summaries of different sections
of the same lecture.

Combine them into ONE coherent study summary.

Requirements:
- Remove repetition.
- Preserve important concepts.
- Organize the material logically.
- Use headings and bullet points.
- Make it useful for exam revision.
- Do not invent information.

Section summaries:

{combined}
"""

    return await generate_response(final_prompt)