"""
app.py - Main Streamlit application entry point.

This is the top-level file that ties everything together.
Run with: streamlit run app.py

Architecture overview:
- UI rendering   → src/ui/components.py
- PDF parsing    → src/resume_parser.py
- Embeddings     → src/embeddings.py
- RAG pipeline   → src/rag_pipeline.py
- ATS scoring    → src/ats.py
- LLM calls      → src/llm.py
- Config         → src/config.py
"""

import streamlit as st

# ── Page config must be the FIRST Streamlit call ──────────────────────────────
st.set_page_config(
    page_title="Resume RAG Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import a clean, modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark background for the whole app */
    .stApp {
        background-color: #020817;
        color: #e2e8f0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0a0f1e;
        border-right: 1px solid #1e293b;
    }

    /* Remove default Streamlit padding on main block */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    /* Style all Streamlit buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover {
        opacity: 0.85 !important;
    }

    /* Style tab headers */
    .stTabs [data-baseweb="tab-list"] {
        background: #0f172a;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        color: #94a3b8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b !important;
        color: #e2e8f0 !important;
    }

    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    /* File uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: #0f172a !important;
        border: 1.5px dashed #334155 !important;
        border-radius: 8px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }

    /* Hide the default Streamlit menu & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Internal imports (after set_page_config) ──────────────────────────────────
from src.config import validate_config
from src.resume_parser import parse_resume
from src.embeddings import store_chunks_in_chroma
from src.rag_pipeline import answer_question, generate_resume_summary
from src.ats import run_ats_analysis, generate_interview_questions
from src.ui.components import (
    render_header,
    render_sidebar,
    render_ats_score_card,
    render_skills_section,
    render_suggestions,
    render_interview_questions,
    render_resume_summary,
    render_rag_qa_section,
    render_error,
    render_success,
)


# ── Session state initialization ──────────────────────────────────────────────
def init_session_state() -> None:
    """Initialize all session state variables on first run."""
    defaults = {
        "resume_text": None,       # Full extracted resume text
        "resume_chunks": None,     # Chunked text list
        "ats_report": None,        # ATSReport dict
        "resume_summary": None,    # LLM-generated summary string
        "interview_questions": [], # List of question strings
        "analyze_clicked": False,  # Whether analysis has been triggered
        "resume_processed": False, # Whether the current PDF has been embedded
        "last_pdf_name": None,     # Track which PDF is loaded (for re-uploads)
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ── Main application ──────────────────────────────────────────────────────────
def main() -> None:
    """Main application controller."""
    init_session_state()
    render_header()

    # Validate config before doing anything
    config_valid, config_msg = validate_config()
    if not config_valid:
        render_error(config_msg)
        st.stop()

    # ── Sidebar: get user inputs ───────────────────────────────────────────
    uploaded_file, job_description = render_sidebar()

    # ── Process uploaded PDF ───────────────────────────────────────────────
    if uploaded_file is not None:
        # Only re-process if a new file is uploaded
        if st.session_state["last_pdf_name"] != uploaded_file.name:
            with st.spinner("📖 Parsing resume PDF..."):
                try:
                    resume_text, chunks = parse_resume(uploaded_file)
                    st.session_state["resume_text"] = resume_text
                    st.session_state["resume_chunks"] = chunks
                    st.session_state["resume_processed"] = False  # Force re-embed
                    st.session_state["last_pdf_name"] = uploaded_file.name
                    st.session_state["ats_report"] = None  # Reset old results
                    st.session_state["resume_summary"] = None
                    st.session_state["interview_questions"] = []
                except ValueError as e:
                    render_error(str(e))
                    st.stop()

        # Embed chunks into ChromaDB if not done yet
        if not st.session_state["resume_processed"]:
            with st.spinner("🧮 Generating embeddings..."):
                store_chunks_in_chroma(st.session_state["resume_chunks"])
                st.session_state["resume_processed"] = True

    # ── Run analysis when button is clicked ───────────────────────────────
    if st.session_state.get("analyze_clicked") and st.session_state["resume_text"]:
        st.session_state["analyze_clicked"] = False  # Reset so it doesn't re-run

        if not job_description.strip():
            st.warning("⚠️ Please paste a job description in the sidebar to run analysis.")
        else:
            # Generate resume summary
            with st.spinner("📝 Summarizing resume..."):
                st.session_state["resume_summary"] = generate_resume_summary(
                    st.session_state["resume_text"]
                )

            # Run ATS analysis
            with st.spinner("🔍 Running ATS analysis..."):
                st.session_state["ats_report"] = run_ats_analysis(
                    st.session_state["resume_text"],
                    job_description,
                )

            # Generate interview questions
            with st.spinner("🎤 Generating interview questions..."):
                st.session_state["interview_questions"] = generate_interview_questions(
                    st.session_state["resume_text"],
                    job_description,
                )

            render_success("Analysis complete! Scroll down to view results.")

    # ── Render results ────────────────────────────────────────────────────
    if st.session_state["resume_text"] is None:
        # Welcome / empty state
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; color: #334155;">
                <div style="font-size: 5rem;">📄</div>
                <h3 style="color: #475569; margin: 1rem 0 0.5rem 0;">
                    Upload your resume to get started
                </h3>
                <p style="color: #64748b; max-width: 400px; margin: 0 auto;">
                    Upload a PDF resume in the sidebar, paste a job description,
                    then click <b>Analyze Resume</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    # ── Tabs for the results sections ────────────────────────────────────
    tabs = st.tabs([
        "📊 Overview",
        "🎯 ATS Score",
        "💡 Skills",
        "📈 Suggestions",
        "🎤 Interview Prep",
        "💬 Ask Questions",
    ])

    # ── Tab 1: Overview / Resume Summary ─────────────────────────────────
    with tabs[0]:
        st.markdown("### 📄 Resume Summary")

        if st.session_state["resume_summary"]:
            render_resume_summary(st.session_state["resume_summary"])
        else:
            # Show raw extracted text preview
            st.caption("Summary will appear after analysis. Preview of extracted text:")
            with st.expander("📋 Raw Extracted Text Preview", expanded=True):
                st.text(st.session_state["resume_text"][:2000] + "...")

        # Chunk count info
        if st.session_state["resume_chunks"]:
            st.caption(
                f"ℹ️ Resume split into **{len(st.session_state['resume_chunks'])}** chunks "
                f"and indexed in ChromaDB."
            )

    # ── Tab 2: ATS Score ─────────────────────────────────────────────────
    with tabs[1]:
        if st.session_state["ats_report"]:
            report = st.session_state["ats_report"]

            col1, col2 = st.columns([1, 2])
            with col1:
                render_ats_score_card(report["ats_score"])

                # Keyword match sub-metric
                st.markdown(f"""
                    <div style="background: #0f172a; border-radius: 8px;
                                padding: 0.75rem; text-align: center; border: 1px solid #1e293b;">
                        <div style="color: #94a3b8; font-size: 0.8rem;">Keyword Match</div>
                        <div style="color: #a78bfa; font-size: 1.4rem; font-weight: 700;">
                            {report['keyword_match_pct']}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("#### 📝 Assessment")
                if report["summary"]:
                    st.markdown(f"""
                        <div style="background: #0f172a; border-radius: 10px;
                                    padding: 1rem 1.25rem; border: 1px solid #1e293b;
                                    color: #cbd5e1; line-height: 1.7;">
                            {report['summary']}
                        </div>
                    """, unsafe_allow_html=True)

                # Score breakdown
                st.markdown("#### 📊 Score Breakdown")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Keyword Match", f"{report['keyword_match_pct']}%")
                with col_b:
                    st.metric("Overall ATS Score", f"{report['ats_score']}%")
        else:
            st.info("⬅️ Upload a resume and paste a job description, then click **Analyze Resume** to get your ATS score.")

    # ── Tab 3: Skills ─────────────────────────────────────────────────────
    with tabs[2]:
        if st.session_state["ats_report"]:
            report = st.session_state["ats_report"]
            render_skills_section(
                matched=report["matched_skills"],
                missing=report["missing_skills"],
            )
        else:
            st.info("⬅️ Run analysis to see skill matching results.")

    # ── Tab 4: Improvement Suggestions ───────────────────────────────────
    with tabs[3]:
        if st.session_state["ats_report"]:
            st.markdown("### 📈 Improvement Suggestions")
            st.caption("AI-generated recommendations to improve your resume for this role.")
            render_suggestions(st.session_state["ats_report"]["improvement_suggestions"])
        else:
            st.info("⬅️ Run analysis to see improvement suggestions.")

    # ── Tab 5: Interview Questions ────────────────────────────────────────
    with tabs[4]:
        if st.session_state["interview_questions"]:
            st.markdown("### 🎤 Interview Questions")
            st.caption("Tailored questions based on your resume and the job description.")
            render_interview_questions(st.session_state["interview_questions"])
        else:
            st.info("⬅️ Run analysis to generate interview questions.")

    # ── Tab 6: RAG Q&A ────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown("### 💬 Ask Questions About Your Resume")

        # Quick question chips
        st.caption("Quick questions:")
        quick_qs = [
            "What are my top skills?",
            "Summarize my work experience",
            "What projects have I worked on?",
            "What is my educational background?",
        ]
        cols = st.columns(len(quick_qs))
        for i, (col, q) in enumerate(zip(cols, quick_qs)):
            with col:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    st.session_state["quick_question"] = q

        st.markdown("")

        # Handle quick question or form input
        question = render_rag_qa_section()

        if "quick_question" in st.session_state:
            question = st.session_state.pop("quick_question")

        if question:
            with st.spinner("🤔 Thinking..."):
                answer = answer_question(question)

            st.markdown(f"""
                <div style="background: #0f172a; border-radius: 10px; 
                            padding: 1rem 1.25rem; border: 1px solid #1e293b;
                            margin-top: 1rem;">
                    <div style="color: #a78bfa; font-size: 0.85rem; 
                                font-weight: 600; margin-bottom: 0.5rem;">
                        🤖 Answer
                    </div>
                    <div style="color: #e2e8f0; line-height: 1.7;">{answer}</div>
                </div>
            """, unsafe_allow_html=True)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
