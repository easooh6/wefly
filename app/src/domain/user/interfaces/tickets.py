from abc import ABC, abstractmethod
from src.domain.user.dto.entities.tickets import UserTicketDTO
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from typing import List
class TicketInterface(ABC):

    @abstractmethod
    async def add_ticket(self, dto: UserTicketDTO) -> UserTicketResponseDTO:
        '''add new ticket'''
        pass
    
    @abstractmethod
    async def select_user_ticket(self, user_id: int) -> List[UserTicketResponseDTO]:
        pass
    