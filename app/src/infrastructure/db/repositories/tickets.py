from src.infrastructure.db.models.ticket import Tickets
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user.interfaces.tickets import TicketInterface
from sqlalchemy.exc import (OperationalError,IntegrityError,
                            ProgrammingError,SQLAlchemyError,)
from src.domain.user.dto.entities.tickets import UserTicketDTO
from src.domain.user.exceptions import (TicketError, TicketAlreadyExistsError, TicketNotFoundError,
                                        TicketRepositoryError, InvalidTicketDataError, DatabaseConnectionError,
                                        TicketNotAvailableError)
from src.domain.auth.exceptions.db import DBServiceError
from src.domain.user.dto.responses.ticket import UserTicketResponseDTO
from sqlalchemy import select, delete
from typing import List

class TicketsCRUD(TicketInterface):

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_ticket(self, dto: UserTicketDTO) -> UserTicketResponseDTO:
        try:
            model = Tickets(**dto.model_dump())
            self.db.add(model)
            await self.db.flush()
            await self.db.refresh(model)
            return UserTicketResponseDTO(internal_id=model.internal_id ,id=model.id,
                user_id=model.user_id,
                name=model.name,
                racenumber=model.racenumber,
                departuredate=model.departuredate,
                departuretime=model.departuretime,
                originport=model.originport,
                origincityName=model.origincityName,
                arrivaldate=model.arrivaldate,
                arrivaltime=model.arrivaltime,
                destinationport=model.destinationport,
                destinationcityName=model.destinationcityName,
                flighttime=model.flighttime,
                price_light=model.price_light,
                price_optimal=model.price_optimal,
                price_comfort=model.price_comfort)
        except IntegrityError as e:
            raise TicketAlreadyExistsError
        except OperationalError as e:
            raise DBServiceError
        except SQLAlchemyError as e:
            raise TicketRepositoryError
    
    async def select_user_ticket(self, user_id: int) -> List[UserTicketResponseDTO]:
        try:
            query = select(Tickets).where(Tickets.user_id == user_id)
            result = await self.db.execute(query)
            tickets = result.scalars().all()
            if not tickets:
                return []
            return [
            UserTicketResponseDTO(
                internal_id=t.internal_id,
                id=t.id,
                user_id=t.user_id,
                name=t.name,
                racenumber=t.racenumber,
                departuredate=t.departuredate,
                departuretime=t.departuretime,
                originport=t.originport,
                origincityName=t.origincityName,
                arrivaldate=t.arrivaldate,
                arrivaltime=t.arrivaltime,
                destinationport=t.destinationport,
                destinationcityName=t.destinationcityName,
                flighttime=t.flighttime,
                price_light=t.price_light,
                price_optimal=t.price_optimal,
                price_comfort=t.price_comfort,
            )
            for t in tickets
        ]
        except OperationalError as e:
            raise DBServiceError
        except SQLAlchemyError as e:
            raise TicketRepositoryError



