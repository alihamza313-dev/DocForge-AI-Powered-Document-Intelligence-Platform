from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from sqlalchemy import select

# @staticmethod
# A static method belongs to the class but doesn't need an object.

# Example:
# class Math:

#     @staticmethod
#     def add(a, b):
#         return a + b

# Call it:
# Math.add(10, 20)
# No object is created.
# No self exists.

class DocumentRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        **kwargs
    ):
        document = Document(**kwargs)

        db.add(document)

        await db.commit()

        await db.refresh(document)

        return document


    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        document_id,
    ):
        result = await db.execute(
            select(Document)
            .where(Document.id == document_id)
        )

        return result.scalar_one_or_none()


    @staticmethod
    async def get_user_documents(
        db: AsyncSession,
        user_id,
    ):

        result = await db.execute(
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.uploaded_at.desc())
        )

        return result.scalars().all()
    

    @staticmethod
    async def delete(
        db: AsyncSession,
        document: Document,
    ):

        await db.delete(document)
        await db.commit()