import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass



# Now look at FastAPI Users' base schema:

# Something like:

# class BaseUser(Generic[ID]):
#     id: ID
#     email: str
#     is_active: bool
#     is_superuser: bool
#     is_verified: bool

# ID is a placeholder.

# It is saying:

# "I don't know what type your ID is. You tell me."

# Example:

# If your ID is integer:

# class UserRead(BaseUser[int]):
#     pass

# Then it becomes:

# id: int

# For your project:

# You use UUID:

# class UserRead(schemas.BaseUser[uuid.UUID]):

# so FastAPI Users understands:

# id: uuid.UUID

# Your final schema becomes conceptually:

# class UserRead:
#     id: uuid.UUID
#     email: str
#     is_active: bool
#     is_superuser: bool
#     is_verified: bool