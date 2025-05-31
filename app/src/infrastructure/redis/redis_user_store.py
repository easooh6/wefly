import json
from fastapi import Depends
from .redis_pool import get_redis_client
from src.domain.auth.dto.request.user_create import UserCreateDTO
import logging

logger = logging.getLogger()

class RedisUserStore:

    _USER_DATA_EXPIRATION = 1800  

    _USER_PREFIX = "user_data:"
    
    def __init__(self, redis = Depends(get_redis_client)):
        self.redis = redis
    
    async def save_user_data(self, user: UserCreateDTO):
        """Сохраняет данные пользователя в Redis"""
        key = f"{self._USER_PREFIX}{user.email}"
        await self.redis.set(
            key, 
            user.model_dump_json(),
            ex=self._USER_DATA_EXPIRATION
        )
        logger.debug('User %s was saved in Redis', user.email)
    
    async def get_user_data(self, email: str) -> UserCreateDTO:
        """Получает данные пользователя из Redis"""
        key = f"{self._USER_PREFIX}{email}"
        data = await self.redis.get(key)
        
        if data:
            logger.debug('User %s was got from Redis', email)
            return UserCreateDTO(**json.loads(data))
        return None
    
    async def delete_user_data(self, email: str):
        """Удаляет данные пользователя из Redis"""
        key = f"{self._USER_PREFIX}{email}"
        await self.redis.delete(key)
        logger.debug('User %s was deleted from Redis', email)    