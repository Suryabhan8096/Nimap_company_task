from __future__ import annotations

from app.rag.embeddings import generate_embeddings
from app.rag.reranker import rerank
from app.rag.vector_store import query_collection


def retrieval_pipeline(
    query: str,
    top_k: int = 5,
    initial_fetch: int = 20,
    where_filter: dict | None = None,
) -> list[dict]:
    """
    Full retrieval pipeline:
    Query -> Embedding -> Vector Search -> Top results -> Reranking -> Final results
    """
    # Step 1: Generate query embedding
    query_embedding = generate_embeddings([query])[0]

    # Step 2: Vector search (broad retrieval)
    results = query_collection(query_embedding, top_k=initial_fetch, where_filter=where_filter)

    if not results["documents"] or not results["documents"][0]:
        return []

    # Step 3: Prepare candidates
    candidates = []
    for i, doc_text in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        candidates.append({
            "text": doc_text,
            "document_id": metadata["document_id"],
            "document_title": metadata["document_title"],
            "company_name": metadata.get("company_name", ""),
            "chunk_index": metadata["chunk_index"],
            "page_number": metadata.get("page_number", 0),
            "vector_score": 1 - distance,  # cosine similarity
        })

    # Step 4: Rerank
    reranked = rerank(query, candidates, top_n=top_k)

    return reranked
