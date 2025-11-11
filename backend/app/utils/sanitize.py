import re

# Very basic scrubbing to avoid using protected attributes in scoring.
# Note: This does not guarantee legal compliance; consult counsel for production use.
SENSITIVE_PATTERNS = [
    r"\bage\b\s*[:\-]?\s*\d+",
    r"\bdob\b[:\-]?\s*\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}",
    r"\b(male|female|gender|married|single)\b",
    r"\breligion\b[:\-]?\s*[a-zA-Z]+",
    r"\bnationality\b[:\-]?\s*[a-zA-Z]+"
]

def sanitize_text(text: str) -> str:
    out = text
    for pat in SENSITIVE_PATTERNS:
        out = re.sub(pat, "[REDACTED]", out, flags=re.IGNORECASE)
    return out
