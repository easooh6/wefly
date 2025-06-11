from src.presentation.di.user_di import get_current_user
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from src.domain.auth.dto.response.user_profile import UserProfileDTO
from src.presentation.routers.user.responses.profile import UserProfileResponse
from .responses.ticket import UserTicketResponse
from .requests.ticket import UserTicketRequest
from ...di.service.user import get_tickets_service
from src.domain.user.dto.entities.tickets import UserTicketDTO
from typing import List
from ...di.auth_di import verify_access_token

router = APIRouter()

@router.get('/profile', response_model=UserProfileResponse, status_code=200)
async def profile(user: UserProfileDTO = Depends(get_current_user)):
    return UserProfileResponse(**user.model_dump())

@router.post('/add_ticket', response_model=UserTicketResponse, status_code=201)
async def add_ticket(request: UserTicketRequest, user: UserProfileDTO = Depends(get_current_user),
                     service = Depends(get_tickets_service)):
    ticket = UserTicketDTO(**request.model_dump(), user_id=user.id)

    result = await service.add_ticket(ticket)
    return UserTicketResponse(**result.model_dump())

@router.get('/tickets', response_model=List[UserTicketResponse], status_code=200)
async def get_user_ticket(user = Depends(get_current_user),
                          service = Depends(get_tickets_service)):
    tickets = await service.select_user_ticket(user.id)
    return [UserTicketResponse(**ticket.model_dump()) for ticket in tickets]
