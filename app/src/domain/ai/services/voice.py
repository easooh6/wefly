from src.domain.parsing.dto.requests import SearchRoundTripRequestDTO, SearchOneWayRequestDTO
from src.infrastructure.ai.gemini_client import GeminiClient
from src.infrastructure.ai.prompts import Prompts
from ..exceptions import *
import logging
import asyncio
import json
from google.genai import errors as genai_errors

logger = logging.getLogger('wefly.ai_voice')

class VoiceService:

    def __init__(self, client: GeminiClient):
        self.client = client
    
    async def process_voice(self, audio_bytes: bytes,
                            mime_type: str) -> SearchOneWayRequestDTO | SearchRoundTripRequestDTO:
        logger.info('started processing voice')
        
        try:
            response: str = await self.client.transcribe_voice(audio_bytes, mime_type, Prompts.get_universal_prompt())
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
            logger.error("Network connection error: %s",str(e))
            raise ConnectionError
            
        except genai_errors.ClientError as e:
            logger.error("Gemini API unauthorized: %s",str(e))
            raise GeminiuUnauthorizedError
            
        except genai_errors.ServerError as e:
            logger.error("Gemini service unavailable: %s", str(e))
            raise GeminiUnavailableError
            
        except genai_errors.APIError as e:
            logger.error("Gemini request timeout: %s", str(e))
            raise GeminiTimeoutError
        
        except json.JSONDecodeError as e:
            logger.error("Failed to parse Gemini response as JSON: %s", str(e))
            raise VoiceProcessingError

        except (KeyError, TypeError, ValueError) as e:
            logger.error("Failed to create DTO from parsed data: %s", str(e))
            raise VoiceProcessingError

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise VoiceProcessingError



