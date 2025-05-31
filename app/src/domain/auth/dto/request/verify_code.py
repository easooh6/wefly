from pydantic import BaseModel, EmailStr

class VerifyCodeDTO(BaseModel):
    email: EmailStr
    code: int

    class Config:
        from_attributes = True