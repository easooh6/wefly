from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions, Part
from .settings import settings
import base64


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options=HttpOptions(api_version="v1")
        )

    async def transcribe_voice(self, audio_bytes: bytes, mime_type: str, prompt: str) -> str:
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        contents = [
            Part(text=prompt),  
            Part(inline_data={"mime_type": mime_type, "data": audio_b64}) 
        ]
        
        response = await self.client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=GenerateContentConfig(
                temperature=settings.TEMPERATURE,
                max_output_tokens=settings.MAX_RESPONSE_LENGTH
            )
        )
        
        return response.text

