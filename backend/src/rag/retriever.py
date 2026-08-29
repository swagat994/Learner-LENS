from src.rag.embeddings import generate_embedding
from src.rag.vector_store import search_chunks


def retrieve_relevant_chunks(
    question: str,
    user_id: str,
    course_id: str,
    n_results: int = 5,
):
    question_embedding = generate_embedding(
        question
    )

    results = search_chunks(
        embedding=question_embedding,
        user_id=user_id,
        course_id=course_id,
        n_results=n_results,
    )

    chunks = []

    documents = results.get(
        "documents",
        [[]],
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        chunks.append(
            {
                "text": document,
                "metadata": metadata,
            }
        )

    return chunks