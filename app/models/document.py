from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), default="application/pdf")
    document_type = Column(String(100), nullable=True)
    company_name = Column(String(255), nullable=True)
    description = Column(String(1000), nullable=True)
    is_indexed = Column(Boolean, default=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
