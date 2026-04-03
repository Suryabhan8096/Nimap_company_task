import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.auth.router import router as auth_router
from app.database.init_db import init_db
from app.documents.router import router as documents_router
from app.middleware.error_handler import register_error_handlers
from app.rag.router import router as rag_router

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")
    yield


app = FastAPI(
    title="Financial Document Management System",
    description="API for managing financial documents with semantic analysis using RAG pipeline",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

register_error_handlers(app)

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(rag_router)


@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
def frontend():
    html_path = BASE_DIR / "templates" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
