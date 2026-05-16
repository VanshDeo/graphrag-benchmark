"""Shared embedding helpers for Pinecone-backed RAG."""

import os
from pinecone import Pinecone
from google import genai

EMBED_MODEL = os.getenv("PINECONE_EMBED_MODEL", "gemini-embedding-001")
EMBED_DIMENSION = int(os.getenv("PINECONE_EMBEDDING_DIMENSION", "3072"))


def get_pinecone_client() -> Pinecone:
    return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


def embed_texts(
    pc: Pinecone,
    texts: list[str],
    *,
    input_type: str,
) -> list[list[float]]:
    """Embed texts with Google Gemini Embedding (gemini-embedding-001 by default)."""
    if not texts:
        return []
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    task_type = "RETRIEVAL_QUERY" if input_type == "query" else "RETRIEVAL_DOCUMENT"
    embeddings = []
    for text in texts:
        result = client.models.embed_content(
            model=EMBED_MODEL,
            contents=text,
            config={
                "task_type": task_type,
                "output_dimensionality": EMBED_DIMENSION,
            },
        )
        if not result.embeddings:
            raise ValueError(f"Embedding API returned no embeddings for input: {text[:80]}...")
        embeddings.append(result.embeddings[0].values)
    return embeddings
