from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time
from typing import Optional, List, Dict, Any

class TicketRequestDTO(BaseModel):

    id: str | None = None
    user_id: int
    name: str | None = None
    racenumber: str | None = None  

    departuredate: datetime | None = None
    departuretime: time | None = None
    originport: str | None = None
    origincityName: str | None = None

    arrivaldate: datetime | None = None
    arrivaltime: time | None = None
    destinationport: str | None = None
    destinationcityName: str | None = None

    flighttime: str | None = None
    price_light: Optional[int] = None
    price_optimal: Optional[int] = None
    price_comfort: Optional[int] = None

    class Config:
        populate_by_name = True
        str_strip_whitespace = True
        validate_assignment = True  