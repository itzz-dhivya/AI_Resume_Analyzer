from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def _split_skills(skill_str):
    # Accept comma-separated or newline or space-separated small list
    if not skill_str:
        return []
    parts = [s.strip() for s in skill_str.replace("\n", ",").split(",") if s.strip()]
    return parts

def match_skills_from_text(parsed_resume: dict, job_skills_input: str) -> dict:
    """
    parsed_resume: output of parse_resume()
    job_skills_input: string of skills (comma-separated)
    Returns dict: matched_skills, missing_skills, skill_match_percent
    """
    resume_skills = [s.lower() for s in parsed_resume.get("Skills", [])]
    job_skills = [s.lower() for s in _split_skills(job_skills_input)]

    if not job_skills:
        return {"matched_skills": [], "missing_skills": [], "skill_match_percent": 0}

    # Exact keyword matching
    matched = []
    for js in job_skills:
        for rs in resume_skills:
            if js == rs or js in rs or rs in js:
                matched.append(js)
                break

    matched = sorted(list(set(matched)))
    missing = [s for s in job_skills if s not in matched]

    # compute percent = matched / required * 100
    percent = int(round(len(matched) / len(job_skills) * 100)) if job_skills else 0

    # If no natural matches, apply TF-IDF semantic similarity fallback
    if percent == 0 and resume_skills:
        texts = ["; ".join(resume_skills), "; ".join(job_skills)]
        try:
            tfidf = TfidfVectorizer().fit_transform(texts)
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            percent = int(round(float(sim) * 100))
            # don't populate matched/missing in this fallback
        except Exception:
            pass

    return {"matched_skills": matched, "missing_skills": missing, "skill_match_percent": percent}
