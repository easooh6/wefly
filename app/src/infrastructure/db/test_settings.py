from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

class Settings(BaseSettings):
    DB_TEST_HOST: str
    DB_TEST_PORT: str
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_TEST_PORT}/{self.DB_TEST_NAME}"
    
    class Config:
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        env_file = os.path.join(base_dir, ".env")
        env_file_encoding = "utf-8"
        extra = 'ignore'


settings_db_test = Settings()
