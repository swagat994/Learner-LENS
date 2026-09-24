from src.ai.langchain_llm import llm
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

        response = await llm.ainvoke(prompt)

        summaries.append(response.content)

    if len(summaries) == 1:
        return summaries[0]

    combined = "\n\n".join(summaries)

    final_prompt = f"""
You are an expert academic assistant.

Combine these section summaries into ONE coherent
study summary.

Requirements:
- Remove repetition.
- Preserve important concepts.
- Organize logically.
- Use headings and bullet points.
- Make it useful for exam revision.
- Do not invent information.

Section summaries:

{combined}
"""

    response = await llm.ainvoke(final_prompt)

    return response.content