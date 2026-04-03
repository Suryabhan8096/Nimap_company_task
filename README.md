Financial Document Management System

This project is a FastAPI-based application that helps manage financial documents and perform smart search using AI.

It includes user authentication, role-based access, document upload, and a semantic search system using a RAG pipeline.

🚀 Features
User registration and login using JWT authentication
Role-based access (Admin, Analyst, Auditor, Client)
Upload and manage PDF documents
Search documents using keywords and metadata
Semantic search using AI (RAG pipeline)
Retrieve relevant content from documents
🛠️ Technologies Used
FastAPI (Backend framework)
SQLAlchemy (Database ORM)
SQLite (Database)
ChromaDB (Vector database)
Sentence Transformers (Embeddings)
PyPDF2 (PDF processing)
JWT (Authentication)
📂 Project Structure (Simple View)
main.py             → Entry point
app/
  ├── auth/         → Login & user management
  ├── documents/    → Document upload & handling
  ├── rag/          → AI search logic
  ├── models/       → Database models
  ├── schemas/      → API schemas
  └── database/     → DB connection
⚙️ How to Run
1. Create virtual environment
python -m venv venv
venv\Scripts\activate
2. Install dependencies
pip install -r requirements.txt
3. Run project
uvicorn main:app --reload

👉 Open in browser:

Swagger UI: http://localhost:8000/docs
🔐 User Roles
Admin → Full access
Analyst → Upload & search documents
Auditor → View & delete documents
Client → Only view/search
🔍 How It Works (Simple Explanation)
User uploads a PDF document
System extracts text from PDF
Text is divided into smaller parts (chunks)
Each chunk is converted into embeddings
Stored in vector database (ChromaDB)
When user searches → similar content is retrieved
💡 Example Use Case
Upload financial reports
Search like: "revenue growth in Q4"
System returns relevant content from documents
🧪 Testing
pytest tests/
