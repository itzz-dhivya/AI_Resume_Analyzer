import fitz  # PyMuPDF
import docx
import os

def extract_text(file_path: str) -> str:
    """
    Extract text from PDF or DOCX. Returns cleaned text (single string).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        # Use PyMuPDF
        with fitz.open(file_path) as doc:
            for page in doc:
                txt = page.get_text("text")
                if txt:
                    text += txt + "\n"
    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    else:
        raise ValueError("Unsupported file format. Only .pdf and .docx allowed")

    # Normalize whitespace
    text = " ".join(text.split())
    return text
