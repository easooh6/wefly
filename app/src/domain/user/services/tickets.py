from src.infrastructure.db.repositories.tickets_crud import Tickets_CRUD
from src.infrastructure.db.models.ticket import Tickets
from fastapi import Depends
from src.domain.user.dto.entities.created_ticket import CreatedTicketDTO
from src.domain.user.dto.requests.ticket import TicketRequestDTO
from sqlalchemy.exc import (OperationalError,IntegrityError,
                            ProgrammingError,SQLAlchemyError)

class TicketsService:

    def __init__(self, crud: Tickets_CRUD = Depends()):
        self.crud = crud
    
    async def add_ticket(self, data: TicketRequestDTO) -> CreatedTicketDTO:
        try:
            ticket= Tickets(**data.model_dump())
            await self.crud.add_ticket(ticket)
            return CreatedTicketDTO(id=ticket.id, user_id=ticket.user_id)
        except OperationalError:
            raise
        except IntegrityError:
            raise
        except ProgrammingError:
            raise
        except SQLAlchemyError:
            raise