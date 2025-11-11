# AI-Powered Resume Screening System (Starter)

This repo is a **production-minded starter** for building an AI-assisted resume screening tool.
It includes:
- A FastAPI backend for parsing resumes, embedding them, and ranking against a job description.
- A lightweight, framework-free frontend for uploading resumes and viewing ranked results.
- A simple, transparent ranking pipeline: **keyword coverage** + **skill matching** + **semantic similarity** (Sentence Transformers).
- A small sample dataset and unit tests.

> ⚠️ Ethics & Compliance: Avoid using protected attributes (age, gender, race, religion, etc.) in scoring. This starter includes guards to drop sensitive features. Always comply with local employment laws.

## Quickstart

### 1) Python env
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run the API
```bash
uvicorn app.main:app --reload --port 8000
```

### 3) Open the UI
Just open `frontend/index.html` in your browser (or serve it with any static server).
The UI expects the API at `http://localhost:8000`.

## Endpoints

- `POST /rank` — Body:
```json
{
  "job_text": "...",
  "resumes": [
    { "id": "cv-1", "text": "..." },
    { "id": "cv-2", "text": "..." }
  ]
}
```
Response (sorted highest first):
```json
{
  "ranked": [{"id":"cv-1","score":0.82,"subscores":{"semantic":0.77,"keywords":0.9,"skills":0.8}}, ...]
}
```

- `POST /parse` — Body:
```json
{ "content_base64": "<PDF or DOCX base64>" }
```
Returns extracted text. (For demo, use the CSV samples in `data/resumes/` to skip PDFs.)

## How the Scoring Works

1. **Keyword coverage**: proportion of job keywords found in resume.
2. **Skill match**: overlap between extracted skills (from a normalised skills list) and job-required skills.
3. **Semantic similarity**: cosine similarity of embeddings between job text and resume text.
4. **Final score**: weighted blend (defaults: 0.35 semantic, 0.4 keywords, 0.25 skills).

You can tune weights in `app/models/ranker.py`.

## Notes

- Embeddings model defaults to `sentence-transformers/all-MiniLM-L6-v2` (fast, good baseline).
- Resume parsing supports **PDF** (pdfminer.six) and **DOCX** (python-docx).
- Sensitive attributes are scrubbed by a simple regex-based sanitizer in `utils/sanitize.py`.
- Add more robust skill extraction by swapping in spaCy NER or a curated ontology (e.g., ESCO, O*NET).

## Tests
Run:
```bash
pytest
```

## Roadmap Ideas
- Feedback loop: recruiters can mark relevant/irrelevant to train a reranker.
- Explanation UI: highlight matched skills/keywords in each resume.
- Fairness checks: disparate impact metrics per cohort (only on *non-protected, job-related* cohorts).
- Vector DB integration for large volumes (FAISS, Qdrant, Pinecone).
