from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.models.ranker import Ranker
from app.utils.parser import parse_document_base64
from app.utils.sanitize import sanitize_text

app = FastAPI(title="AI Resume Screening API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ranker = Ranker()

class ResumeItem(BaseModel):
    id: str
    text: str

class RankRequest(BaseModel):
    job_text: str = Field(..., description="Job description text")
    resumes: List[ResumeItem]

class RankResponseItem(BaseModel):
    id: str
    score: float
    subscores: Dict[str, float]

class RankResponse(BaseModel):
    ranked: List[RankResponseItem]

class ParseRequest(BaseModel):
    content_base64: str

class ParseResponse(BaseModel):
    text: str

@app.post("/rank", response_model=RankResponse)
def rank_resumes(req: RankRequest):
    job_text = sanitize_text(req.job_text)
    resumes = [{"id": r.id, "text": sanitize_text(r.text)} for r in req.resumes]
    results = ranker.rank(job_text, resumes)
    return {"ranked": results}

@app.post("/parse", response_model=ParseResponse)
def parse_resume(req: ParseRequest):
    text = parse_document_base64(req.content_base64)
    return {"text": sanitize_text(text)}
