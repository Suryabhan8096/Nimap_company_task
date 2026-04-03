from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLITE_URL: str = "sqlite:///./financial_docs.db"
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    UPLOAD_DIR: str = "./uploads"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
