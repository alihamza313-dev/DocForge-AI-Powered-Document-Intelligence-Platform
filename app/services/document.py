import os
from uuid import uuid4

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.repositories.document import DocumentRepository
from app.models.user import User

from app.services.ocr import OCRService
from app.repositories.docs_content import DocumentContentRepository

from app.schemas.document import DocumentDetailResponse,DocumentListResponse

from fastapi import HTTPException
import os


class DocumentService:

    @staticmethod
    async def upload_document(
        file: UploadFile,
        user: User,
        db: AsyncSession,
    ) -> Document:

        # Create uploads folder if it doesn't exist
        os.makedirs("uploads", exist_ok=True)

        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4()}{file_ext}"

        # Full path
        file_path = os.path.join("uploads", unique_filename)

        # Save file
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        # Create database record
        document = await DocumentRepository.create(
            db=db,
            filename=file.filename,      # original name
            file_path=file_path,         # saved path
            status="processed",
            user_id=user.id,
        )

        extracted_text = await OCRService.extract_text(file_path)
        print(type(extracted_text))
        print(extracted_text)
        await DocumentContentRepository.create(
            db = db,
            document_id = document.id,
            extracted_text = extracted_text
        )

        return document
    
#=============================
    @staticmethod
    async def get_document(
        document_id,
        db: AsyncSession,
    ):

        document = await DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )

        if not document:
            return None

        return document
    
#=============================
    @staticmethod
    async def get_document_details(
        document_id,
        db: AsyncSession,
    )->DocumentDetailResponse:

        document = await DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )
        #get_by_id function in repsositories check in database about the document of the specific id and return it if it exist and return none if not

        if not document:
            return None

        content = await DocumentContentRepository.get_by_document_id(
            db=db,
            document_id=document.id,
        )

        #this function get the document_contents from comtent table by calling the repository name get_document_by_id

        return {
            "id": document.id,
            "filename": document.filename,
            "status": document.status,
            "uploaded_at": document.uploaded_at,
            "extracted_text": (
                content.extracted_text
                if content
                else ""
            ),
        }
    
#===============================
    @staticmethod
    async def get_my_documents(
        user: User,
        db: AsyncSession,
    )->DocumentListResponse:

        documents = await DocumentRepository.get_user_documents(
            db=db,
            user_id=user.id,
        )

        return [
            {
                "id": doc.id,
                "filename": doc.filename,
                "status": doc.status,
                "uploaded_at": doc.uploaded_at,
            }
            for doc in documents
        ]
    
#===========================

# This is an async static method that deletes a document, but only if:

# The document exists.
# The logged-in user owns the document.
# The file exists on disk.

    @staticmethod
    async def delete_document(
        document_id,
        user: User,
        db: AsyncSession,
    ):

        document = await DocumentRepository.get_by_id(
            db=db,
            document_id=document_id,
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

    #The following condition ensures the authorization by checking that  even if document exist, is it also related to the person or user that are requesting to delete it if yes then delete it otherwise raise an error.
        if document.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        await DocumentRepository.delete(
            db=db,
            document=document,
        )

        return {
            "message": "Document deleted successfully"
        }