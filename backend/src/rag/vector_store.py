import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="lecture_chunks"
)


def add_chunk(
    chunk_id: str,
    text: str,
    embedding: list[float],
    metadata: dict,
):
    collection.upsert(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
    )


def search_chunks(
    embedding: list[float],
    user_id: str,
    course_id: str,
    n_results: int = 5,
):
    return collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={
            "$and": [
                {"user_id": user_id},
                {"course_id": course_id},
            ]
        },
    )