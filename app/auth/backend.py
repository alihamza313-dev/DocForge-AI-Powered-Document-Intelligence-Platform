import uuid

from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.core.config import settings


bearer_transport = BearerTransport(
    tokenUrl="auth/jwt/login"
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=3600,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Question:
# so inshort bearer transport is basically for to get the token from the authorization header so that it can be used later for authnetication and authirization for each request to validate tha user and expiry time
# and  jwt startegy is used to create access token when user login uses secret key and expiry time for token and moreover later for decode the token only but in manually for creating token i pass from the login ebdpoint to this function email as a paramter in a dictionary like sub : email then it add the expiry time in it and create the access token but i do not see anything here in the parameter 
# and finally the authentiation backend is used for manage the whole system means when ever user send request it then transport bearer use to acces the tokem from the header and also the to get the current user from use the function of jwt startegy that decode the token and give the user back then what it handle is it also handle all the end points like register , login and me let me explain

# Answer:
# BearerTransport
# ---------------
# Defines where JWT token comes from.
# Usually Authorization: Bearer <token>

# JWTStrategy
# -----------
# Creates JWT token.
# Decodes JWT token.
# Verifies signature.
# Checks expiration.

# AuthenticationBackend
# ---------------------
# Connects Transport and Strategy.

# Authentication Flow:
# 1. Get token from request.
# 2. Validate token.
# 3. Extract user id from token.
# 4. Load user from database.

# It does NOT create login/register endpoints.
# Endpoints are created by FastAPI Users routers.