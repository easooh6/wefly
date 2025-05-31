from pydantic import BaseModel

class RefreshRequest(BaseModel):
    refresh: str

    class Config:
        from_attributes = True