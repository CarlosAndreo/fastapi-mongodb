from typing import Annotated

from core.jwt import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import ChangePassword, Token, User, UserCreate
from services.auth import authenticate_user, get_current_user
from services.user import change_password, create_user, get_user

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post(
    path="/register",
    summary="Register a new user",
    description="Register a new user in the database",
    status_code=status.HTTP_201_CREATED,
    response_description="User registered successfully",
    responses={
        status.HTTP_201_CREATED: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "string",
                        "email": "string",
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {"example": {"detail": "Invalid input data"}}
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
    response_model=User,
    operation_id="register_user",
)
async def register_user(user: UserCreate) -> User:
    """
    Register a new user in the database
    """
    existing_user = await get_user(username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    user = await create_user(user=user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
    return user


@user_router.post(
    path="/login",
    summary="Login to the application",
    description="Login to the application",
    status_code=status.HTTP_200_OK,
    response_description="JWT token generated successfully",
    responses={
        status.HTTP_200_OK: {
            "description": "JWT token generated successfully",
            "content": {
                "application/json": {
                    "example": {"access_token": "string", "token_type": "bearer"}
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
    response_model=Token,
    operation_id="login",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Login to the application
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.username})
    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@user_router.get(
    path="/me",
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
    response_model=User,
    operation_id="get_current_user",
)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Retrieve the current user from the database
    """
    return current_user


@user_router.patch(
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
    response_model=User,
    operation_id="change_password",
)
async def patch_change_password(
    current_user: Annotated[User, Depends(get_current_user)],
    passwords: ChangePassword,
) -> User:
    """
    Change the password of the current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(
        username=current_user.username, password=passwords.old_password
    )
    if not user:
        raise credentials_exception
    user = await change_password(user=current_user, new_password=passwords.new_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
    return user
