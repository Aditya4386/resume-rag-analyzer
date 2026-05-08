"""
rag_pipeline.py - The RAG (Retrieval-Augmented Generation) pipeline.

Ties together:
1. Embedding-based retrieval from ChromaDB
2. Context formatting
3. LLM-powered answer generation

This is the core of the application's Q&A feature.
"""

from src.embeddings import retrieve_relevant_chunks
from src.llm import query_llm
from src.prompts import get_rag_qa_prompt


def answer_question(question: str) -> str:
    """
    Answer a user question about the resume using RAG.

    Pipeline:
    1. Embed the question
    2. Retrieve the top-K most relevant resume chunks from ChromaDB
    3. Format them as context
    4. Send context + question to the LLM
    5. Return the answer

    Args:
        question: The user's natural language question.

    Returns:
        LLM-generated answer grounded in the resume content.
    """
    # Step 1 & 2: Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(query=question)

    if not relevant_chunks:
        return "❌ No resume data found. Please upload a resume first."

    # Step 3: Format context
    context = "\n\n".join(relevant_chunks)

    # Step 4: Build prompt and query LLM
    prompt = get_rag_qa_prompt(context=context, question=question)

    # Step 5: Return answer
    answer = query_llm(
        prompt=prompt,
        system_message="You are a helpful resume analyst. Answer only based on the provided context.",
    )

    return answer


def generate_resume_summary(resume_text: str) -> str:
    """
    Generate a structured summary of the resume using the LLM.

    Unlike RAG QA, this uses the full resume text directly
    (no retrieval needed — we already have all the content).

    Args:
        resume_text: Full extracted resume text.

    Returns:
        Structured summary string from the LLM.
    """
    from src.prompts import get_resume_summary_prompt

    prompt = get_resume_summary_prompt(resume_text)
    return query_llm(
        prompt=prompt,
        system_message="You are a professional resume reviewer. Be accurate and concise.",
    )
