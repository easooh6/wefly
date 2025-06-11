from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.repositories.tickets import TicketsCRUD
from src.infrastructure.db.db import get_db_session


async def get_tickets_rep(session: AsyncSession = Depends(get_db_session)):
    return TicketsCRUD(session)


