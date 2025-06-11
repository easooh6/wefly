from src.domain.auth.dto.request.user_auth import UserAuthRequestDTO
from src.domain.auth.dto.response.user_auth import UserAuthResponseDTO
from src.domain.auth.dto.domain.user_auth import UserAuthDTO
from src.infrastructure.db.repositories.user_crud import UserCRUD
from src.domain.auth.utils.hasher import verify_hash
from fastapi import Depends
from src.domain.auth.exceptions.hash import WrongPasswordError
from src.domain.auth.exceptions.db import UserNotFound
from src.infrastructure.auth.JWT.jwt_manager import JWTManager
from src.domain.auth.dto.domain.jwt import TokenDTO
from src.infrastructure.db.repositories.refresh_crud import RefreshTokenCRUD
from src.domain.auth.dto.domain.refresh import RefreshTokenDTO
from src.infrastructure.db.models.refresh_model import RefreshToken
from ..utils.hasher import hash_token
from datetime import datetime, timedelta
from src.infrastructure.auth.JWT.jwt_settings import jwt_settings
from src.domain.auth.dto.request.logout import LogoutDTO
from src.domain.auth.exceptions.jwt import RefreshNotFoundError
import logging

logger = logging.getLogger("wefly.auth")


class AuthUser:

    def __init__(self, db_user: UserCRUD = Depends(),
                  jwt_manager: JWTManager = Depends(),
                  db_refresh: RefreshTokenCRUD = Depends()):
        self.db_user = db_user
        self.jwt_manager = jwt_manager
        self.db_refresh = db_refresh

    async def auth_user(self, data: UserAuthRequestDTO) -> UserAuthResponseDTO:
        logger.info('Authentication attempt for %s', data.email )
        user = await self.db_user.select_user(data.email)
        if not user:
            raise UserNotFound
        if not verify_hash(data.password,user.hashed_password):
            raise WrongPasswordError
        
        access_dto = TokenDTO(user_id=user.id, email=user.email,
                              is_admin=user.is_admin, token_type= 'access')
        refresh_dto = TokenDTO(user_id=user.id, email=user.email,
                              is_admin=user.is_admin, token_type= 'refresh')
        
        access_token = self.jwt_manager.create_access_token(access_dto)
        refresh_token = self.jwt_manager.create_refresh_token(refresh_dto)

        hashed_refresh = hash_token(token=refresh_token)

        created_at = datetime.utcnow()
        expires_at = datetime.utcnow() + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        refresh_db = RefreshToken(user_id=user.id, token_hash = hashed_refresh,
                                  expires_at = expires_at, created_at = created_at)
        
        try:
            await self.db_refresh.add_refresh(refresh_db)
        except Exception as e:
            raise
        
        logger.info('Successful authentication for %s', data.email)
        return UserAuthResponseDTO(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, token: LogoutDTO) -> bool:
        hashed_result = hash_token(token.refresh_hash)
        result = await self.db_refresh.delete_refresh_by_hash(hashed_result)
        if not result:
            raise RefreshNotFoundError
        logger.info('Successful logout')
        return result



