from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

class SettingsSMTP(BaseSettings):
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str

    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = SettingsSMTP()