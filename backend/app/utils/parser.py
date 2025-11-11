import base64, io
from typing import Optional
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

def parse_document_base64(content_base64: str) -> str:
    raw = base64.b64decode(content_base64)
    # Try PDF first
    try:
        text = pdf_extract_text(io.BytesIO(raw))
        if text and len(text.strip()) > 0:
            return text
    except Exception:
        pass
    # Try DOCX
    try:
        with io.BytesIO(raw) as buf:
            doc = Document(buf)
            return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        pass
    # Fallback to plain text
    try:
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return ""
