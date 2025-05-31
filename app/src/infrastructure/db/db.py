from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.infrastructure.db.settings import settings_db

from collections.abc import AsyncGenerator
import logging

logger = logging.getLogger('wefly.db')

logger.info('Initializing database engine')

async_engine = create_async_engine(
    url= settings_db.DATABASE_URL_asyncpg,
    pool_size=5,
    max_overflow=10
)

session_fabric = async_sessionmaker(async_engine,
                                    expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    logger.debug('Starting DB session')
    async with session_fabric() as session:

        try:
            yield session
            await session.commit()
            logger.debug('Database session committed successfully')
        except Exception as e:
            await session.rollback()
            logger.error('Database session rollback due to error: %s', str(e))
            raise
        finally:
            logger.debug('Database session closed')
