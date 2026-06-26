from app.db.session import AsyncSessionLocal
from app.repositories.document import DocumentRepository
from app.repositories.docs_content import DocumentContentRepository
from app.services.ocr import OCRService


class DocumentProcessorService:

    @staticmethod
    async def process_document(
        document_id,
        file_path: str,
    ) -> None:
        async with AsyncSessionLocal() as db:
            try:
                document = await DocumentRepository.get_by_id(
                    db=db,
                    document_id=document_id,
                )

                if not document:
                    return

                await DocumentRepository.update_status(
                    db=db,
                    document=document,
                    status="processing",
                )

                extracted_text = await OCRService.extract_text(file_path)

                await DocumentContentRepository.create(
                    db=db,
                    document_id=document.id,
                    extracted_text=extracted_text,
                )

                await DocumentRepository.update_status(
                    db=db,
                    document=document,
                    status="processed",
                )

            except Exception:
                document = await DocumentRepository.get_by_id(
                    db=db,
                    document_id=document_id,
                )

                if document:
                    await DocumentRepository.update_status(
                        db=db,
                        document=document,
                        status="failed",
                    )