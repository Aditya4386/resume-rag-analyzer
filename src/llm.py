"""
llm.py - Groq LLM integration module.

Handles all communication with the Groq API using the Llama 3 model.
Provides a simple query_llm() function used by other modules.
"""

from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

# ── Client singleton ──────────────────────────────────────────────────────────
_client: Groq | None = None


def get_groq_client() -> Groq:
    """
    Return a Groq client, initializing it only once.

    Returns:
        Initialized Groq client.

    Raises:
        ValueError: If GROQ_API_KEY is not set.
    """
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Please copy .env.example to .env and add your key."
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def query_llm(prompt: str, system_message: str = "") -> str:
    """
    Send a prompt to the Groq LLM and return the response text.

    Args:
        prompt: The user-facing prompt / question.
        system_message: Optional system-level instruction to set the AI's role.

    Returns:
        The LLM's response as a plain string.

    Raises:
        Exception: Propagates any Groq API errors.
    """
    client = get_groq_client()

    messages = []

    # Add system message if provided
    if system_message:
        messages.append({"role": "system", "content": system_message})

    messages.append({"role": "user", "content": prompt})

    # Call the Groq API
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )

    # Extract the text from the first choice
    return response.choices[0].message.content.strip()
