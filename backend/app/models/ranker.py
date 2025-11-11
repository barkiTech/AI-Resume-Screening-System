from typing import List, Dict
import numpy as np
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sentence_transformers import SentenceTransformer, util

SKILL_BANK = {
    "python","java","c++","c","javascript","typescript","node","react","angular",
    "spring","spring boot","django","flask","fastapi","rest","graphql","sql","nosql",
    "mysql","postgres","mongodb","docker","kubernetes","aws","gcp","azure","ci/cd",
    "jenkins","git","linux","pandas","numpy","scikit-learn","nlp","ml","deep learning",
    "data structures","algorithms","oop","microservices","html","css","terraform"
}

def tokenize(text: str) -> List[str]:
    # simple tokenization
    return [t for t in re.findall(r"[a-zA-Z+#\.]+", text.lower()) if t not in ENGLISH_STOP_WORDS and len(t) > 1]

def extract_keywords(text: str) -> List[str]:
    tokens = tokenize(text)
    # naive: return top unique tokens (cap at 100)
    seen = []
    for t in tokens:
      if t not in seen:
        seen.append(t)
      if len(seen) >= 100:
        break
    return seen

def extract_skills(text: str) -> List[str]:
    tx = text.lower()
    found = set()
    for s in SKILL_BANK:
        if s in tx:
            found.add(s)
    return sorted(found)

class Ranker:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 w_semantic: float = 0.35, w_keywords: float = 0.40, w_skills: float = 0.25):
        self.model = SentenceTransformer(model_name)
        self.w_sem = w_semantic
        self.w_kw = w_keywords
        self.w_sk = w_skills

    def _semantic_sim(self, job_text: str, resumes: List[Dict]) -> List[float]:
        texts = [job_text] + [r["text"] for r in resumes]
        embs = self.model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)
        job_vec = embs[0]
        res_vecs = embs[1:]
        sims = util.cos_sim(job_vec, res_vecs).cpu().numpy().flatten().tolist()
        # map from [-1,1] -> [0,1]
        sims = [(s + 1.0) / 2.0 for s in sims]
        return sims

    def _keyword_score(self, job_text: str, resume_text: str) -> float:
        job_kw = set(extract_keywords(job_text))
        res_tokens = set(tokenize(resume_text))
        if not job_kw:
            return 0.0
        overlap = len(job_kw & res_tokens)
        return overlap / len(job_kw)

    def _skill_score(self, job_text: str, resume_text: str) -> float:
        job_sk = set(extract_skills(job_text))
        res_sk = set(extract_skills(resume_text))
        if not job_sk:
            # fallback: reward any skills present
            return min(len(res_sk) / 10.0, 1.0)
        if not res_sk:
            return 0.0
        return len(job_sk & res_sk) / len(job_sk)

    def rank(self, job_text: str, resumes: List[Dict]) -> List[Dict]:
        sem_sims = self._semantic_sim(job_text, resumes)
        out = []
        for i, r in enumerate(resumes):
            kw = self._keyword_score(job_text, r["text"])
            sk = self._skill_score(job_text, r["text"])
            sem = sem_sims[i]
            score = self.w_sem * sem + self.w_kw * kw + self.w_sk * sk
            out.append({
                "id": r["id"],
                "score": float(round(score, 4)),
                "subscores": {"semantic": float(round(sem, 4)),
                              "keywords": float(round(kw, 4)),
                              "skills": float(round(sk, 4))}
            })
        out.sort(key=lambda x: x["score"], reverse=True)
        return out
