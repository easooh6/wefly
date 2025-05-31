from pydantic import BaseModel, EmailStr

class EmailResponse(BaseModel):
    success: bool = True
    message: str

    class Config:
        from_attributes = True