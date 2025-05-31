from src.presentation.di.user_di import get_current_user
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from src.domain.auth.dto.response.user_profile import UserProfileDTO
from src.presentation.routers.user.responses.user_profile import UserProfileResponse
router = APIRouter()

@router.get('/profile', response_model=UserProfileResponse, status_code=200)
async def profile(user: UserProfileDTO = Depends(get_current_user)):
    return UserProfileResponse(**user.model_dump())