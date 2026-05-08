"""
config.py - Central configuration for the Resume RAG application.

Handles:
- Environment variables
- Streamlit Cloud secrets
- Application settings
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env file (works locally)
load_dotenv()


# ── Groq / LLM settings ──────────────────────────────────────────────────────

# First check local .env
# If not found, check Streamlit Cloud secrets
GROQ_API_KEY: str = os.getenv(
    "GROQ_API_KEY",
    st.secrets.get("GROQ_API_KEY", "")
)

# Current active Groq model
LLM_MODEL: str = "llama-3.1-8b-instant"

# Lower temperature = more consistent responses
LLM_TEMPERATURE: float = 0.3

# Maximum response tokens
LLM_MAX_TOKENS: int = 1024


# ── Embedding settings ────────────────────────────────────────────────────────

# Sentence-transformers embedding model
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"


# ── ChromaDB settings ─────────────────────────────────────────────────────────

# Persistent database path
CHROMA_DB_PATH: str = "./chroma_db"

# Chroma collection name
CHROMA_COLLECTION_NAME: str = "resume_chunks"


# ── Text splitting settings ───────────────────────────────────────────────────

# Characters per chunk
CHUNK_SIZE: int = 500

# Overlap between chunks
CHUNK_OVERLAP: int = 100


# ── Retrieval settings ────────────────────────────────────────────────────────

# Number of retrieved chunks
TOP_K_RESULTS: int = 3


# ── File settings ─────────────────────────────────────────────────────────────

# Temporary uploaded file storage
DATA_DIR: str = "./data"


def validate_config() -> tuple[bool, str]:
    """
    Validate required configuration values.

    Returns:
        tuple[bool, str]:
            (is_valid, message)
    """

    if not GROQ_API_KEY:
        return (
            False,
            "❌ GROQ_API_KEY not found. Add it to .env or Streamlit secrets."
        )

    return True, "✅ Configuration is valid."