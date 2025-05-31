from pydantic import BaseModel, EmailStr
from typing import Literal

class TokenDTO(BaseModel):
    user_id: int
    email: EmailStr
    is_admin: bool = False
    token_type: Literal['access', 'refresh']

    class Config:
        from_attributes = True

