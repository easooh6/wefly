from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    
    class Config:
        from_attributes = True