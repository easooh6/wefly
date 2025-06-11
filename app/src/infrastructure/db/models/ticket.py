from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, Time
from .base import Base
from datetime import datetime, time

class Tickets(Base):
    
    __tablename__ = 'tickets'
    internal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[str] = mapped_column(String, primary_key=False)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(default='QAZAQ AIR JSC')
    racenumber: Mapped[str] = mapped_column(String)
    departuredate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    departuretime: Mapped[time] = mapped_column(Time)
    originport: Mapped[str] = mapped_column(String(3))
    origincityName: Mapped[str] = mapped_column(String)
    arrivaldate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    arrivaltime: Mapped[time] = mapped_column(Time)
    destinationport: Mapped[str] = mapped_column(String(3))
    destinationcityName: Mapped[str] = mapped_column(String)
    flighttime: Mapped[str] = mapped_column(String)
    price_light: Mapped[int] = mapped_column(Integer)
    price_optimal: Mapped[int] = mapped_column(Integer)
    price_comfort: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship("User", back_populates="tickets")