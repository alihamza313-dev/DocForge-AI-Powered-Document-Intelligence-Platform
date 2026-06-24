from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


# FastAPI Users does not magically know:

# your database session
# your User model
# your table name
# how to query users

# So you give it this:

# SQLAlchemyUserDatabase(session, User)