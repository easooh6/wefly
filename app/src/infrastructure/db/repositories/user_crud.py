from src.infrastructure.db.models.user_model import User
from src.infrastructure.db.db import get_db_session
from sqlalchemy import select, update, delete
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
class UserCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user
    
    async def select_user(self,email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def select_user_by_id(self,id: int) -> User | None:
        query = select(User).where(User.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    

    