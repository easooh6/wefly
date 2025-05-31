from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreatedUserDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True