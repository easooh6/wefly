import pytest
from src.domain.user.services.tickets import TicketsService
from unittest.mock import AsyncMock
from src.domain.user.dto.entities.tickets import UserTicketDTO
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from src.domain.user.exceptions import TicketAlreadyExistsError
from src.domain.user.exceptions import TicketNotFoundError

@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_ticket():
    infrastructure_mock = AsyncMock()

    dto = UserTicketDTO(
        id = '1',
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

    expected_result = UserTicketResponseDTO(
        internal_id=1,
        **dto.model_dump()
    )

    infrastructure_mock.add_ticket.return_value = expected_result

    service = TicketsService(infrastructure_mock)

    result = await service.add_ticket(dto)
    
    assert result == expected_result
    infrastructure_mock.add_ticket.assert_called_once_with(dto)
    assert isinstance(result, UserTicketResponseDTO)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_ticket_already_exists():
    infrastructure_mock = AsyncMock()

    dto = UserTicketDTO(
        id = '1',
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

    infrastructure_mock.add_ticket.side_effect = TicketAlreadyExistsError

    service = TicketsService(infrastructure_mock)
    
    with pytest.raises(TicketAlreadyExistsError):
        await service.add_ticket(dto)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_select_ticket():
    interface_mock = AsyncMock()

    expected_result = [UserTicketResponseDTO(
        internal_id=1,
        id = '1',
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
    ]

    interface_mock.select_user_ticket.return_value = expected_result

    service = TicketsService(interface_mock)
    
    user_id = expected_result[0].user_id

    result = await service.select_user_ticket(user_id)

    assert result == expected_result
    assert result[0].user_id == user_id
    assert isinstance(result, list)
    assert all(isinstance(item, UserTicketResponseDTO) for item in result)
    interface_mock.select_user_ticket.assert_called_once_with(user_id)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_select_ticket_not_found():

    interface_mock = AsyncMock()

    interface_mock.select_user_ticket.side_effect = TicketNotFoundError

    service = TicketsService(interface_mock)
    user_id = 1

    with pytest.raises(TicketNotFoundError):
        await service.select_user_ticket(user_id)
    
    