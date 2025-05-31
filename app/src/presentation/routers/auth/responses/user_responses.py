from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserRegisterResponse(BaseModel):
    id: int
    email: EmailStr = Field(...,max_length=50)
    name: str
    created_at: datetime

    class Config:
        from_attributes = True