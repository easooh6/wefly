import os
from pydantic_settings import BaseSettings

class AI_Settings(BaseSettings):
    
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    
    AUDIO_MAX_SIZE_MB: int = 10
    SUPPORTED_AUDIO_FORMATS: list = ["mp3", "wav", "m4a", "webm", "ogg"]
    
    
    MAX_RESPONSE_LENGTH: int = 1000
    TEMPERATURE: float = 0


    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = AI_Settings()