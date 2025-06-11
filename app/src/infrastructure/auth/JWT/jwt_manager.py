import jwt
from datetime import datetime, timedelta
from .jwt_settings import jwt_settings
from src.domain.auth.dto.domain.jwt import TokenDTO
from src.domain.auth.exceptions.jwt import InvalidPayloadError,ExpiredCredentialError, CredentialError
import logging

logger = logging.getLogger('wefly.jwt')

class JWTManager:

    def __init__(self):
        self.secret_key = jwt_settings.SECRET_KEY
        self.algorithm = jwt_settings.ALGORITHM
        self.access_token_expire = jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire = jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS

    def create_access_token(self, token: TokenDTO) -> str:
        payload = {

            **token.model_dump(),
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire)

        }
        logger.debug('access token successfully created')
        return jwt.encode(payload=payload,algorithm=self.algorithm, key=self.secret_key)
    
    def create_refresh_token(self, token: TokenDTO) -> str:
        payload = {

            **token.model_dump(),
            "exp": datetime.utcnow() + timedelta(days=self.refresh_token_expire)

        }
        logger.debug('refresh token successfully created')
        return jwt.encode(payload=payload,algorithm=self.algorithm, key=self.secret_key)
    
    def decode_token(self, token: str, expected_token: str) -> TokenDTO:
        logger.debug('Decoding %s token', expected_token)
        try:
            payload: dict = jwt.decode(token,self.secret_key,algorithms=[self.algorithm])
            user_id = payload.get('user_id')
            email = payload.get('email')
            token_type = payload.get('token_type')
            if token_type != expected_token:
                raise CredentialError
            if not user_id or not email:
                raise InvalidPayloadError
            logger.debug('Decoded %s token', expected_token)
            return TokenDTO(**payload)
        except jwt.ExpiredSignatureError:
            raise ExpiredCredentialError
        except jwt.InvalidTokenError:
            raise CredentialError


    def refresh_access_token(self,token: str) -> str:
        payload = self.decode_token(token, expected_token='refresh')
        payload.token_type = 'access'
        new_access = self.create_access_token(payload)
        return new_access






