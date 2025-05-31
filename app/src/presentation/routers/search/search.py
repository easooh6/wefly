from src.domain.parsing.dto.requests import SearchOneWayRequestDTO, SearchRoundTripRequestDTO
from src.domain.parsing.dto.responses import SearchResponseDTO
from src.domain.parsing.services.fly_service import FlyService
from .responses.responses import SearchResponse, SearchResponseMany
from .requests.requests import SearchOneWayRequest, SearchRoundTripRequest
from fastapi import Depends, APIRouter
from ...di.search_di import get_fly_service

router = APIRouter()

@router.post('/search', response_model= SearchResponse, status_code=200)
async def search(request: SearchOneWayRequest,service: FlyService = Depends(get_fly_service)):
    request_dto = SearchOneWayRequestDTO(**request.model_dump(by_alias=True))
    response = await service.search_one_way(request_dto)
    return SearchResponse(**response.model_dump())

@router.post('/search_round', response_model=SearchResponseMany, status_code=200)
async def search_many(request: SearchRoundTripRequest, service: FlyService = Depends(get_fly_service)):
    request_dto = SearchRoundTripRequestDTO(**request.model_dump(by_alias = True))
    response = await service.search_round_trip(request_dto)
    return SearchResponseMany(**response.model_dump())
