from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.document import Document
from app.rag.chunking import split_text_into_chunks
from app.rag.embeddings import generate_embeddings
from app.rag.extraction import extract_text_from_pdf
from app.rag.pipeline import retrieval_pipeline
from app.rag.vector_store import add_documents, delete_documents


def index_document(db: Session, doc_id: int) -> int:
    """Extract, chunk, embed, and store a document in the vector DB. Returns chunk count."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise ValueError(f"Document {doc_id} not found")

    # Extract text from PDF
    pages = extract_text_from_pdf(doc.file_path)
    if not pages:
        raise ValueError("No text could be extracted from the PDF")

    # Split into chunks
    chunks = split_text_into_chunks(pages)
    if not chunks:
        raise ValueError("No chunks generated from the document")

    # Generate embeddings
    texts = [c["text"] for c in chunks]
    embeddings = generate_embeddings(texts)

    # Store in vector DB
    count = add_documents(
        doc_id=doc.id,
        chunks=chunks,
        embeddings=embeddings,
        doc_title=doc.title,
        company_name=doc.company_name,
    )

    # Mark as indexed
    doc.is_indexed = True
    db.commit()

    return count


def remove_document_embeddings(db: Session, doc_id: int) -> None:
    """Remove all embeddings for a document from the vector DB."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise ValueError(f"Document {doc_id} not found")

    delete_documents(doc_id)

    doc.is_indexed = False
    db.commit()


def semantic_search(query: str, top_k: int = 5, where_filter: dict | None = None) -> list[dict]:
    """Perform semantic search using the full retrieval pipeline."""
    return retrieval_pipeline(query, top_k=top_k, where_filter=where_filter)


def retrieve_context(query: str, top_k: int = 5, document_id: int | None = None) -> dict:
    """Retrieve context for a query, optionally scoped to a specific document."""
    where_filter = None
    if document_id:
        where_filter = {"document_id": document_id}

    results = retrieval_pipeline(query, top_k=top_k, where_filter=where_filter)

    context_parts = []
    sources = []
    for r in results:
        context_parts.append(r["text"])
        sources.append({
            "document_id": r["document_id"],
            "document_title": r["document_title"],
            "page_number": r.get("page_number", 0),
            "chunk_index": r["chunk_index"],
            "score": r.get("rerank_score", r.get("vector_score", 0)),
        })

    return {
        "context": "\n\n---\n\n".join(context_parts),
        "sources": sources,
    }
