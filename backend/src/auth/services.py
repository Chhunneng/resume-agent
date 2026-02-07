"""Authentication business logic."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from src.datetime.utils import get_current_utc_datetime

from .jwt import TokenType, create_access_token, create_refresh_token, verify_token
from .models import Role, User
from .password import hash_password
from .schemas import LoginRequest, RegisterRequest, TokenResponse
from .validators import validate_user_for_auth


async def get_default_roles(session: AsyncSession) -> list[Role]:
    """
    Get default roles from database.

    Args:
        session: Database session.

    Returns:
        List of default roles.
    """
    result = await session.exec(select(Role).where(Role.is_default == True))
    return list(result.scalars().all())


def generate_user_tokens(user: User) -> TokenResponse:
    """
    Generate access and refresh tokens for a user.

    Args:
        user: User model instance with roles loaded.

    Returns:
        Token response with access and refresh tokens.
    """
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        roles=user.get_role_names(),
    )
    refresh_token = create_refresh_token(
        user_id=user.id,
        email=user.email,
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


async def register_user(
    session: AsyncSession,
    request: RegisterRequest,
) -> TokenResponse:
    """
    Register a new user and return tokens.

    Args:
        session: Database session.
        request: Registration request data.

    Returns:
        Token response with access and refresh tokens.

    Raises:
        HTTPException: If email already registered.
    """
    result = await session.exec(select(User).where(User.email == request.email))
    existing_user: User | None = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    password_hash = hash_password(request.password)
    default_roles = await get_default_roles(session)

    new_user = User(
        **request.model_dump(exclude={"password"}),
        password_hash=password_hash,
        roles=default_roles,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    result = await session.exec(
        select(User).where(User.id == new_user.id).options(selectinload(User.roles)),
    )
    user_with_roles = result.scalars().one()
    return generate_user_tokens(user_with_roles)


async def login_user(
    session: AsyncSession,
    request: LoginRequest,
) -> TokenResponse:
    """
    Authenticate user and return tokens.

    Args:
        session: Database session.
        request: Login request data.

    Returns:
        Token response with access and refresh tokens.

    Raises:
        HTTPException: If email/password invalid or user inactive.
    """
    result = await session.exec(
        select(User).where(User.email == request.email).options(selectinload(User.roles)),
    )
    user = result.scalar_one_or_none()
    validate_user_for_auth(user, request.password)

    user.last_login = get_current_utc_datetime().replace(tzinfo=None)
    await session.commit()

    return generate_user_tokens(user)


async def refresh_tokens(
    session: AsyncSession,
    refresh_token: str,
) -> TokenResponse:
    """
    Issue new access and refresh tokens using a valid refresh token.

    Args:
        session: Database session.
        refresh_token: Valid refresh token string.

    Returns:
        Token response with new access and refresh tokens.

    Raises:
        HTTPException: If refresh token invalid or user not found/inactive.
    """
    try:
        payload = verify_token(refresh_token, token_type=TokenType.REFRESH)
        user_id = int(payload.get("sub"))
    except (ValueError, KeyError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        ) from e

    result = await session.exec(
        select(User).where(User.id == user_id).options(selectinload(User.roles)),
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    validate_user_for_auth(user)
    return generate_user_tokens(user)
