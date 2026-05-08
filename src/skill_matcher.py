"""
skill_matcher.py - Skill extraction and matching between resume and job description.

Uses a combination of:
- A curated skill keyword list for fast matching
- LLM-based extraction for nuanced/contextual skills
"""

import re
from typing import List, Set

# ── Common tech & professional skills dictionary ──────────────────────────────
# This list covers the most common skills seen in tech resumes and JDs.
COMMON_SKILLS: List[str] = [
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
    # Web Frameworks
    "react", "vue", "angular", "nextjs", "nuxtjs", "svelte", "django",
    "flask", "fastapi", "express", "spring", "rails", "laravel", "asp.net",
    # Data & ML
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch",
    "tensorflow", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
    "seaborn", "hugging face", "transformers", "llm", "rag", "langchain",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "sqlite", "oracle", "dynamodb", "cassandra", "neo4j", "chromadb",
    # Cloud & DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "ci/cd", "linux", "bash", "git",
    # Data Engineering
    "spark", "kafka", "airflow", "dbt", "hadoop", "etl", "data pipeline",
    "snowflake", "bigquery", "redshift", "databricks",
    # APIs & Architecture
    "rest api", "graphql", "microservices", "grpc", "websocket", "oauth",
    "jwt", "api design", "system design", "distributed systems",
    # Soft Skills
    "agile", "scrum", "jira", "communication", "leadership", "teamwork",
    "problem solving", "project management", "mentoring",
    # Other Tech
    "html", "css", "tailwind", "bootstrap", "figma", "selenium", "pytest",
    "unit testing", "tdd", "code review", "excel", "tableau", "power bi",
]


def extract_skills_from_text(text: str) -> Set[str]:
    """
    Extract skills from a text by matching against the COMMON_SKILLS list.

    Performs case-insensitive matching using regex word boundaries to avoid
    false positives (e.g., "Go" matching "good").

    Args:
        text: Any block of text (resume or job description).

    Returns:
        Set of matched skill strings (lowercase).
    """
    text_lower = text.lower()
    found_skills: Set[str] = set()

    for skill in COMMON_SKILLS:
        # Use word boundaries to match whole words/phrases only
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return found_skills


def match_skills(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Compare skills found in the resume vs. the job description.

    Args:
        resume_text: Full resume text.
        job_description: Target job description text.

    Returns:
        A dict with keys:
            - resume_skills: set of all skills found in resume
            - jd_skills: set of all skills found in job description
            - matched_skills: skills present in both
            - missing_skills: JD skills NOT found in resume
            - match_percentage: float 0-100
    """
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_skills_from_text(job_description)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills.difference(resume_skills)

    # Calculate match percentage against JD requirements
    match_pct = (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0

    return {
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_percentage": round(match_pct, 1),
    }
