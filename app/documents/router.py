from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.documents.service import (
    create_document,
    delete_document,
    get_document,
    list_documents,
    save_uploaded_file,
    search_documents,
)
from app.enums import UserRole
from app.models.user import User
from app.schemas.document import DocumentListResponse, DocumentRead, DocumentUploadResponse

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: str = Form(None),
    company_name: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.ANALYST)),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")

    filename, file_path = save_uploaded_file(content, file.filename)
    doc = create_document(
        db=db,
        title=title,
        filename=filename,
        original_name=file.filename,
        file_path=file_path,
        file_size=len(content),
        uploaded_by=current_user.id,
        document_type=document_type,
        company_name=company_name,
        description=description,
    )
    return DocumentUploadResponse(id=doc.id, title=doc.title, filename=doc.filename)


@router.get("/", response_model=DocumentListResponse)
def get_all_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    documents, total = list_documents(db, skip, limit)
    return DocumentListResponse(total=total, documents=documents)


@router.get("/search", response_model=list[DocumentRead])
def search_docs(
    title: str = Query(None),
    company_name: str = Query(None),
    document_type: str = Query(None),
    uploaded_by: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_documents(db, title, company_name, document_type, uploaded_by)


@router.get("/{doc_id}", response_model=DocumentRead)
def get_document_by_id(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc = get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{doc_id}", status_code=status.HTTP_200_OK)
def delete_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.AUDITOR)),
):
    if not delete_document(db, doc_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": f"Document {doc_id} deleted successfully"}
