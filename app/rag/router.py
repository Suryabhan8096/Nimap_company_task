from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.enums import UserRole
from app.models.user import User
from app.rag.service import index_document, remove_document_embeddings, retrieve_context, semantic_search
from app.schemas.rag import (
    ContextRequest,
    ContextResponse,
    IndexResponse,
    SearchQuery,
    SearchResultItem,
    SemanticSearchResponse,
)

router = APIRouter(prefix="/rag", tags=["RAG - Semantic Analysis"])


@router.post("/index/{doc_id}", response_model=IndexResponse)
def index_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.ANALYST)),
):
    try:
        chunks_count = index_document(db, doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")
    return IndexResponse(document_id=doc_id, chunks_indexed=chunks_count)


@router.delete("/index/{doc_id}")
def remove_index(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    try:
        remove_document_embeddings(db, doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Embeddings for document {doc_id} removed"}


@router.post("/search", response_model=SemanticSearchResponse)
def search(
    search_query: SearchQuery,
    current_user: User = Depends(get_current_user),
):
    where_filter = {}
    if search_query.document_type:
        where_filter["document_type"] = search_query.document_type
    if search_query.company_name:
        where_filter["company_name"] = search_query.company_name

    results = semantic_search(
        query=search_query.query,
        top_k=search_query.top_k,
        where_filter=where_filter if where_filter else None,
    )

    items = [
        SearchResultItem(
            chunk_text=r["text"],
            document_id=r["document_id"],
            document_title=r["document_title"],
            company_name=r.get("company_name"),
            chunk_index=r["chunk_index"],
            score=r.get("rerank_score", r.get("vector_score", 0)),
        )
        for r in results
    ]

    return SemanticSearchResponse(query=search_query.query, results=items, total_results=len(items))


@router.post("/context", response_model=ContextResponse)
def get_context(
    request: ContextRequest,
    current_user: User = Depends(get_current_user),
):
    result = retrieve_context(
        query=request.query,
        top_k=request.top_k,
        document_id=request.document_id,
    )
    return ContextResponse(
        query=request.query,
        context=result["context"],
        sources=result["sources"],
    )
