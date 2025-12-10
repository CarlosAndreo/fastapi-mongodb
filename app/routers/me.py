from typing import Annotated

from core.logger import get_logger
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import ChangePassword, User
from services.auth import authenticate_user, get_current_user
from services.user import change_password

logger = get_logger(name=__name__)

me_router = APIRouter(prefix="/me", tags=["me"])


@me_router.get(
    path="",
    summary="Retrieve current user",
    description="Retrieve the current user from the database",
    status_code=status.HTTP_200_OK,
    response_description="Current user retrieved successfully",
    responses={
        status.HTTP_200_OK: {
            "description": "Current user retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "string",
                        "email": "string",
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {"example": {"detail": "Invalid credentials"}}
            },
        },
    },
    operation_id="me",
)
async def me(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Retrieve the current user from the database
    """
    logger.info(f"User {user.username} retrieved their profile")
    return user


@me_router.patch(
    path="/change-password",
    summary="Change password",
    description="Change the password of the current user",
    status_code=status.HTTP_200_OK,
    response_description="Password changed successfully",
    responses={
        status.HTTP_200_OK: {
            "description": "Password changed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "string",
                        "email": "string",
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {"example": {"detail": "Invalid credentials"}}
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred"}
                }
            },
        },
    },
    operation_id="change_password",
)
async def patch_change_password(
    current_user: Annotated[User, Depends(get_current_user)],
    passwords: ChangePassword,
) -> User:
    """
    Change the password of the current user
    """
    logger.info(f"User {current_user.username} attempting to change password")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(
        username=current_user.username, password=passwords.old_password
    )
    if not user:
        logger.warning(
            f"Password change failed for user {current_user.username}: Incorrect old password"
        )
        raise credentials_exception
    user = await change_password(user=current_user, new_password=passwords.new_password)
    if not user:
        logger.error(
            f"Failed to change password for user {current_user.username} in database"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
    logger.info(f"Password changed successfully for user {current_user.username}")
    return user
