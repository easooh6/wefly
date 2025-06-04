from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time
from typing import Optional, List, Dict, Any

class TicketRequestDTO(BaseModel):

    id: str | int | None = None
    user_id: int
    name: str | None = None
    racenumber: str | None = None  

    departuredate: str | None = None
    departuretime: str | None = None
    originport: str | None = None
    origincityName: str | None = None

    arrivaldate: str | None = None
    arrivaltime: str | None = None
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