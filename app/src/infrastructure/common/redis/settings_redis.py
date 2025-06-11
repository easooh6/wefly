from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

class SettingsSMTP(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = SettingsSMTP()
