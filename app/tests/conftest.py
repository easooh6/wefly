import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.infrastructure.db.test_settings import settings_db_test
from src.infrastructure.db.models import Base
from typing import AsyncGenerator
from src.infrastructure.common.redis.redis_pool import REDIS_URL
import redis.asyncio as redis
from sqlalchemy import text, delete
from httpx import AsyncClient, ASGITransport
from src.presentation.main import app

TABLES = ['tickets', 'users']

@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Создает тестовую БД для всей сессии"""
    engine = create_async_engine(
        settings_db_test.DATABASE_URL_asyncpg,
        echo=False,  # Отключаем SQL логи в тестах
    )
    
    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Очищаем после всех тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest_asyncio.fixture(scope='session')
async def test_session_fabric(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session(test_session_fabric):
    async with test_session_fabric() as session:
        trans = await session.begin() 
        try:
            yield session
        finally:
            await trans.rollback()  
            await session.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    """Создает Redis клиент для всей тестовой сессии"""

    client = await redis.from_url(
        url=REDIS_URL,
        decode_responses=True,
        max_connections=5
    )
    
    # Очищаем в начале сессии
    await client.flushdb()
    
    yield client  # ✅ Возвращаем готовый клиент

    # Очищаем и закрываем в конце сессии
    await client.flushdb()
    await client.aclose()

# ✅ ДОБАВЛЯЕМ clean_redis для изоляции тестов
@pytest_asyncio.fixture
async def clean_redis(redis_client):
    """Очищает Redis перед каждым тестом"""
    await redis_client.flushdb()
    yield redis_client

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        yield client