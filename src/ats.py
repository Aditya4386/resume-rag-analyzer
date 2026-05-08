"""
ats.py - ATS (Applicant Tracking System) score calculation and analysis.

Combines:
1. Keyword-based skill matching (fast, deterministic)
2. LLM-based contextual analysis (nuanced, qualitative)

to produce a comprehensive ATS report.
"""

import re
from typing import TypedDict

from src.llm import query_llm
from src.prompts import get_ats_analysis_prompt
from src.skill_matcher import match_skills


class ATSReport(TypedDict):
    """Structured output from ATS analysis."""
    ats_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    improvement_suggestions: list[str]
    summary: str
    keyword_match_pct: float
    llm_raw_output: str


def parse_llm_ats_response(llm_output: str) -> dict:
    """
    Parse the structured LLM ATS response into Python data.

    The LLM is prompted to return a specific format; this function
    extracts each section using regex and string splitting.

    Args:
        llm_output: Raw text from the LLM.

    Returns:
        Dict with parsed fields.
    """
    result = {
        "ats_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "improvement_suggestions": [],
        "summary": "",
    }

    # Extract ATS score (looks for "ATS_SCORE: 75" pattern)
    score_match = re.search(r'ATS_SCORE:\s*(\d+)', llm_output, re.IGNORECASE)
    if score_match:
        result["ats_score"] = min(100, int(score_match.group(1)))

    # Extract matched skills section
    matched_section = _extract_section(llm_output, "MATCHED_SKILLS", "MISSING_SKILLS")
    result["matched_skills"] = _parse_bullet_list(matched_section)

    # Extract missing skills section
    missing_section = _extract_section(llm_output, "MISSING_SKILLS", "IMPROVEMENT_SUGGESTIONS")
    result["missing_skills"] = _parse_bullet_list(missing_section)

    # Extract improvement suggestions
    suggestions_section = _extract_section(llm_output, "IMPROVEMENT_SUGGESTIONS", "SUMMARY")
    result["improvement_suggestions"] = _parse_numbered_or_bullet_list(suggestions_section)

    # Extract summary
    summary_section = _extract_section(llm_output, "SUMMARY", None)
    result["summary"] = summary_section.strip()

    return result


def _extract_section(text: str, start_marker: str, end_marker: str | None) -> str:
    """
    Extract text between two section markers.

    Args:
        text: Full LLM output.
        start_marker: The section header to start from.
        end_marker: The next section header to stop at (or None for end of text).

    Returns:
        Text content of that section.
    """
    start_pattern = rf'{start_marker}:?\s*\n'
    start_match = re.search(start_pattern, text, re.IGNORECASE)

    if not start_match:
        return ""

    start_idx = start_match.end()

    if end_marker:
        end_pattern = rf'{end_marker}:?\s*\n'
        end_match = re.search(end_pattern, text[start_idx:], re.IGNORECASE)
        if end_match:
            return text[start_idx: start_idx + end_match.start()]

    return text[start_idx:]


def _parse_bullet_list(text: str) -> list[str]:
    """Extract bullet-point items from a text block."""
    items = []
    for line in text.strip().split('\n'):
        line = line.strip()
        # Remove bullet markers: -, *, •
        if line.startswith(('-', '*', '•')):
            item = line.lstrip('-*• ').strip()
            if item:
                items.append(item)
    return items


def _parse_numbered_or_bullet_list(text: str) -> list[str]:
    """Extract numbered or bulleted list items from a text block."""
    items = []
    for line in text.strip().split('\n'):
        line = line.strip()
        # Match "1. Item" or "- Item" or "* Item"
        match = re.match(r'^[\d]+\.\s+(.+)$', line) or \
                re.match(r'^[-*•]\s+(.+)$', line)
        if match:
            items.append(match.group(1).strip())
    return items


def run_ats_analysis(resume_text: str, job_description: str) -> ATSReport:
    """
    Run a full ATS analysis combining keyword matching and LLM analysis.

    The final ATS score is a weighted blend:
    - 40% from keyword/skill matching (objective)
    - 60% from LLM assessment (contextual)

    Args:
        resume_text: Full resume text.
        job_description: Target job description.

    Returns:
        ATSReport TypedDict with all analysis fields.
    """
    # Step 1: Fast keyword-based skill match
    skill_data = match_skills(resume_text, job_description)
    keyword_pct = skill_data["match_percentage"]

    # Step 2: LLM-based contextual analysis
    prompt = get_ats_analysis_prompt(resume_text, job_description)
    llm_output = query_llm(
        prompt=prompt,
        system_message="You are an expert ATS analyst. Follow the exact output format requested.",
    )

    # Step 3: Parse LLM response
    parsed = parse_llm_ats_response(llm_output)

    # Step 4: Blend scores (weighted average)
    llm_score = parsed["ats_score"]
    blended_score = int(0.4 * keyword_pct + 0.6 * llm_score)

    # Step 5: Merge skill lists (LLM may catch skills the keyword list misses)
    all_matched = list(set(skill_data["matched_skills"] + parsed["matched_skills"]))
    all_missing = list(set(skill_data["missing_skills"] + parsed["missing_skills"]))
    # Remove from missing if already in matched
    all_missing = [s for s in all_missing if s not in all_matched]

    return ATSReport(
        ats_score=blended_score,
        matched_skills=sorted(all_matched),
        missing_skills=sorted(all_missing),
        improvement_suggestions=parsed["improvement_suggestions"],
        summary=parsed["summary"],
        keyword_match_pct=keyword_pct,
        llm_raw_output=llm_output,
    )


def generate_interview_questions(resume_text: str, job_description: str) -> list[str]:
    """
    Generate tailored interview questions using the LLM.

    Args:
        resume_text: Full resume text.
        job_description: Target job description.

    Returns:
        List of interview question strings.
    """
    from src.prompts import get_interview_questions_prompt

    prompt = get_interview_questions_prompt(resume_text, job_description)
    llm_output = query_llm(
        prompt=prompt,
        system_message="You are an experienced technical interviewer. Generate specific, relevant questions.",
    )

    # Parse questions from the LLM output
    questions = []
    for line in llm_output.split('\n'):
        line = line.strip()
        # Match numbered items: "1. Question text"
        match = re.match(r'^\d+\.\s+(.+)$', line)
        if match:
            questions.append(match.group(1).strip())

    return questions if questions else [llm_output]  # Fallback to raw output
