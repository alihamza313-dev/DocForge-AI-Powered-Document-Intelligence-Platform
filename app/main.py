# docforge/
# │
# ├── app/
# │   ├── api/
# │   ├── core/
# │   ├── db/
# │   ├── models/
# │   ├── schemas/
# │   ├── services/
# │   ├── repositories/
# │   ├── tasks/
# │   ├── templates/
# │   ├── static/
# │   └── main.py
# │
# ├── uploads/
# │
# ├── tests/
# │
# ├── alembic/
# │
# ├── requirements.txt
# │
# ├── .env
# │
# ├── .gitignore
# │
# ├── Dockerfile
# │
# └── docker-compose.yml


from fastapi import FastAPI

from app.auth.users import (
    fastapi_users,
    current_active_user
)

from app.auth.backend import auth_backend

from app.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate
)

from app.models.user import User
from app.api.document import router as document_router


app = FastAPI(title="DocForge")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate
    ),
    prefix="/users",
    tags=["users"],
)

#the upper router is for the authentication

# get_auth_router()
# -----------------
# Needs auth_backend because it creates login/logout
# and handles authentication tokens.


# get_register_router()
# --------------------
# No auth_backend because user is not authenticated yet.


# get_users_router()
# -----------------
# No auth_backend because FastAPIUsers already received
# auth_backend during initialization.

app.include_router(document_router)