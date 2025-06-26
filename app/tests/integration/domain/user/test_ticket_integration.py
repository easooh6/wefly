import pytest
from src.domain.user.services.tickets import TicketsService
from src.domain.user.interfaces.tickets import TicketInterface
from src.domain.user.dto.entities.tickets import UserTicketDTO
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from src.infrastructure.db.repositories.tickets import TicketsCRUD
from src.infrastructure.db.models.user_model import User

@pytest.mark.integration
@pytest.mark.asyncio
async def test_add_select_ticket(db_session):
    db = TicketsCRUD(db_session)
    service = TicketsService(db)
    
    user_model = User(id=1,name='test', email='test@email.com', hashed_password= 'testpass')
    db_session.add(user_model)
    await db_session.flush()

    dto = UserTicketDTO(
        id = '5',
        user_id=1,
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
    result = await service.add_ticket(dto)

    assert isinstance(result, UserTicketResponseDTO)
    assert dto.user_id == result.user_id
    
    data_db = await db.select_user_ticket(dto.user_id)

    assert any(ticket.id == dto.id for ticket in data_db)
    assert isinstance(data_db, list)

    

