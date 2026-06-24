import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.auth.db import get_user_db
from app.core.config import settings
from app.models.user import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):

    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)  #injects the user database into the manager.
  

# The manager handles the logic.
#while
# The database adapter(which is sqlalchemy user database we introduce in the db.py which take our database session and table user to perform database queries by providing us functions like create() ,get_by_email().. etc) handles the storage.

# Inshort we can say that
# UserManager is the business-logic layer of FastAPI Users. It uses SQLAlchemyUserDatabase to access the User table, manages users through built-in methods (create, update, reset password, verify email, etc.), and can be customized with hooks and token settings. UUIDIDMixin and BaseUserManager[User, uuid.UUID] tell FastAPI Users that it manages the User model whose primary key type is UUID.

# Remember:
# get_db()

# gave us:

# Database session

# and:

# get_user_db()

# gave us:

# SQLAlchemyUserDatabase

# Now:

# get_user_manager()

# creates:

# UserManager