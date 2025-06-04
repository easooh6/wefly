from src.infrastructure.db.models.ticket import Tickets
from src.infrastructure.db.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.exc import (OperationalError,IntegrityError,
                            ProgrammingError,SQLAlchemyError,)

class Tickets_CRUD:

    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db
    
    async def add_ticket(self, model: Tickets) -> Tickets:
        try:
            self.db.add(model)
            await self.db.flush()
            return model
        except IntegrityError as e:
            raise
        except OperationalError as e:
            raise
        except ProgrammingError as e:
            raise
        except SQLAlchemyError as e:
            raise



