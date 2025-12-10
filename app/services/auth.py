from typing import Annotated

from core.constants import API_PREFIX
from core.jwt import decode_access_token
from core.security import verify_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from schemas.user import User, UserInDB

from services.user import get_user, get_user_in_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{API_PREFIX}/auth/login",
    scheme_name="oauth2_scheme",
    description="User authentication",
    refreshUrl=f"{API_PREFIX}/auth/refresh",
)


async def authenticate_user(username: str, password: str) -> UserInDB | None:
    """
    Authenticate a user with the given username and password
    """
    user = await get_user_in_db(username=username)
    if not user:
        return None
    if not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        return None
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User | None:
    """
    Get the current user from the token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token=token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=username)
    if user is None:
        raise credentials_exception
    return user
