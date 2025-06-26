import pytest
from unittest.mock import AsyncMock
from src.presentation.main import app
from src.domain.auth.dto.response.user_profile import UserProfileDTO
from src.presentation.di.user_di import get_current_user
from src.presentation.di.service.user import get_tickets_service
from src.presentation.routers.user.requests.ticket import UserTicketRequest
from httpx import AsyncClient
from src.presentation.routers.user.responses.ticket import UserTicketResponse
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from src.domain.user.exceptions import TicketNotFoundError

@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_ticket(async_client: AsyncClient):

    service = AsyncMock()
    
    user = UserProfileDTO(id=1, name = 'test', email = 'test@email.com', is_admin = False)
    
    request = UserTicketRequest(id = "ABC123",
    name =  "test",
    racenumber= "EK202",
    departuredate= "2025-07-10T00:00:00",
    departuretime= "14:30:00",
    originport= "JFK",
    origincityName= "New York",
    arrivaldate= "2025-07-10T00:00:00",
    arrivaltime= "20:45:00",
    destinationport= "DXB",
    destinationcityName= "Dubai",
    flighttime= "12h 15m",
    price_light= 350,
    price_optimal= 500,
    price_comfort= 750)

    ticket_dto = UserTicketResponseDTO(**request.model_dump(), user_id=user.id, internal_id=1)

    service.add_ticket.return_value = ticket_dto

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_tickets_service] = lambda: service

    response = await async_client.post('/user/add_ticket', json=request.model_dump(mode="json"))

    expected_response = UserTicketResponse(**ticket_dto.model_dump())

    assert response.status_code == 201
    assert expected_response.model_dump(mode="json") == response.json()

    app.dependency_overrides.clear()
    

@pytest.mark.unit
@pytest.mark.asyncio
async def test_select_ticket(async_client: AsyncClient):

    service = AsyncMock()
    user = UserProfileDTO(id=1, name = 'test', email = 'test@email.com', is_admin = False)

    request = UserTicketRequest(id = "ABC123",
    name =  "test",
    racenumber= "EK202",
    departuredate= "2025-07-10T00:00:00",
    departuretime= "14:30:00",
    originport= "JFK",
    origincityName= "New York",
    arrivaldate= "2025-07-10T00:00:00",
    arrivaltime= "20:45:00",
    destinationport= "DXB",
    destinationcityName= "Dubai",
    flighttime= "12h 15m",
    price_light= 350,
    price_optimal= 500,
    price_comfort= 750)

    ticket_dto = UserTicketResponseDTO(**request.model_dump(), user_id=user.id, internal_id=1)

    service.select_user_ticket.return_value =[ticket_dto]


    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_tickets_service] = lambda: service

    response = await async_client.get('/user/tickets')

    expected_response = [UserTicketResponse(**ticket_dto.model_dump())]

    assert response.status_code == 200
    assert [r.model_dump(mode="json") for r in expected_response] == response.json()

    app.dependency_overrides.clear()

@pytest.mark.unit
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'invalid_json',
       [
            {},
            {'id': '1', 'name': 'test'},
            {'name': 'test', 'racenumber': 'ABC'},
            {'id': '1', 'racenumber': 'ABC'},
            {'id': 1, 'name': 1, 'racenumber': 1},
        ]
    )
async def test_add_ticket_invalid_input(async_client: AsyncClient, invalid_json):

    service = AsyncMock()

    user = UserProfileDTO(id=1, name = 'test', email = 'test@email.com', is_admin = False)
 
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_tickets_service] = lambda: service

    response = await async_client.post("/user/add_ticket", json=invalid_json)
    assert response.status_code == 422

@pytest.mark.unit
@pytest.mark.asyncio
async def test_select_invalid_output(async_client: AsyncClient):
    service = AsyncMock()
    user = UserProfileDTO(id=1, name='test', email='test@email.com', is_admin=False)

    service.select_user_ticket.side_effect = TicketNotFoundError

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_tickets_service] = lambda: service

    response = await async_client.get('/user/tickets')

    assert response.status_code == 400
    assert response.json() ==   {"message":"Ticket not found."}

    app.dependency_overrides.clear()

