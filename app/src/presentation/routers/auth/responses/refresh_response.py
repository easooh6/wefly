from pydantic import BaseModel

class RefreshResponse(BaseModel):
    access: str

    class Config:
        from_attributes = True