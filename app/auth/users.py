from fastapi import Depends

from fastapi_users import FastAPIUsers

from app.auth.backend import auth_backend
from app.auth.manager import get_user_manager
from app.models.user import User

import uuid


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
# auth_backend is needed for the router generation itself, not because FastAPIUsers doesn't know it.

current_active_user = fastapi_users.current_user(
    active=True
)