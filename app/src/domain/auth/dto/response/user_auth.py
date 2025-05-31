from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserAuthResponseDTO(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True