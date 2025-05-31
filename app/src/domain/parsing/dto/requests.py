from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional

class SearchOneWayRequestDTO(BaseModel):
    searchGroupId: str = 'standard'
    segmentsCount: int = 1
    date_0: str = Field(..., alias='date[0]', description="Дата в формате DD.MM.YYYY")
    origin_city_code_0: str = Field(..., alias='origin-city-code[0]', description="Код города отправления")
    destination_city_code_0: str = Field(..., alias='destination-city-code[0]', description="Код города назначения")
    adultsCount: int = Field(default=1, ge=1, le=9, description="Количество взрослых")
    childrenCount: int = Field(default=0, ge=0, le=9, description="Количество детей")
    childCount: int = Field(default=0, ge=0, le=9)
    infantsWithSeatCount: int = Field(default=0, ge=0, le=9, description="Младенцы с местом")
    infantsWithoutSeatCount: int = Field(default=0, ge=0, le=9, description="Младенцы без места")

    class Config:
        populate_by_name = True 
        str_strip_whitespace = True

class SearchRoundTripRequestDTO(BaseModel):
    searchGroupId: str = 'standard'
    segmentsCount: int = 2
  
    date_0: str = Field(..., alias='date[0]')
    origin_city_code_0: str = Field(..., alias='origin-city-code[0]')
    destination_city_code_0: str = Field(..., alias='destination-city-code[0]')

    date_1: str = Field(..., alias='date[1]')
    origin_city_code_1: str = Field(..., alias='origin-city-code[1]')
    destination_city_code_1: str = Field(..., alias='destination-city-code[1]')

    adultsCount: int = Field(default=1, ge=1, le=9)
    childrenCount: int = Field(default=0, ge=0, le=9)
    childCount: int = Field(default=0, ge=0, le=9)
    infantsWithSeatCount: int = Field(default=0, ge=0, le=9)
    infantsWithoutSeatCount: int = Field(default=0, ge=0, le=9)
    