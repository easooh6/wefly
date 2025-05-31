from pydantic import BaseModel, EmailStr

class UserHashedDTO(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True