
from fastapi import Depends
from src.infrastructure.parser.parser import ParseFly
from src.domain.parsing.services.fly_service import FlyService

def get_parser() -> ParseFly:
    
    return ParseFly()

def get_fly_service(parser: ParseFly = Depends(get_parser)) -> FlyService:

    return FlyService(parser)


