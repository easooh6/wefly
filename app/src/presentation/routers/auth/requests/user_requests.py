from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(...,max_length=50)
    code: int

    class Config:
        from_attributes = True