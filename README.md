# Financial Document Management System with Semantic Analysis

A FastAPI-based system for managing financial documents with JWT authentication, role-based access control, and a RAG (Retrieval-Augmented Generation) pipeline for semantic search.

## Features

- **JWT Authentication** - Register/login with secure password hashing
- **Role-Based Access Control** - Admin, Analyst, Auditor, Client roles with granular permissions
- **Document Management** - Upload, retrieve, search, and delete PDF documents
- **RAG Pipeline** - PDF extraction → chunking → embedding → vector storage (ChromaDB)
- **Semantic Search** - Query → Embedding → Vector Search → Reranking → Results
- **Context Retrieval** - Get relevant document context for any query

## Project Structure

```
├── main.py                     # FastAPI app entry point
├── requirements.txt
├── .env                        # Configuration
├── app/
│   ├── config.py               # Settings (from .env)
│   ├── enums.py                # UserRole enum
│   ├── exceptions.py           # Custom exceptions
│   ├── database/
│   │   ├── base.py             # SQLAlchemy declarative base
│   │   ├── session.py          # DB engine & session
│   │   └── init_db.py          # Table creation
│   ├── models/
│   │   ├── user.py             # User model
│   │   └── document.py         # Document model
│   ├── schemas/
│   │   ├── user.py             # Auth request/response schemas
│   │   ├── document.py         # Document schemas
│   │   └── rag.py              # RAG/search schemas
│   ├── auth/
│   │   ├── router.py           # /auth endpoints
│   │   ├── service.py          # Auth business logic
│   │   ├── security.py         # JWT & password utils
│   │   └── dependencies.py     # get_current_user, require_role
│   ├── documents/
│   │   ├── router.py           # /documents endpoints
│   │   └── service.py          # Document CRUD
│   └── rag/
│       ├── router.py           # /rag endpoints
│       ├── service.py          # RAG orchestration
│       ├── extraction.py       # PDF text extraction
│       ├── chunking.py         # Text chunking
│       ├── embeddings.py       # Sentence-transformer embeddings
│       ├── vector_store.py     # ChromaDB operations
│       ├── reranker.py         # Cross-encoder reranking
│       └── pipeline.py         # Full retrieval pipeline
└── tests/
```

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and update `SECRET_KEY`:

```bash
cp .env.example .env
```

### 4. Run the server

```bash
python main.py
# or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/auth/register` | Register new user | Public |
| POST | `/auth/login` | Login, get JWT token | Public |
| GET | `/auth/me` | Get current user profile | Authenticated |
| GET | `/auth/users` | List all users | Admin |
| PUT | `/auth/users/{id}/role` | Update user role | Admin |

### Documents (`/documents`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/documents/upload` | Upload PDF document | Admin, Analyst |
| GET | `/documents/` | List all documents | Authenticated |
| GET | `/documents/search` | Search by metadata | Authenticated |
| GET | `/documents/{id}` | Get document by ID | Authenticated |
| DELETE | `/documents/{id}` | Delete document | Admin, Auditor |

### RAG - Semantic Analysis (`/rag`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/rag/index/{doc_id}` | Index document into vector DB | Admin, Analyst |
| DELETE | `/rag/index/{doc_id}` | Remove document embeddings | Admin |
| POST | `/rag/search` | Semantic search | Authenticated |
| POST | `/rag/context` | Retrieve document context | Authenticated |

## RBAC Permission Matrix

| Action | Admin | Analyst | Auditor | Client |
|--------|-------|---------|---------|--------|
| Upload document | Yes | Yes | No | No |
| Delete document | Yes | No | Yes | No |
| View/list documents | Yes | Yes | Yes | Yes |
| Index into vector DB | Yes | Yes | No | No |
| Remove embeddings | Yes | No | No | No |
| Semantic search | Yes | Yes | Yes | Yes |
| Manage users/roles | Yes | No | No | No |

## Usage Example

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"analyst@company.com","username":"analyst1","password":"securepass"}'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst1","password":"securepass"}'
# Response: {"access_token":"eyJ...","token_type":"bearer"}

# 3. Upload document (requires Admin/Analyst role)
curl -X POST http://localhost:8000/documents/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@report.pdf" \
  -F "title=Annual Report 2025" \
  -F "company_name=Acme Corp" \
  -F "document_type=annual_report"

# 4. Index document for semantic search
curl -X POST http://localhost:8000/rag/index/1 \
  -H "Authorization: Bearer <token>"

# 5. Semantic search
curl -X POST http://localhost:8000/rag/search \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"revenue growth in Q4","top_k":5}'

# 6. Get context
curl -X POST http://localhost:8000/rag/context \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query":"what are the key financial risks?","top_k":3}'
```

## Running Tests

```bash
pytest tests/ -v
```

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM (SQLite)
- **ChromaDB** - Vector database
- **sentence-transformers** - Embeddings (all-MiniLM-L6-v2) & reranking (cross-encoder/ms-marco-MiniLM-L-6-v2)
- **PyPDF2** - PDF text extraction
- **python-jose** - JWT tokens
- **passlib** - Password hashing (bcrypt)
