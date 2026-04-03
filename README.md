Financial Document Management System

This project is a backend application built using FastAPI. It is used to manage financial documents and perform smart search using basic AI concepts.

The system allows users to register, login, upload documents, and search information from those documents.

Features
User registration and login using JWT authentication
Role-based access like Admin, Analyst, Auditor, and Client
Upload and manage PDF documents
Search documents using keywords
Semantic search using RAG concept
Retrieve relevant content from documents
Technologies Used
FastAPI for backend
SQLAlchemy for database handling
SQLite as database
ChromaDB for vector storage
Sentence Transformers for embeddings
PyPDF2 for reading PDF files
JWT for authentication
Project Structure

main.py – Entry point

app folder contains:

auth – user login and authentication
documents – document upload and management
rag – search and AI logic
models – database models
schemas – API request and response
database – database connection
How to Run

Step 1: Create virtual environment
python -m venv venv
venv\Scripts\activate

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Run project
uvicorn main:app --reload

Open in browser:
http://localhost:8000/docs

User Roles

Admin – full access
Analyst – upload and search documents
Auditor – view and delete documents
Client – view and search only

How It Works

User uploads a PDF file
System reads the PDF and extracts text
Text is divided into smaller parts
These parts are converted into embeddings
Stored in vector database
When user searches, similar content is returned
