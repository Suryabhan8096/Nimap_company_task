import re

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """Extract text from PDF, returning a list of {page_number, text} dicts."""
    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = _clean_text(text)
        if text.strip():
            pages.append({"page_number": i + 1, "text": text})
    return pages


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E\n]", "", text)
    return text.strip()
