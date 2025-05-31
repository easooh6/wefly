from .user_di import get_current_user
from fastapi import Depends
from src.domain.auth.dto.response.user_profile import UserProfileDTO
from fastapi import Depends, HTTPException

async def verify_admin(data: UserProfileDTO = Depends(get_current_user)):
    if data.is_admin != True:
        raise HTTPException(status_code=403, detail='Admin access required')
    return data 