# DocForge

DocForge is a backend project that allows authenticated users to upload document images, extract text from those images using OCR, and store both the document information and extracted text in PostgreSQL.

The project is built to practice real backend concepts instead of only basic CRUD operations. It includes authentication, database migrations, file uploads, ownership checks, OCR integration, one-to-one and one-to-many relationships, and layered backend architecture.

---

# Project Goal

The goal of DocForge is to create a document intelligence API.

A user can:

* Register an account
* Log in and receive a JWT access token
* Upload a document image
* Save the uploaded file locally
* Extract text from the uploaded image using EasyOCR
* Store extracted text in PostgreSQL
* View their uploaded documents
* View one document with its extracted text
* Delete their own documents
* Prevent other users from accessing or deleting their documents

For example, a user can upload:

* Invoice image
* Receipt image
* Handwritten note image
* Scanned document
* Screenshot containing text

The system extracts text and saves it with the document.

---

# Current Features

## Authentication

Authentication is implemented using FastAPI Users and JWT.

Users can:

* Register
* Log in
* Receive an access token
* Access protected endpoints
* View their own user information

Protected endpoints require a JWT token in the request header:

```text
Authorization: Bearer <access_token>
```

---

## Document Upload

Authenticated users can upload an image file.

When a user uploads a document:

1. The API receives the file.
2. A unique filename is generated using UUID.
3. The file is saved inside the `uploads/` folder.
4. A document record is created in PostgreSQL.
5. EasyOCR reads the image.
6. Extracted text is saved in the `document_contents` table.
7. The API returns document information.

The original filename and the generated filename are used for different purposes:

```text
Original filename:
invoice.png

Generated filename:
c4e8d4b0-6e22-4d6f-9d1f-2c3e7f7c9c8a.png
```

The original filename is stored so the user can see the actual file name.

The generated filename is used for local storage so two users cannot overwrite each other's files.

---

## OCR Text Extraction

OCR means Optical Character Recognition.

DocForge uses EasyOCR to read text from uploaded images.

Example:

```text
Uploaded image:
HELLO BOSS

Extracted text:
HELLO BOSS
```

EasyOCR runs locally on the machine.

Currently, OCR runs during the upload request. This means large images may take time before the API returns a response.

The next improvement will move OCR processing into a background task.

Future flow:

```text
User uploads document
        ↓
Document saved with status = pending
        ↓
API returns response immediately
        ↓
Background task runs OCR
        ↓
Extracted text is saved
        ↓
Document status becomes processed
```

---

# Architecture

The project follows a layered backend architecture:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL Database
```

Each layer has a separate responsibility.

## Router Layer

The router receives HTTP requests from the user.

Examples:

```text
POST /documents/upload
GET /documents/me
GET /documents/{document_id}
DELETE /documents/{document_id}
```

The router should not contain heavy business logic.

Its job is to:

* Receive request data
* Validate dependencies
* Get the authenticated user
* Call the service layer
* Return a response

---

## Service Layer

The service layer contains business logic.

Examples of business logic:

* Generate a unique filename
* Save a file in the uploads folder
* Run OCR
* Check whether a user owns a document
* Delete the physical file from storage
* Decide document status

The service layer connects routers and repositories.

---

## Repository Layer

The repository layer handles database queries only.

Examples:

* Create a document
* Get document by ID
* Get documents for a user
* Create extracted text record
* Delete document
* Update document status

The repository should not decide whether a user is allowed to delete a document. That is business logic and belongs in the service layer.

---

# Database Design

The project currently has three important tables:

```text
users
documents
document_contents
```

---

## User and Document Relationship

One user can upload multiple documents.

```text
One User
   ↓
Many Documents
```

Example:

```text
User: Ali

Documents:
- invoice.png
- receipt.png
- handwritten_note.png
```

This is a one-to-many relationship.

In the `User` model:

```python
documents: Mapped[list["Document"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan"
)
```

In the `Document` model:

```python
user = relationship(
    "User",
    back_populates="documents"
)
```

---

## Document and Extracted Content Relationship

One document has one extracted text record.

```text
One Document
   ↓
One DocumentContent
```

Example:

```text
Document:
invoice.png

DocumentContent:
"Total amount: 5000 PKR"
```

This is a one-to-one relationship.

The `document_id` is marked as unique:

```python
document_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("documents.id", ondelete="CASCADE"),
    unique=True,
)
```

`unique=True` ensures that one document cannot have multiple extracted-text records.

In the `Document` model:

```python
content: Mapped["DocumentContent"] = relationship(
    back_populates="document",
    uselist=False,
    cascade="all, delete-orphan"
)
```

`uselist=False` tells SQLAlchemy that this relationship returns one object, not a list.

---

# Project Folder Structure

```text
docforge/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   └── document_content.py
│   │
│   ├── repositories/
│   │   ├── document.py
│   │   └── docs_content.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   └── document.py
│   │
│   ├── services/
│   │   ├── document.py
│   │   └── ocr.py
│   │
│   └── main.py
│
├── uploads/
│   └── .gitkeep
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# Important Files

## `app/main.py`

This is the main entry point of the FastAPI application.

It creates the FastAPI app and includes routers.

Example:

```python
from fastapi import FastAPI

app = FastAPI()
```

The application runs with:

```bash
uvicorn app.main:app --reload
```

---

## `app/core/config.py`

This file loads environment variables from `.env`.

Important values include:

```text
DATABASE_URL
SECRET
```

The database URL is used to connect to PostgreSQL.

The secret is used for JWT authentication.

Real secrets should never be pushed to GitHub.

---

## `app/db/session.py`

This file creates the async SQLAlchemy database engine and session factory.

The session factory is used whenever the application needs to communicate with PostgreSQL.

Example concept:

```python
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)
```

---

## `app/models/user.py`

This file contains the User database model.

It is connected with FastAPI Users.

A user can own many documents.

---

## `app/models/document.py`

This file contains the Document model.

A document stores:

```text
id
filename
file_path
status
uploaded_at
user_id
```

`filename` stores the original filename.

`file_path` stores the generated local path.

`user_id` connects the document to the user who uploaded it.

---

## `app/models/document_content.py`

This file contains the extracted text model.

It stores:

```text
id
document_id
extracted_text
created_at
```

Each document can have only one extracted text record.

---

## `app/services/ocr.py`

This file contains OCR logic.

EasyOCR is initialized once:

```python
reader = easyocr.Reader(
    ["en"],
    gpu=False
)
```

Then OCR is called with the saved file path:

```python
results = reader.readtext(
    file_path,
    detail=0
)
```

The OCR result is joined into one string and stored in PostgreSQL.

---

# API Flow

## Upload Document Flow

```text
Client sends POST /documents/upload
        ↓
Router receives file and authenticated user
        ↓
DocumentService.upload_document() is called
        ↓
A unique filename is generated
        ↓
File is saved inside uploads/
        ↓
DocumentRepository.create() saves document data
        ↓
OCRService.extract_text() extracts text from image
        ↓
DocumentContentRepository.create() saves extracted text
        ↓
API returns document information
```

---

## Get One Document Flow

```text
Client sends GET /documents/{document_id}
        ↓
Router gets authenticated user
        ↓
DocumentService.get_document_details() is called
        ↓
Repository gets document from database
        ↓
Service checks ownership
        ↓
Document content is returned
```

The authenticated user dependency is required even if the router does not directly use the `user` variable.

Example:

```python
user: User = Depends(current_active_user)
```

This ensures that only logged-in users can access the endpoint.

The service layer uses the user to verify ownership.

---

## Delete Document Flow

```text
Client sends DELETE /documents/{document_id}
        ↓
Router gets authenticated user
        ↓
Service finds the document
        ↓
Service checks document.user_id == current_user.id
        ↓
Physical file is deleted from uploads/
        ↓
Document row is deleted from PostgreSQL
        ↓
Related document_contents row is deleted automatically
        ↓
Success response is returned
```

The related content row is deleted because of cascade configuration.

---

# Installation

## 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd docforge
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Create `.env`

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/docforge
SECRET=replace_this_with_a_long_random_secret
```

Do not push `.env` to GitHub.

## 5. Create PostgreSQL Database

Create a PostgreSQL database named:

```text
docforge
```

## 6. Run Database Migrations

```bash
alembic upgrade head
```

This creates the required tables.

## 7. Start the Server

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Testing Authentication in Swagger

## Register

Use the register endpoint to create a user.

Example:

```json
{
  "email": "example@gmail.com",
  "password": "strongpassword"
}
```

## Login

Use:

```text
POST /auth/jwt/login
```

Enter:

```text
username: example@gmail.com
password: strongpassword
```

The API returns an access token.

## Authorize

Click the `Authorize` button in Swagger.

For the OAuth2 password flow, enter your email and password.

Swagger calls the login endpoint and automatically stores the token.

After authorization, Swagger sends:

```text
Authorization: Bearer <token>
```

with protected requests.

---

# Technologies Used

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* SQLAlchemy Async
* Alembic
* FastAPI Users
* JWT Authentication
* EasyOCR
* PyTorch
* aiofiles
* asyncpg

---

# Current Limitation

EasyOCR is CPU-intensive.

Currently, OCR runs inside the upload request, so uploading a large image can make the user wait.

This is acceptable for the first version and helps demonstrate the full OCR flow.

The next version will use background processing so uploads return quickly.

---

# Future Improvements

* Background OCR processing using FastAPI BackgroundTasks
* Redis and Celery for scalable job queues
* PDF text extraction
* PDF page-to-image conversion
* Better handwritten text recognition
* Document search using extracted text
* Document categories
* OCR language selection
* File size validation
* File type validation
* Cloud file storage such as AWS S3 or Cloudinary
* Docker containerization
* Frontend dashboard
* Deployment to a cloud platform
* OCR confidence score
* Document processing history
* Rate limiting
* Admin dashboard

---

# Security Notes

* `.env` is ignored by Git.
* JWT tokens protect private endpoints.
* Users can only access their own documents.
* Users can only delete their own documents.
* Generated UUID filenames reduce filename collision risk.
* Uploaded files should not be trusted without validation.
* Future versions should validate file type and file size before saving files.

---

# Author

Ali Hamza

Computer Science Student
Backend Developer Learning AI Integrations
