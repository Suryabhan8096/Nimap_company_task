from __future__ import annotations

from app.config import settings


def split_text_into_chunks(
    pages: list[dict],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[dict]:
    """Split page texts into overlapping chunks with metadata."""
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    chunks = []
    chunk_index = 0

    for page_info in pages:
        text = page_info["text"]
        page_number = page_info["page_number"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "chunk_index": chunk_index,
                    "text": chunk_text.strip(),
                    "page_number": page_number,
                })
                chunk_index += 1

            start += chunk_size - chunk_overlap

    return chunks
