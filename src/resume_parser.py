"""
resume_parser.py - Handles PDF resume parsing and text extraction.

Uses pypdf to extract raw text from uploaded PDF files,
then applies LangChain's RecursiveCharacterTextSplitter to break
the text into overlapping chunks suitable for embedding.
"""

import os
import tempfile
from typing import List

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_DIR


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract all text content from an uploaded PDF file.

    Args:
        pdf_file: A Streamlit UploadedFile object (file-like object).

    Returns:
        A single string containing all extracted text from the PDF.

    Raises:
        ValueError: If the PDF is empty or text extraction fails.
    """
    try:
        # Save the uploaded file to a temp location so pypdf can read it
        os.makedirs(DATA_DIR, exist_ok=True)
        temp_path = os.path.join(DATA_DIR, "temp_resume.pdf")

        with open(temp_path, "wb") as f:
            f.write(pdf_file.read())

        # Use pypdf to read all pages
        reader = PdfReader(temp_path)
        full_text = ""

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += f"\n--- Page {page_num + 1} ---\n{page_text}"

        if not full_text.strip():
            raise ValueError("No text could be extracted from the PDF. It may be image-based.")

        return full_text.strip()

    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def split_text_into_chunks(text: str) -> List[str]:
    """
    Split a long text string into smaller overlapping chunks.

    Uses RecursiveCharacterTextSplitter which tries to split on
    paragraph breaks, then sentences, then words — preserving context.

    Args:
        text: The full extracted resume text.

    Returns:
        A list of text chunks, each ≤ CHUNK_SIZE characters.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Try these separators in order for clean splits
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)
    return chunks


def parse_resume(pdf_file) -> tuple[str, List[str]]:
    """
    Full pipeline: extract text from PDF → split into chunks.

    Args:
        pdf_file: Streamlit UploadedFile object.

    Returns:
        (full_text, chunks) — the complete text and its split chunks.
    """
    full_text = extract_text_from_pdf(pdf_file)
    chunks = split_text_into_chunks(full_text)
    return full_text, chunks
