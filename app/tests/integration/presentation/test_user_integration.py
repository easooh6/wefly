import pytest
from src.presentation.main import app
from src.domain.auth.dto.response.user_profile import UserProfileDTO
from src.presentation.di.user_di import get_current_user
from src.presentation.di.service.user import get_tickets_service
from src.presentation.routers.user.requests.ticket import UserTicketRequest
from httpx import AsyncClient
from src.presentation.routers.user.responses.ticket import UserTicketResponse
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from src.domain.user.exceptions import TicketNotFoundError
from src.infrastructure.db.repositories.tickets import TicketsCRUD
from src.domain.user.services.tickets import TicketsService
from src.infrastructure.db.models.user_model import User
from src.domain.user.dto.entities.tickets import UserTicketDTO

@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_select_ticket(async_client: AsyncClient, db_session):

    user = UserProfileDTO(id=1, name = 'test', email = 'test@email.com', is_admin = False)
    
    infrastructure = TicketsCRUD(db_session)

    service = TicketsService(infrastructure)

    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_tickets_service] = lambda: service

    user_model = User(id=1,name='test', email='test@email.com', hashed_password= 'testpass')
    db_session.add(user_model)
    await db_session.flush()

    request = UserTicketRequest(
        id = '5',
        name='Test',
        racenumber='AB123',
        departuredate='2025-06-30',
        departuretime='08:00',
        originport='JFK',
        origincityName='New York',
        arrivaldate='2025-06-30',
        arrivaltime='12:00',
        destinationport='LAX',
        destinationcityName='Los Angeles',
        flighttime='6h',
        price_light=100.0,
        price_optimal=150.0,
        price_comfort=200.0
    )
    
    json_request = request.model_dump(mode='json')

    result_post = await async_client.post('/user/add_ticket', json=json_request)

    post_data = result_post.json()
    assert post_data['id'] == request.id
    assert post_data['name'] == request.name
    assert post_data['user_id'] == 1
    assert post_data['racenumber'] == request.racenumber

    result_get = await async_client.get('/user/tickets')

    assert result_post.status_code == 201
    assert result_get.status_code == 200

    tickets = result_get.json()
    assert isinstance(tickets, list)
    assert len(tickets) == 1
        
    ticket = tickets[0]
    assert ticket['id'] == request.id
    assert ticket['name'] == request.name
    assert ticket['racenumber'] == request.racenumber
    assert ticket['originport'] == request.originport
    assert ticket['destinationport'] == request.destinationport
    assert ticket['price_light'] == request.price_light
    assert ticket['price_optimal'] == request.price_optimal
    assert ticket['price_comfort'] == request.price_comfort
    assert ticket['user_id'] == user.id

    app.dependency_overrides.clear()
