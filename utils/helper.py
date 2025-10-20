import re

def find_email(text: str):
    m = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return m.group(0) if m else None

def find_phone(text: str):
    # Simple phone pattern - works for many international formats
    m = re.search(r'(\+?\d[\d\-\s]{7,}\d)', text)
    if m:
        return m.group(0)
    return None
