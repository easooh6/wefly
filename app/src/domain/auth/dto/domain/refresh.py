from pydantic import BaseModel
from datetime import datetime

class RefreshTokenDTO(BaseModel):
    id: int
    user_id: int
    token_hash: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
