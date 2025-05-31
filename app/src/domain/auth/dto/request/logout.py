from pydantic import BaseModel

class LogoutDTO(BaseModel):

    refresh_hash: str
    
    class Config:
        from_attributes = True