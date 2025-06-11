from src.domain.user.dto.requests.ticket import TicketRequestDTO
from src.domain.user.exceptions import (TicketError, TicketAlreadyExistsError, TicketNotFoundError,
                                        TicketRepositoryError, InvalidTicketDataError, DatabaseConnectionError,
                                        TicketNotAvailableError)
from src.domain.user.interfaces.tickets import TicketInterface
from src.domain.user.dto.entities.tickets import UserTicketDTO
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from typing import List

class TicketsService:

    def __init__(self, infrastructure: TicketInterface):
        self.inf = infrastructure
    
    async def add_ticket(self, data: UserTicketDTO) -> UserTicketResponseDTO:
        result = await self.inf.add_ticket(data)
        return result
    
    async def select_user_ticket(self, user_id: int) -> List[UserTicketResponseDTO]:
        result = await self.inf.select_user_ticket(user_id)
        if not result:
            raise TicketNotFoundError
        return result
    