import os
from pydantic_settings import BaseSettings

class JWTSettings(BaseSettings):
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')

    class Config:
        env_file = '.env'
        extra = 'ignore'

jwt_settings = JWTSettings()