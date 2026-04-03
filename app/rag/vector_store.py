from __future__ import annotations

import chromadb

from app.config import settings

_client: chromadb.PersistentClient | None = None
COLLECTION_NAME = "financial_documents"


def get_chroma_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    return _client


def get_collection() -> chromadb.Collection:
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_documents(
    doc_id: int,
    chunks: list[dict],
    embeddings: list[list[float]],
    doc_title: str,
    company_name: str | None,
) -> int:
    collection = get_collection()
    ids = [f"doc_{doc_id}_chunk_{c['chunk_index']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "document_id": doc_id,
            "document_title": doc_title,
            "company_name": company_name or "",
            "chunk_index": c["chunk_index"],
            "page_number": c["page_number"],
        }
        for c in chunks
    ]

    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    return len(ids)


def delete_documents(doc_id: int) -> None:
    collection = get_collection()
    results = collection.get(where={"document_id": doc_id})
    if results["ids"]:
        collection.delete(ids=results["ids"])


def query_collection(
    query_embedding: list[float],
    top_k: int = 20,
    where_filter: dict | None = None,
) -> dict:
    collection = get_collection()
    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if where_filter:
        kwargs["where"] = where_filter
    return collection.query(**kwargs)
