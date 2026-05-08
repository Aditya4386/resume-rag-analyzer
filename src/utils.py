"""
utils.py - General utility functions used across the application.

Keeps helper logic out of business-logic modules.
"""

import os
import re
from datetime import datetime


def get_ats_color(score: int) -> str:
    """
    Return a color hex string based on ATS score range.

    Args:
        score: ATS score 0-100.

    Returns:
        Hex color string for use in UI.
    """
    if score >= 80:
        return "#22c55e"   # Green — strong match
    elif score >= 60:
        return "#f59e0b"   # Amber — moderate match
    elif score >= 40:
        return "#f97316"   # Orange — weak match
    else:
        return "#ef4444"   # Red — poor match


def get_ats_label(score: int) -> str:
    """
    Return a human-readable label for an ATS score.

    Args:
        score: ATS score 0-100.

    Returns:
        Label string.
    """
    if score >= 80:
        return "Excellent Match 🌟"
    elif score >= 60:
        return "Good Match ✅"
    elif score >= 40:
        return "Moderate Match ⚠️"
    else:
        return "Poor Match ❌"


def truncate_text(text: str, max_chars: int = 200) -> str:
    """
    Truncate text to a max length and add ellipsis.

    Args:
        text: Input string.
        max_chars: Maximum number of characters.

    Returns:
        Truncated string.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"


def clean_text(text: str) -> str:
    """
    Remove excessive whitespace and normalize line endings.

    Args:
        text: Raw text.

    Returns:
        Cleaned text.
    """
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Replace 3+ consecutive newlines with 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def timestamp() -> str:
    """Return current timestamp as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dir(path: str) -> None:
    """Create a directory if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)
