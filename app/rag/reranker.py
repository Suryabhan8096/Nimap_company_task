from __future__ import annotations

from sentence_transformers import CrossEncoder

from app.config import settings

_reranker: CrossEncoder | None = None


def get_reranker() -> CrossEncoder:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(settings.RERANKER_MODEL_NAME)
    return _reranker


def rerank(query: str, candidates: list[dict], top_n: int = 5) -> list[dict]:
    """Rerank candidates using cross-encoder. Each candidate has 'text' and other metadata."""
    if not candidates:
        return []

    reranker = get_reranker()
    pairs = [[query, c["text"]] for c in candidates]
    scores = reranker.predict(pairs)

    for i, candidate in enumerate(candidates):
        candidate["rerank_score"] = float(scores[i])

    ranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    return ranked[:top_n]
