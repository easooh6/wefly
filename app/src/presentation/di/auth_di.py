from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from src.infrastructure.auth.JWT.jwt_manager import JWTManager

from src.domain.auth.exceptions.jwt import (
    CredentialError, 
    ExpiredCredentialError, 
    InvalidPayloadError
)
from src.domain.auth.dto.domain.jwt import TokenDTO

security = HTTPBearer()


async def verify_access_token(
    credentials = Depends(security),
    jwt_manager: JWTManager = Depends()) -> TokenDTO:

    token = credentials.credentials
    try:
        payload = jwt_manager.decode_token(token, expected_token='access')
        return payload
    except (CredentialError, ExpiredCredentialError, InvalidPayloadError) as e:
        raise HTTPException(status_code=401, detail={"message": "Invalid token"})
