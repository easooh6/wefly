from pydantic import BaseModel, EmailStr

class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    code: int

    class Config:
        from_attributes = True