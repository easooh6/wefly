from src.domain.parsing.dto.requests import SearchOneWayRequestDTO, SearchRoundTripRequestDTO
from src.domain.parsing.dto.responses import SearchResponseDTO
from src.domain.parsing.services.fly_service import FlyService
from .responses.responses import SearchResponse, SearchResponseMany
from .requests.requests import SearchOneWayRequest, SearchRoundTripRequest
from fastapi import Depends, APIRouter, UploadFile, File, HTTPException
from ...di.search_di import get_fly_service
from ...di.ai_di import get_voice_service
from src.domain.ai.services.voice import VoiceService
import logging


logger = logging.getLogger('wefly.fast')
router = APIRouter()

@router.post('/search', response_model= SearchResponse, status_code=200)
async def search(request: SearchOneWayRequest,
                 service: FlyService = Depends(get_fly_service)):
    request_dto = SearchOneWayRequestDTO(**request.model_dump(by_alias=True))
    response = await service.search_one_way(request_dto)
    return SearchResponse(**response.model_dump())

@router.post('/search_round', response_model=SearchResponseMany, status_code=200)
async def search_many(request: SearchRoundTripRequest,
                       service: FlyService = Depends(get_fly_service)):
    request_dto = SearchRoundTripRequestDTO(**request.model_dump(by_alias = True))
    response = await service.search_round_trip(request_dto)
    return SearchResponseMany(**response.model_dump())

@router.post('/search_voice', status_code=200, response_model= SearchResponse | SearchResponseMany)
async def search_voice(
    audio: UploadFile = File(...,),
    voice_service: VoiceService = Depends(get_voice_service),
    flight_service: FlyService = Depends(get_fly_service)):

    if not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    audio_bytes = await audio.read()
    
    if len(audio_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    
    search_request = await voice_service.process_voice(audio_bytes, audio.content_type)

    if isinstance(search_request, SearchRoundTripRequestDTO):
        response = await flight_service.search_round_trip(search_request)
        logger.info(response.model_dump())
        return SearchResponseMany(**response.model_dump())
            
    elif isinstance(search_request, SearchOneWayRequestDTO):
        response = await flight_service.search_one_way(search_request)
        logger.info(response.model_dump())
        return SearchResponse(**response.model_dump())