from src.infrastructure.db.models.refresh_model import RefreshToken
from src.infrastructure.db.models.user_model import User
from src.infrastructure.db.db import get_db_session
from sqlalchemy import select, update, delete
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import and_

class RefreshTokenCRUD:

    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db
    
    async def add_refresh(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        await self.db.flush()
        return token
    
    async def delete_refresh_by_hash(self, token_hash: str) -> bool:
        query = delete(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.db.execute(query)
        return result.rowcount > 0
    
    async def select_refresh_by_hash(self, token_hash: str):
        query = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def select_refresh_tokens_by_user(self, user_id: int) -> list[RefreshToken]:
        query = select(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_all_user_tokens(self, user_id: int) -> int:
        query = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self.db.execute(query)
        return result.rowcount

