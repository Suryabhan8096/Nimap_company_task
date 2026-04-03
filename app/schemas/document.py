from datetime import datetime

from pydantic import BaseModel


class DocumentRead(BaseModel):
    id: int
    title: str
    filename: str
    original_name: str
    file_size: int
    mime_type: str
    document_type: str | None
    company_name: str | None
    description: str | None
    is_indexed: bool
    uploaded_by: int
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    id: int
    title: str
    filename: str
    message: str = "Document uploaded successfully"

    model_config = {"from_attributes": True}


class DocumentSearchQuery(BaseModel):
    title: str | None = None
    company_name: str | None = None
    document_type: str | None = None
    uploaded_by: int | None = None


class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentRead]
