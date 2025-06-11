from ..repository.user import get_tickets_rep
from fastapi import Depends
from src.domain.user.services.tickets import TicketsService
from src.domain.auth.dto.domain.jwt import TokenDTO
from src.presentation.di.auth_di import verify_access_token

async def get_tickets_service(repository = Depends(get_tickets_rep)):
    return TicketsService(repository)