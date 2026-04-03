from pydantic import BaseModel


class IndexResponse(BaseModel):
    document_id: int
    chunks_indexed: int
    message: str = "Document indexed successfully"


class SearchQuery(BaseModel):
    query: str
    top_k: int = 5
    document_type: str | None = None
    company_name: str | None = None


class SearchResultItem(BaseModel):
    chunk_text: str
    document_id: int
    document_title: str
    company_name: str | None
    chunk_index: int
    score: float


class SemanticSearchResponse(BaseModel):
    query: str
    results: list[SearchResultItem]
    total_results: int


class ContextRequest(BaseModel):
    query: str
    top_k: int = 5
    document_id: int | None = None


class ContextResponse(BaseModel):
    query: str
    context: str
    sources: list[dict]
