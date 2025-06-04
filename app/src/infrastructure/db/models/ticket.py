from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime
from .base import Base
from datetime import datetime

class Tickets(Base):
    
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(default='QAZAQ AIR JSC')
    racenumber: Mapped[int] = mapped_column(Integer)
    departuredate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    departuretime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    originport: Mapped[str] = mapped_column(String(3))
    origincityName: Mapped[str] = mapped_column(String)
    arrivaldate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    arrivaltime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    destinationport: Mapped[str] = mapped_column(String(3))
    destinationcityName: Mapped[str] = mapped_column(String)
    flighttime: Mapped[str] = mapped_column(String)
    price_light: Mapped[int] = mapped_column(Integer)
    price_optimal: Mapped[int] = mapped_column(Integer)
    price_comfort: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship("User", back_populates="tickets")