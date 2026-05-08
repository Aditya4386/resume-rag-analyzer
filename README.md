# 📄 Resume RAG Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![RAG](https://img.shields.io/badge/AI-RAG-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

> An AI-powered Resume + Job Description Analyzer built using RAG (Retrieval-Augmented Generation).

Upload a resume PDF, paste a job description, and get:
- ATS score analysis
- Skill gap detection
- Resume improvement suggestions
- AI-generated interview questions
- Resume Q&A using RAG

---

# 🌐 Live Demo

🚀 Deployed Application:

[Resume RAG Analyzer Live App](https://resume-rag-analyzer-for-job-description.streamlit.app/?utm_source=chatgpt.com)

---

# 🚀 Features

| Feature | Description |
|---|---|
| 📤 Resume Upload | Upload PDF resumes with automatic text extraction |
| 🔍 ATS Scoring | Analyze resume compatibility with job descriptions |
| ✅ Skill Matching | Detect matched and missing skills |
| 📈 AI Suggestions | Generate actionable resume improvements |
| 🎤 Interview Questions | AI-generated interview preparation questions |
| 💬 Resume Q&A | Ask questions about the resume using RAG |
| 🧠 Semantic Search | ChromaDB vector similarity retrieval |
| 📝 Resume Summary | AI-generated professional summary |

---

# 🏗️ Tech Stack

- Frontend: Streamlit
- LLM: Groq API + Llama 3.1
- Embeddings: Sentence Transformers
- Vector Database: ChromaDB
- Text Splitting: LangChain
- PDF Parsing: pypdf
- Environment Management: uv

---

# 🔄 RAG Workflow

```text
PDF Resume
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB Vector Store
    ↓
Similarity Retrieval
    ↓
Groq Llama 3.1
    ↓
Final AI Response
```

---

# 📁 Project Structure

```text
resume-rag/
│
├── app.py
├── requirements.txt
├── pyproject.toml
├── .env.example
├── README.md
│
├── data/
├── chroma_db/
├── assets/
│
└── src/
    │
    ├── __init__.py
    ├── ats.py
    ├── config.py
    ├── embeddings.py
    ├── llm.py
    ├── prompts.py
    ├── rag_pipeline.py
    ├── resume_parser.py
    ├── skill_matcher.py
    ├── utils.py
    │
    └── ui/
        ├── __init__.py
        └── components.py
```

---

# ⚙️ Installation

## Prerequisites

- Python 3.10+
- uv package manager
- Groq API key

Install uv:

[uv Documentation](https://docs.astral.sh/uv/?utm_source=chatgpt.com)

---

# 📦 Setup Using uv

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-rag-analyzer.git

cd resume-rag-analyzer
```

---

## 2. Create Virtual Environment

```bash
uv venv
```

---

## 3. Activate Environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 4. Install Dependencies

```bash
uv sync
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Get free API key from:

[Groq Console](https://console.groq.com/?utm_source=chatgpt.com)

---

# ▶️ Run Application Locally

```bash
uv run streamlit run app.py
```

Application runs at:

```text
http://localhost:8501
```

---

# 📖 How To Use

## 1. Upload Resume
Upload a PDF resume from the sidebar.

## 2. Paste Job Description
Paste the target job description.

## 3. Analyze Resume
Click:

```text
🚀 Analyze Resume
```

## 4. Explore Results

- ATS Score
- Resume Summary
- Matched Skills
- Missing Skills
- Improvement Suggestions
- Interview Questions
- Resume Q&A

---

# 🖼️ Screenshots

## ATS Score Analysis

![ATS Score](assets/ats-score.png)

---

## Skill Matching

![Skill Matching](assets/skill-matching.png)

---

## Interview Questions

![Interview Questions](assets/interview-questions.png)

---

## Resume Q&A

![Resume Q&A](assets/rag-qa.png)

---

# 🔧 Configuration

Edit:

```text
src/config.py
```

Main configurable settings:

| Setting | Description |
|---|---|
| `LLM_MODEL` | Groq model name |
| `EMBEDDING_MODEL` | Sentence transformer model |
| `CHUNK_SIZE` | Text chunk size |
| `CHUNK_OVERLAP` | Chunk overlap |
| `TOP_K_RESULTS` | Number of retrieved chunks |

---

# 🧠 Current Model

```text
llama-3.1-8b-instant
```

---

# 🚧 Future Improvements

- Multi-resume comparison
- DOCX support
- PDF export reports
- Cover letter generation
- LinkedIn profile parsing
- User authentication
- Resume ranking dashboard
- Docker deployment
- FastAPI backend integration

---

# 📄 License

MIT License

---

# 🙌 Credits

Built using:
- Streamlit
- ChromaDB
- Sentence Transformers
- LangChain
- Groq API
- Llama 3.1

---

# ⭐ Support

If you found this project useful, consider giving it a star on GitHub.