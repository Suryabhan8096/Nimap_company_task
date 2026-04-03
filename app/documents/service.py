from __future__ import annotations

import os
import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import settings
from app.models.document import Document


def save_uploaded_file(file_content: bytes, original_name: str) -> tuple[str, str]:
    """Save file to disk. Returns (unique_filename, file_path)."""
    ext = os.path.splitext(original_name)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return unique_name, file_path


def create_document(
    db: Session,
    title: str,
    filename: str,
    original_name: str,
    file_path: str,
    file_size: int,
    uploaded_by: int,
    document_type: str | None = None,
    company_name: str | None = None,
    description: str | None = None,
) -> Document:
    doc = Document(
        title=title,
        filename=filename,
        original_name=original_name,
        file_path=file_path,
        file_size=file_size,
        uploaded_by=uploaded_by,
        document_type=document_type,
        company_name=company_name,
        description=description,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_document(db: Session, doc_id: int) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id).first()


def list_documents(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[Document], int]:
    query = db.query(Document)
    total = query.count()
    documents = query.offset(skip).limit(limit).all()
    return documents, total


def delete_document(db: Session, doc_id: int) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        return False
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    db.delete(doc)
    db.commit()
    return True


def search_documents(
    db: Session,
    title: str | None = None,
    company_name: str | None = None,
    document_type: str | None = None,
    uploaded_by: int | None = None,
) -> list[Document]:
    query = db.query(Document)
    if title:
        query = query.filter(Document.title.ilike(f"%{title}%"))
    if company_name:
        query = query.filter(Document.company_name.ilike(f"%{company_name}%"))
    if document_type:
        query = query.filter(Document.document_type.ilike(f"%{document_type}%"))
    if uploaded_by:
        query = query.filter(Document.uploaded_by == uploaded_by)
    return query.all()
