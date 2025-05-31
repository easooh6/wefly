from pydantic import EmailStr, BaseModel

class EmailDTO(BaseModel):
    name: str
    email: EmailStr
    password: int

    class Config:
        from_attributes = True