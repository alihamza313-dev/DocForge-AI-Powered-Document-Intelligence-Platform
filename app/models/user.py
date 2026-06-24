import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import DateTime, func 
from sqlalchemy.orm import Mapped, mapped_column ,relationship

from app.db.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    documents = relationship(
    "Document",
    back_populates="user",
    cascade="all, delete-orphan"
)
    

# This does not connect FastAPI Users to the database.

# It only says:

# "Create a SQLAlchemy model that has the fields FastAPI Users expects."