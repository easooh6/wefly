from src.infrastructure.auth.JWT.jwt_manager import JWTManager
from src.domain.auth.exceptions.jwt import (RefreshNotFoundError, ExpiredCredentialError,
                                                       JWTServiceError, CredentialError,
                                                         InvalidPayloadError)
from src.domain.auth.dto.domain.jwt import TokenDTO
from fastapi import Depends
from ..utils.hasher import hash_token
from src.infrastructure.db.repositories.refresh_crud import RefreshTokenCRUD

class RefreshService:

    def __init__(self, jwt_manager: JWTManager = Depends(),
                 refresh_db: RefreshTokenCRUD = Depends()):
        self.jwt_manager = jwt_manager
        self.refresh_db = refresh_db

    async def refresh_access_token(self, token: str) -> str:
        hashed_token = None
        try:
            hashed_token = hash_token(token=token)
            last = await self.refresh_db.select_refresh_by_hash(hashed_token)
            if not last:
                raise RefreshNotFoundError
            new_access =self.jwt_manager.refresh_access_token(token)
            return new_access
        except (CredentialError, InvalidPayloadError, ExpiredCredentialError):
            if hashed_token:
                await self.refresh_db.delete_refresh_by_hash(hashed_token)
            raise
