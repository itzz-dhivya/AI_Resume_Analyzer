import spacy
import re
from utils.text_cleaner import clean_text
from utils.helper import find_email, find_phone

# load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    raise RuntimeError("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm") from e

# a small expandable skills list
DEFAULT_SKILLS = [
    "python", "java", "c++", "sql", "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "django", "flask",
    "excel", "power bi", "tableau", "nlp", "aws", "azure", "git", "docker", "kubernetes"
]

EDU_KEYWORDS = ["b.tech", "b.e", "m.tech", "mba", "b.sc", "m.sc", "phd", "bachelor", "master", "degree"]

def parse_resume(text: str) -> dict:
    """
    Returns a dictionary with keys: Name, Email, Phone, Skills (list), Education (list), Experience (years or str)
    """
    raw = clean_text(text)
    doc = nlp(raw)

    out = {"Name": None, "Email": None, "Phone": None, "Skills": [], "Education": [], "Experience": None}

    # email and phone
    out["Email"] = find_email(raw) or "Not found"
    out["Phone"] = find_phone(raw) or "Not found"

    # Name: first PERSON entity with heuristics
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            # avoid picking short tokens like "CV"
            if len(name.split()) <= 4 and len(name) > 1:
                out["Name"] = name
                break

    # Education detection
    low = raw.lower()
    edus = set()
    for kw in EDU_KEYWORDS:
        if kw in low:
            # Capture surrounding phrase (simple)
            m = re.search(r'([A-Z][\w &,-]{0,60}'+ re.escape(kw) + r'[^\.\n]{0,60})', raw, flags=re.IGNORECASE)
            if m:
                edus.add(m.group(0).strip())
            else:
                edus.add(kw)
    out["Education"] = list(edus) if edus else []

    # Experience detection (years)
    m = re.search(r'(\d+)\s*\+?\s*(?:years|yrs|year|yr)', raw, flags=re.IGNORECASE)
    out["Experience"] = m.group(0) if m else "Not found"

    # Skills: keyword matching (case-insensitive). Expandable.
    found = []
    for skill in DEFAULT_SKILLS:
        if skill.lower() in low:
            found.append(skill.title())
    out["Skills"] = sorted(list(set(found)))

    return out
