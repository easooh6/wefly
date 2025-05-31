from pydantic import EmailStr, BaseModel

class EmailCodeDTO(BaseModel):
    code: int
    success: bool = True

    class Config:
        from_attributes = True