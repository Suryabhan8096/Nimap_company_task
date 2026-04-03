from fastapi import HTTPException, status


class DocumentNotFound(HTTPException):
    def __init__(self, doc_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document {doc_id} not found")


class Unauthorized(HTTPException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class IndexingError(HTTPException):
    def __init__(self, detail: str = "Indexing failed"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class EmbeddingError(HTTPException):
    def __init__(self, detail: str = "Embedding generation failed"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
