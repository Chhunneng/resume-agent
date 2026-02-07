"""Authentication API routes."""

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.connection import get_db_session

from . import services
from .dependencies import get_current_active_user
from .models import User
from .schemas import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account and return authentication tokens.",
)
async def register(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """
    Register a new user.

    Creates a new user account with the provided information and returns
    JWT access and refresh tokens. Assigns default roles to the new user.
    """
    return await services.register_user(session, request)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate user and return authentication tokens.",
)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """
    Login user.

    Authenticates a user with email and password, then returns
    JWT access and refresh tokens.
    """
    return await services.login_user(session, request)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh tokens",
    description="Generate new access and refresh tokens using a valid refresh token.",
)
async def refresh_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """
    Refresh tokens.

    Generates new access and refresh tokens using a valid refresh token.
    """
    return await services.refresh_tokens(session, request.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the current authenticated user's information.",
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Get current user information.

    Returns the information of the currently authenticated user.
    """
    return UserResponse.from_user(current_user)
