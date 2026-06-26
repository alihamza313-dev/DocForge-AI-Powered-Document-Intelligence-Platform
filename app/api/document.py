from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.users import current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentRead,DocumentListResponse
from app.services.document import DocumentService
from uuid import UUID

from fastapi import BackgroundTasks
from app.services.document_processor import DocumentProcessorService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    document = await DocumentService.upload_document(
        file=file,
        user=user,
        db=db,
    )

    background_tasks.add_task(
        DocumentProcessorService.process_document,
        document.id,
        document.file_path,
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
        "message": "Document uploaded. OCR processing started.",
    }

# THIS route will depend upon the upload document function in the document service class whixh is present in the services folder in document.py which help to create the document detail like its filename, file path and create document object and then pass ot to another function create which is present in document.py in repositories which actually take this object and store it into the database. 
#===================

@router.get("/me")
async def get_my_documents(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):

    return await DocumentService.get_my_documents(
        user=user,
        db=db,
    )

#this router is for getting all the documents of the current user

#==========================
@router.get("/{document_id}")
async def get_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user) 
):

    return await DocumentService.get_document_details(
        document_id=document_id,
        db=db,
    )

    #user: User = Depends(current_active_user),
    #  #at this fastapi user check that jwt token and its validation or expiry and then allow to enter in this function 

    # this endpoint call the service name get_document_details() this service return the details of specific document

#===================================

@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):

    return await DocumentService.delete_document(
        document_id=document_id,
        user=user,
        db=db,
    )