# AI_Resume_Parser

AI-Powered Resume Parser & Analyzer — Streamlit frontend, Python backend, MySQL support.

## Features
- Upload PDF/DOCX resumes
- Extract Name, Email, Phone, Education, Skills, Experience using spaCy + heuristics
- Compute skill match vs. a job profile (keyword and TF-IDF fallback)
- Simple weighted resume scoring
- Save parsed results locally (JSON) and optionally into MySQL

## Setup
1. Clone this repo and cd into project root.
2. Create virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
