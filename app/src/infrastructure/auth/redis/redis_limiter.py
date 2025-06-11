import redis.asyncio as redis
from src.infrastructure.common.redis.redis_pool import get_redis_client
from fastapi import Depends


class RedisLimiter():

    _CODE_EXPIRATION = 300
    _RATE_LIMIT = 3

    def __init__(self, redis = Depends(get_redis_client)):
        self.redis = redis

    async def save_code(self,email,code):
        await self.redis.set(email,code,ex=self._CODE_EXPIRATION)

    async def get_code(self, email):
        code_value = await self.redis.get(email)
        if code_value is None:
            return None
        
        # Безопасное преобразование значения в int
        try:
            # Если это байты
            if isinstance(code_value, bytes):
                return int(code_value.decode('utf-8'))
            # Если это строка
            else:
                return int(code_value)
        except (ValueError, TypeError) as e:
            print(f"Error converting code to int: {e}, value: {code_value}, type: {type(code_value)}")
            return None
    
    async def delete_code(self,email):
        await self.redis.delete(email)

    async def check_rate_limit(self,email) -> bool:
        key = f"user:{email}"
        request = await self.redis.get(key)
        if not request:
            await self.redis.set(key,1,ex=self._CODE_EXPIRATION)
            return True
        elif int(request) < self._RATE_LIMIT:
            await self.redis.set(key,int(request)+1,ex=self._CODE_EXPIRATION)
            return True
        elif int(request) >= self._RATE_LIMIT:
            return False
