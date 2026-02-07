"""LLM config API: set and list user API keys per provider."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import get_current_active_user
from src.auth.models import User
from src.database.connection import get_db_session
from src.llm import services as llm_services
from src.llm.schemas import LLMConfigListResponse, LLMConfigSetRequest

router = APIRouter(tags=["llm"])


@router.put(
    "/llm-config",
    status_code=status.HTTP_200_OK,
    summary="Set LLM API key",
    description="Store encrypted API key for a provider (openai, deepseek).",
)
async def set_llm_config(
    body: LLMConfigSetRequest,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    try:
        await llm_services.upsert_llm_config(
            session,
            user_id=current_user.id,
            provider=body.provider,
            api_key=body.api_key,
        )
        await session.commit()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return {"status": "ok", "provider": body.provider}


@router.get(
    "/llm-config",
    response_model=LLMConfigListResponse,
    summary="List LLM config status",
    description="List which providers are configured for the current user (no keys returned).",
)
async def get_llm_config(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> LLMConfigListResponse:
    configs = await llm_services.list_llm_config_status(session, user_id=current_user.id)
    return LLMConfigListResponse(configs=configs)
