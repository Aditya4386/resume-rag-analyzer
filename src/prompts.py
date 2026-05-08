"""
prompts.py - All LLM prompt templates in one place.

Centralizing prompts makes them easy to iterate on without
touching business logic in other modules.
"""


def get_rag_qa_prompt(context: str, question: str) -> str:
    """
    Build a RAG-style QA prompt that grounds answers in retrieved chunks.

    Args:
        context: Concatenated relevant resume chunks.
        question: The user's question about the resume.

    Returns:
        A formatted prompt string ready to send to the LLM.
    """
    return f"""You are a professional resume analyst. Answer the question below 
using ONLY the provided resume context. Be concise and accurate.

--- RESUME CONTEXT ---
{context}
----------------------

Question: {question}

Answer (based strictly on the resume context above):"""


def get_ats_analysis_prompt(resume_text: str, job_description: str) -> str:
    """
    Prompt for generating a detailed ATS compatibility analysis.

    Args:
        resume_text: Full extracted resume text.
        job_description: The job description to match against.

    Returns:
        Formatted prompt string.
    """
    return f"""You are an expert ATS (Applicant Tracking System) analyst.

Analyze the resume against the job description and provide a structured analysis.

--- RESUME ---
{resume_text[:3000]}  
--------------

--- JOB DESCRIPTION ---
{job_description[:2000]}
-----------------------

Provide your analysis in this EXACT format:

ATS_SCORE: [number between 0-100]

MATCHED_SKILLS:
- [skill 1]
- [skill 2]
- [skill 3]
(list all matched skills)

MISSING_SKILLS:
- [missing skill 1]
- [missing skill 2]
(list all important skills from JD not found in resume)

IMPROVEMENT_SUGGESTIONS:
1. [Specific, actionable suggestion]
2. [Specific, actionable suggestion]
3. [Specific, actionable suggestion]
4. [Specific, actionable suggestion]
5. [Specific, actionable suggestion]

SUMMARY:
[2-3 sentence overall assessment of the resume fit for this role]"""


def get_resume_summary_prompt(resume_text: str) -> str:
    """
    Prompt for generating a concise professional summary of a resume.

    Args:
        resume_text: Full extracted resume text.

    Returns:
        Formatted prompt string.
    """
    return f"""You are a professional resume reviewer.

Read the following resume and provide a structured summary:

--- RESUME ---
{resume_text[:3000]}
--------------

Provide a summary in this format:

CANDIDATE_NAME: [name if found, else "Not found"]

PROFESSIONAL_SUMMARY:
[2-3 sentences describing the candidate's background and expertise]

KEY_SKILLS:
- [skill 1]
- [skill 2]
- [skill 3]
(list top 8-10 skills)

EXPERIENCE_HIGHLIGHTS:
- [highlight 1]
- [highlight 2]
- [highlight 3]

EDUCATION:
[Degree, Institution, Year if present]

YEARS_OF_EXPERIENCE: [estimated years or "Not specified"]"""


def get_interview_questions_prompt(resume_text: str, job_description: str) -> str:
    """
    Prompt for generating tailored interview questions.

    Args:
        resume_text: Full extracted resume text.
        job_description: The target job description.

    Returns:
        Formatted prompt string.
    """
    return f"""You are an experienced technical interviewer.

Based on the resume and job description below, generate targeted interview questions
that will help assess if this candidate is right for the role.

--- RESUME (excerpt) ---
{resume_text[:2000]}
------------------------

--- JOB DESCRIPTION ---
{job_description[:1500]}
-----------------------

Generate 10 interview questions across these categories:

TECHNICAL_QUESTIONS:
1. [Question testing a specific technical skill]
2. [Question testing another technical skill]
3. [Question about a project mentioned in resume]
4. [Question about technical depth]

BEHAVIORAL_QUESTIONS:
5. [STAR-format behavioral question]
6. [Question about teamwork/collaboration]
7. [Question about handling challenges]

ROLE_SPECIFIC_QUESTIONS:
8. [Question specific to this job's requirements]
9. [Question about relevant experience]
10. [Question about career goals alignment]"""
