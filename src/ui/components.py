"""
components.py - Reusable Streamlit UI components.

All visual building blocks live here to keep app.py clean.
Each function renders one logical section of the UI.
"""

import streamlit as st
from src.utils import get_ats_color, get_ats_label


def render_header() -> None:
    """Render the top application header and tagline."""
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
            <h1 style="font-size: 2.4rem; font-weight: 800; 
                       background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin-bottom: 0.3rem;">
                📄 Resume RAG Analyzer
            </h1>
            <p style="color: #94a3b8; font-size: 1rem; margin: 0;">
                AI-powered resume analysis · ATS scoring · Interview prep
            </p>
        </div>
        <hr style="border-color: #1e293b; margin: 0.5rem 0 1.5rem 0;">
    """, unsafe_allow_html=True)


def render_sidebar() -> tuple[object | None, str]:
    """
    Render the sidebar with file uploader and job description input.

    Returns:
        (uploaded_file, job_description) — the user's inputs.
    """
    with st.sidebar:
        st.markdown("""
            <h2 style="color: #a78bfa; font-weight: 700; margin-bottom: 0.2rem;">
                ⚙️ Input Panel
            </h2>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Resume Upload ──────────────────────────────────────────────────
        st.markdown("**📂 Upload Resume (PDF)**")
        uploaded_file = st.file_uploader(
            label="Drop your resume here",
            type=["pdf"],
            help="Upload a PDF resume to analyze",
            label_visibility="collapsed",
        )

        st.markdown("---")

        # ── Job Description ────────────────────────────────────────────────
        st.markdown("**📋 Job Description**")
        job_description = st.text_area(
            label="Paste job description",
            placeholder="Paste the full job description here...\n\nExample:\nWe are looking for a Senior Python Developer with 5+ years experience in Django, PostgreSQL, and AWS...",
            height=280,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # ── Analyze Button ─────────────────────────────────────────────────
        analyze_clicked = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
        )

        # Store button state in session
        if analyze_clicked:
            st.session_state["analyze_clicked"] = True

        # ── Info box ───────────────────────────────────────────────────────
        st.markdown("""
            <div style="background: #0f172a; border: 1px solid #1e293b; 
                        border-radius: 8px; padding: 0.75rem; margin-top: 1rem;
                        font-size: 0.8rem; color: #64748b;">
                <b style="color: #94a3b8;">How to use:</b><br>
                1. Upload your PDF resume<br>
                2. Paste a job description<br>
                3. Click Analyze Resume<br>
                4. Ask questions below
            </div>
        """, unsafe_allow_html=True)

    return uploaded_file, job_description


def render_ats_score_card(score: int) -> None:
    """
    Render a large, visually prominent ATS score card.

    Args:
        score: ATS score 0-100.
    """
    color = get_ats_color(score)
    label = get_ats_label(score)

    # Determine arc length for circular progress (circumference = 2πr ≈ 251)
    circumference = 251
    arc_length = int(circumference * score / 100)

    st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; 
                    background: #0f172a; border-radius: 16px; 
                    border: 1px solid #1e293b; margin-bottom: 1rem;">
            <svg width="160" height="160" viewBox="0 0 100 100">
                <!-- Background circle -->
                <circle cx="50" cy="50" r="40" fill="none" 
                        stroke="#1e293b" stroke-width="8"/>
                <!-- Progress arc -->
                <circle cx="50" cy="50" r="40" fill="none"
                        stroke="{color}" stroke-width="8"
                        stroke-dasharray="{arc_length} {circumference}"
                        stroke-linecap="round"
                        transform="rotate(-90 50 50)"/>
                <!-- Score text -->
                <text x="50" y="45" text-anchor="middle" 
                      font-size="22" font-weight="bold" fill="{color}">{score}</text>
                <text x="50" y="60" text-anchor="middle" 
                      font-size="9" fill="#64748b">ATS SCORE</text>
            </svg>
            <div style="font-size: 1.1rem; font-weight: 600; color: {color}; 
                        margin-top: 0.5rem;">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def render_skills_section(matched: list, missing: list) -> None:
    """
    Render matched and missing skills as colored pill badges.

    Args:
        matched: List of matched skill strings.
        missing: List of missing skill strings.
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Matched Skills")
        if matched:
            pills_html = " ".join([
                f'<span style="display: inline-block; background: #064e3b; '
                f'color: #6ee7b7; padding: 3px 10px; border-radius: 20px; '
                f'font-size: 0.78rem; margin: 2px; border: 1px solid #065f46;">'
                f'{skill}</span>'
                for skill in matched
            ])
            st.markdown(f'<div style="line-height: 2.2;">{pills_html}</div>',
                        unsafe_allow_html=True)
        else:
            st.info("No matching skills detected.")

    with col2:
        st.markdown("#### ❌ Missing Skills")
        if missing:
            pills_html = " ".join([
                f'<span style="display: inline-block; background: #450a0a; '
                f'color: #fca5a5; padding: 3px 10px; border-radius: 20px; '
                f'font-size: 0.78rem; margin: 2px; border: 1px solid #7f1d1d;">'
                f'{skill}</span>'
                for skill in missing
            ])
            st.markdown(f'<div style="line-height: 2.2;">{pills_html}</div>',
                        unsafe_allow_html=True)
        else:
            st.success("No critical skills missing! 🎉")


def render_suggestions(suggestions: list[str]) -> None:
    """
    Render improvement suggestions as a numbered card list.

    Args:
        suggestions: List of suggestion strings.
    """
    if not suggestions:
        st.info("No suggestions available.")
        return

    for i, suggestion in enumerate(suggestions, 1):
        st.markdown(f"""
            <div style="background: #0f172a; border-left: 3px solid #6366f1;
                        border-radius: 0 8px 8px 0; padding: 0.75rem 1rem;
                        margin: 0.5rem 0;">
                <span style="color: #6366f1; font-weight: 700;">#{i}</span>
                <span style="color: #cbd5e1; margin-left: 0.5rem;">{suggestion}</span>
            </div>
        """, unsafe_allow_html=True)


def render_interview_questions(questions: list[str]) -> None:
    """
    Render interview questions in expandable accordion-style cards.

    Args:
        questions: List of interview question strings.
    """
    if not questions:
        st.info("No interview questions generated.")
        return

    categories = {
        "Technical": [],
        "Behavioral": [],
        "Role-Specific": [],
        "General": [],
    }

    # Simple categorization by position (matches prompt structure)
    for i, q in enumerate(questions):
        if i < 4:
            categories["Technical"].append(q)
        elif i < 7:
            categories["Behavioral"].append(q)
        elif i < 10:
            categories["Role-Specific"].append(q)
        else:
            categories["General"].append(q)

    icons = {"Technical": "⚙️", "Behavioral": "🧠", "Role-Specific": "🎯", "General": "💬"}

    for category, qs in categories.items():
        if qs:
            with st.expander(f"{icons[category]} {category} Questions ({len(qs)})", expanded=(category == "Technical")):
                for i, q in enumerate(qs, 1):
                    st.markdown(f"""
                        <div style="background: #0f172a; border-radius: 8px;
                                    padding: 0.75rem 1rem; margin: 0.4rem 0;
                                    border: 1px solid #1e293b;">
                            <span style="color: #a78bfa; font-weight: 600;">Q{i}.</span>
                            <span style="color: #e2e8f0; margin-left: 0.4rem;">{q}</span>
                        </div>
                    """, unsafe_allow_html=True)


def render_resume_summary(summary_text: str) -> None:
    """
    Render the LLM-generated resume summary in a clean card.

    Args:
        summary_text: Raw summary output from the LLM.
    """
    # Format sections by bolding the labels
    formatted = summary_text
    labels = [
        "CANDIDATE_NAME", "PROFESSIONAL_SUMMARY", "KEY_SKILLS",
        "EXPERIENCE_HIGHLIGHTS", "EDUCATION", "YEARS_OF_EXPERIENCE"
    ]
    for label in labels:
        display = label.replace("_", " ").title()
        formatted = formatted.replace(
            f"{label}:", f"\n**{display}:**"
        )

    st.markdown(f"""
        <div style="background: #0f172a; border: 1px solid #1e293b;
                    border-radius: 12px; padding: 1.25rem 1.5rem;">
    """, unsafe_allow_html=True)
    st.markdown(formatted)
    st.markdown("</div>", unsafe_allow_html=True)


def render_rag_qa_section() -> str | None:
    """
    Render the RAG Q&A input section.

    Returns:
        The user's question string, or None if not submitted.
    """
    st.markdown("#### 💬 Ask About Your Resume")
    st.caption("Ask anything about your resume — skills, experience, projects, etc.")

    with st.form("rag_qa_form", clear_on_submit=False):
        question = st.text_input(
            label="Your question",
            placeholder="e.g. What programming languages do I know? / Summarize my work experience",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Ask →", use_container_width=False)

    if submitted and question.strip():
        return question.strip()
    return None


def render_error(message: str) -> None:
    """Display a styled error message."""
    st.markdown(f"""
        <div style="background: #450a0a; border: 1px solid #b91c1c;
                    border-radius: 8px; padding: 0.75rem 1rem; color: #fca5a5;">
            ⚠️ {message}
        </div>
    """, unsafe_allow_html=True)


def render_success(message: str) -> None:
    """Display a styled success message."""
    st.markdown(f"""
        <div style="background: #064e3b; border: 1px solid #065f46;
                    border-radius: 8px; padding: 0.75rem 1rem; color: #6ee7b7;">
            ✅ {message}
        </div>
    """, unsafe_allow_html=True)
