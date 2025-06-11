import redis.asyncio as redis
from .settings_redis import settings
import logging

# Глобальная переменная для хранения клиента
_redis_client = None
REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"

logger = logging.getLogger()

async def get_redis_client():
    global _redis_client
    if _redis_client is None:
        # Создаем клиент только один раз
        _redis_client = await redis.from_url(
            url=REDIS_URL, 
            decode_responses=True,
            # Можно настроить пул соединений
            max_connections=10
        )
    logger.debug('Redis connection activated')
    return _redis_client
