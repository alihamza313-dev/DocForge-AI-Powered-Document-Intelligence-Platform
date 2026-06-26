from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session




# async_sessionmaker creates new database sessions (it's from SQLAlchemy, not built into Python).
# async with guarantees the session is cleaned up.
# yield temporarily hands the open session to the caller and resumes later so the cleanup can happen afterward. This is why yield is commonly used in FastAPI dependency functions.

# async with AsyncSessionLocal() as session:
#     ...

# Python automatically expands it to something conceptually like:

# session = AsyncSessionLocal()

# try:
#     ...
# finally:
#     await session.close()

# So async with is mostly syntactic sugar for "create this resource and always clean it up."