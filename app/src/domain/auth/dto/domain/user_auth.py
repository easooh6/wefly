from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserAuthDTO(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True