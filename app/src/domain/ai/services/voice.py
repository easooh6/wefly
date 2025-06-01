from src.domain.parsing.dto.requests import SearchRoundTripRequestDTO, SearchOneWayRequestDTO
from src.infrastructure.ai.gemini_client import GeminiClient
from src.infrastructure.ai.prompts import Prompts
from ..exceptions import *
import logging
import asyncio
import json
import google.api_core.exceptions

logger = logging.getLogger('wefly.ai_voice')

class VoiceService:

    def __init__(self, prompts: Prompts,
                 client: GeminiClient):
        self.prompts = prompts
        self.client = client
    
    async def process_voice(self, audio_bytes: bytes,
                            mime_type: str) -> SearchOneWayRequestDTO | SearchRoundTripRequestDTO:
        logger.info('started processing voice')
        
        try:
            response: str = await self.client.transcribe_voice(audio_bytes, mime_type, self.prompts.universal_prompt)
            cleaned = response.strip()
            if "```json" in cleaned:
                start = cleaned.find("```json") + 7
            end = cleaned.find("```", start)
            cleaned = cleaned[start:end].strip()
            data = json.loads(cleaned)

            if data.get("segmentsCount") == 2:
                logger.info('gemini returned round-trip request')
                return SearchRoundTripRequestDTO(**data)
            else:
                logger.info('gemini returned one-way request')
                return SearchOneWayRequestDTO(**data)
            
        except ConnectionError as e:
            logger.error(f"Network connection error: {str(e)}")
            raise ConnectionError
            
        except google.api_core.exceptions.Unauthorized:
            logger.error("Gemini API unauthorized")
            raise GeminiuUnauthorizedError
            
        except google.api_core.exceptions.ServiceUnavailable:
            logger.error("Gemini service unavailable")
            raise GeminiUnavailableError
            
        except google.api_core.exceptions.DeadlineExceeded:
            logger.error("Gemini request timeout")
            raise GeminiTimeoutError
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise VoiceProcessingError



