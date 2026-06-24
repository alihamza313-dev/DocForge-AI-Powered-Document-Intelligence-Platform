from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DocumentContent
from sqlalchemy import select


class DocumentContentRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        document_id,
        extracted_text: str,
    ) -> DocumentContent:

        content = DocumentContent(
            document_id=document_id,
            extracted_text=extracted_text,
        )

        db.add(content)

        await db.commit()
        await db.refresh(content)

        return content
    


    @staticmethod
    async def get_by_document_id(
        db: AsyncSession,
        document_id,
    ):
        result = await db.execute(
            select(DocumentContent)
            .where(
                DocumentContent.document_id == document_id
            )
        )

        return result.scalar_one_or_none()