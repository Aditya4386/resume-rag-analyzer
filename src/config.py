"""
config.py - Central configuration for the Resume RAG application.

All settings, constants, and environment variable loading happen here.
Import from this module anywhere you need config values.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ── Groq / LLM settings ──────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
LLM_MODEL: str = "llama-3.1-8b-instant"     # Groq model to use
LLM_TEMPERATURE: float = 0.3           # Lower = more deterministic output
LLM_MAX_TOKENS: int = 1024            # Max tokens per LLM response

# ── Embedding settings ────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"   # Sentence-transformers model

# ── ChromaDB settings ─────────────────────────────────────────────────────────
CHROMA_DB_PATH: str = "./chroma_db"          # Persistent storage path
CHROMA_COLLECTION_NAME: str = "resume_chunks"

# ── Text splitting settings ───────────────────────────────────────────────────
CHUNK_SIZE: int = 500     # Characters per chunk
CHUNK_OVERLAP: int = 100  # Overlap between consecutive chunks

# ── Retrieval settings ────────────────────────────────────────────────────────
TOP_K_RESULTS: int = 3    # Number of relevant chunks to retrieve

# ── File settings ─────────────────────────────────────────────────────────────
DATA_DIR: str = "./data"  # Temp storage for uploaded files


def validate_config() -> tuple[bool, str]:
    """
    Check that all required config values are set.

    Returns:
        (is_valid: bool, message: str)
    """
    if not GROQ_API_KEY:
        return False, "❌ GROQ_API_KEY is not set. Please add it to your .env file."
    return True, "✅ Configuration is valid."
