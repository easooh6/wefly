from src.domain.ai.services.voice import VoiceService
from src.infrastructure.ai.gemini_client import GeminiClient
from src.infrastructure.ai.prompts import Prompts

def get_voice_service() -> VoiceService:
    client= GeminiClient()
    return VoiceService(client)