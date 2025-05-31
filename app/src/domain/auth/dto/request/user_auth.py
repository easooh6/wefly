from pydantic import BaseModel, EmailStr

class UserAuthRequestDTO(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True