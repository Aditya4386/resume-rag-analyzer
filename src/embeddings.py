"""
embeddings.py - Manages sentence-transformer embeddings and ChromaDB storage.

This module:
1. Loads the sentence-transformer model (all-MiniLM-L6-v2)
2. Encodes text chunks into dense vector embeddings
3. Stores them in ChromaDB for persistent retrieval
4. Provides a similarity search function
"""

from typing import List
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from src.config import (
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    TOP_K_RESULTS,
)

# ── Singleton model — load once, reuse everywhere ─────────────────────────────
_embedding_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """
    Return the embedding model, loading it only once (singleton pattern).

    The model is cached in a module-level variable to avoid reloading
    on every function call (loading takes ~2 seconds).

    Returns:
        A loaded SentenceTransformer model instance.
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convert a list of text strings into embedding vectors.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of float vectors (one per input text).
    """
    model = get_embedding_model()
    # convert_to_list ensures we get plain Python lists, not numpy arrays
    embeddings = model.encode(texts, convert_to_numpy=True).tolist()
    return embeddings


# ── ChromaDB helpers ──────────────────────────────────────────────────────────

def get_chroma_collection() -> chromadb.Collection:
    """
    Connect to (or create) a persistent ChromaDB collection.

    Returns:
        A ChromaDB collection ready for add/query operations.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    # get_or_create_collection is idempotent — safe to call multiple times
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # Use cosine similarity
    )
    return collection


def store_chunks_in_chroma(chunks: List[str]) -> None:
    """
    Embed text chunks and store them in ChromaDB.

    Each chunk gets:
    - A unique ID (chunk_0, chunk_1, …)
    - Its embedding vector
    - The original text as the document

    Clears any existing data first so each upload is fresh.

    Args:
        chunks: List of text chunks from the resume.
    """
    collection = get_chroma_collection()

    # Clear previous resume data before inserting new one
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # Generate embeddings for all chunks at once (batched = faster)
    embeddings = embed_texts(chunks)

    # Create unique IDs for each chunk
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
    )


def retrieve_relevant_chunks(query: str) -> List[str]:
    """
    Find the most semantically similar chunks to a query.

    Args:
        query: The user's question or a skill/keyword to search for.

    Returns:
        List of the top-K most relevant text chunks.
    """
    collection = get_chroma_collection()

    # Embed the query using the same model
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(TOP_K_RESULTS, collection.count()),  # Guard against empty DB
    )

    # results["documents"] is a list of lists — flatten one level
    return results["documents"][0] if results["documents"] else []
