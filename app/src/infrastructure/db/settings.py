from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        env_file = os.path.join(base_dir, ".env")
        env_file_encoding = "utf-8"
        extra = 'ignore'


settings_db = Settings()
