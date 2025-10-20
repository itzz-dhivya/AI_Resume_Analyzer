import re

def clean_text(text: str) -> str:
    """
    Basic cleaning: remove extra whitespace, unusual chars; keep case for names.
    """
    if not text:
        return ""
    # Replace multiple newlines/tabs/spaces with single space
    t = re.sub(r'[\r\n\t]+', ' ', text)
    t = re.sub(r'\s{2,}', ' ', t)
    t = t.strip()
    return t
