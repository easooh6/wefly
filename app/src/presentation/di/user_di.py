from fastapi import Depends, HTTPException
from src.infrastructure.db.repositories.user_crud import UserCRUD
from src.domain.auth.dto.domain.jwt import TokenDTO
from src.presentation.di.auth_di import verify_access_token
from src.domain.auth.dto.response.user_profile import UserProfileDTO
import logging
from src.infrastructure.db.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger('wefly.auth.di')

async def get_user_crud(session: AsyncSession = Depends(get_db_session)) -> UserCRUD:
    return UserCRUD(session)

async def get_current_user(
    token_payload: TokenDTO = Depends(verify_access_token),
    user_crud: UserCRUD = Depends(get_user_crud)) -> UserProfileDTO:
    logger.info("Getting current user profile for user_id: %s", token_payload.user_id)

    user = await user_crud.select_user_by_id(token_payload.user_id)
    if not user:
        raise HTTPException(status_code=401, detail={"message": "User not found"})
    
    logger.info("User profile retrieved successfully: %s", user.email)
    return UserProfileDTO(id=user.id,name=user.name,email=user.email,
                          is_admin=user.is_admin)
