from .settings import settings
import google.generativeai as genai
import asyncio



class GeminiClient:

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config={
                "temperature": settings.TEMPERATURE,
                "max_output_tokens": settings.MAX_RESPONSE_LENGTH
            }
        )
    # убрать event_loop нахуй, почитать что лучше
    async def transcribe_voice(self, audio_bytes: bytes, mime_type: str, prompt: str) -> str:
        audio_part = {
            "mime_type": mime_type,
            "data": audio_bytes
        }
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: self.model.generate_content([prompt, audio_part])
        )

        return response.text
    
