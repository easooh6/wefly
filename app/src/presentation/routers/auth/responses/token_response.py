from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: str = 'bearer'

    class Config:
        from_attributes = True