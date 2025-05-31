from fastapi import FastAPI, Depends, APIRouter, HTTPException, Response, Request
from src.domain.auth.services.email_service import EmailService
from src.presentation.routers.auth.requests.email_requests import RegisterRequest
from src.presentation.routers.auth.requests.user_requests import UserRegisterRequest
from src.presentation.routers.auth.requests.token_request import TokenRequest
from src.presentation.routers.auth.responses.email_responses import EmailResponse
from src.presentation.routers.auth.responses.user_responses import UserRegisterResponse
from src.presentation.routers.auth.responses.token_response import TokenResponse
from src.domain.auth.dto.request.user_create import UserCreateDTO
from src.domain.auth.services.register import RegisterService
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.services.auth import AuthUser
from src.domain.auth.dto.request.user_auth import UserAuthRequestDTO
from src.presentation.routers.auth.requests.refresh_request import RefreshRequest
from src.presentation.routers.auth.responses.refresh_response import RefreshResponse
from src.domain.auth.services.refresh_service import RefreshService
from src.domain.auth.dto.request.logout import LogoutDTO
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post('/send-verification', response_model = EmailResponse, status_code=200)
async def send_verification(email_request: RegisterRequest,
                             service: EmailService = Depends()):
    email_dto = UserCreateDTO(name=email_request.name,
        email=email_request.email,
        password=email_request.password,
        code=0
        )
    result = await service.send_verification_code(email_dto)
    return EmailResponse(message='The letter was sent')


@router.post('/registration',response_model=UserRegisterResponse,status_code=200)
@limiter.limit('3/minute')
async def registration(request: Request, user_request:UserRegisterRequest,
                        service: RegisterService = Depends()):
    verify_dto = VerifyCodeDTO(email=user_request.email, code=user_request.code)
    result = await service.register_user(verify_dto)
    return UserRegisterResponse(**result.model_dump())
        
@router.post('/login', response_model=TokenResponse, status_code=200)
@limiter.limit('5/minute')
async def login(request: Request, login_request: TokenRequest, service: AuthUser = Depends()):
    user_dto = UserAuthRequestDTO(**login_request.model_dump())
    user = await service.auth_user(user_dto)
    return TokenResponse(access_token= user.access_token,refresh_token= user.refresh_token)
   

@router.post('/refresh', response_model=RefreshResponse, status_code=200)
async def refresh(refresh_request: RefreshRequest, service: RefreshService = Depends()): 
    access = await service.refresh_access_token(refresh_request.refresh)
    return RefreshResponse(access=access)
   

@router.post('/logout',status_code=200)
async def logout(refresh_request: RefreshRequest, service: AuthUser = Depends()):
    data_dto = LogoutDTO(refresh_hash=refresh_request.refresh)
    await service.logout(data_dto)
    return {"message": "User logged out successfully"}
   