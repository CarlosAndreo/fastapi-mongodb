from typing import Annotated

from core.jwt import create_access_token, create_refresh_token, verify_refresh_token
from core.logger import get_logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import RefreshToken, Token, User, UserCreate
from services.auth import authenticate_user
from services.user import create_user, get_user

logger = get_logger(name=__name__)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
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
    operation_id="register",
)
async def register(user: UserCreate) -> User:
    """
    Register a new user in the database
    """
    logger.info(f"Attempting to register user: {user.username}")
    existing_user = await get_user(username=user.username)
    if existing_user:
        logger.error(f"Registration failed: User {user.username} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    user_created = await create_user(user=user)
    if not user_created:
        logger.error(f"Failed to create user {user.username} in database")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
    logger.info(f"User {user.username} registered successfully")
    return user_created


@auth_router.post(
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
    operation_id="login",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Login to the application
    """
    logger.info(f"Login attempt for user: {form_data.username}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        logger.warning(
            f"Login failed for user: {form_data.username} - Invalid credentials"
        )
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    logger.info(f"User {user.username} logged in successfully")
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@auth_router.post(
    path="/refresh",
    summary="Refresh access token",
    description="Generate a new access token using a valid refresh token",
    status_code=status.HTTP_200_OK,
    response_description="JWT tokens generated successfully",
    responses={
        status.HTTP_200_OK: {
            "description": "JWT tokens generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "string",
                        "refresh_token": "string",
                        "token_type": "bearer",
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid or expired refresh token",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
    operation_id="refresh",
)
async def refresh(
    refresh_token_data: RefreshToken,
) -> Token:
    """
    Generate a new access token using a valid refresh token
    """
    logger.info("Attempting to refresh access token")

    payload = verify_refresh_token(token=refresh_token_data.refresh_token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not payload:
        logger.warning("Token refresh failed: Invalid refresh token")
        raise credentials_exception
    username = payload.get("sub")
    if not username:
        logger.error("Token refresh failed: Username not found in token")
        raise credentials_exception
    user = await get_user(username=username)
    if not user:
        logger.error(f"Token refresh failed: User {username} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    logger.info(f"Access token refreshed successfully for user: {user.username}")
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
