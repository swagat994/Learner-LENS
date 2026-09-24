from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from src.rag.vector_store import client


class SentenceTransformerEmbeddings(Embeddings):

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )
        return embedding.tolist()


embeddings = SentenceTransformerEmbeddings()


vectorstore = Chroma(
    client=client,
    collection_name="lecture_chunks",
    embedding_function=embeddings,
)


def get_retriever(
    user_id: str,
    course_id: str,
    n_results: int = 5,
):
    return vectorstore.as_retriever(
        search_kwargs={
            "k": n_results,
            "filter": {
                "$and": [
                    {"user_id": user_id},
                    {"course_id": course_id},
                ]
            },
        }
    )