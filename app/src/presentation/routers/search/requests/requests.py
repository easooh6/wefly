from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional

class SearchOneWayRequest(BaseModel):
    searchGroupId: str = 'standard'
    segmentsCount: int = 1
    date_0: str = Field(..., alias='date[0]', description="Дата в формате DD.MM.YYYY")
    origin_city_code_0: str = Field(..., alias='origin-city-code[0]', description="Код города отправления")
    destination_city_code_0: str = Field(..., alias='destination-city-code[0]', description="Код города назначения")
    adultsCount: int = Field(default=1, ge=1, le=9, description="Количество взрослых")
    childrenCount: int = Field(default=0, ge=0, le=9, description="Количество детей")
    childCount: int = Field(default=0, ge=0, le=9)  # Дублирует childrenCount
    infantsWithSeatCount: int = Field(default=0, ge=0, le=9, description="Младенцы с местом")
    infantsWithoutSeatCount: int = Field(default=0, ge=0, le=9, description="Младенцы без места")

    
    @field_validator('date_0')
    @classmethod
    def validate_date_format(cls, v):
        """Валидация формата даты"""
        if isinstance(v, str):
            try:
                # Проверяем формат DD.MM.YYYY
                datetime.strptime(v, '%d.%m.%Y')
                return v
            except ValueError:
                raise ValueError('Дата должна быть в формате DD.MM.YYYY')
        elif isinstance(v, (date, datetime)):
            return v.strftime('%d.%m.%Y')
        else:
            raise ValueError('Неверный тип даты')
    
    @field_validator('origin_city_code_0', 'destination_city_code_0')
    @classmethod
    def validate_airport_code(cls, v):
        """Валидация кода аэропорта"""
        if not v or len(v) != 3:
            raise ValueError('Код аэропорта должен содержать 3 символа')
        return v.upper()

    class Config:
        populate_by_name = True  # Позволяет использовать как алиас, так и имя поля
        str_strip_whitespace = True

# src/domain/parsing/dto/requests.py
class SearchRoundTripRequest(BaseModel):
    searchGroupId: str = 'standard'
    segmentsCount: int = 2
    
    # Туда
    date_0: str = Field(..., alias='date[0]')
    origin_city_code_0: str = Field(..., alias='origin-city-code[0]')
    destination_city_code_0: str = Field(..., alias='destination-city-code[0]')
    
    # Обратно
    date_1: str = Field(..., alias='date[1]')
    origin_city_code_1: str = Field(..., alias='origin-city-code[1]')
    destination_city_code_1: str = Field(..., alias='destination-city-code[1]')
    
    # Пассажиры
    adultsCount: int = Field(default=1, ge=1, le=9)
    childrenCount: int = Field(default=0, ge=0, le=9)
    childCount: int = Field(default=0, ge=0, le=9)
    infantsWithSeatCount: int = Field(default=0, ge=0, le=9)
    infantsWithoutSeatCount: int = Field(default=0, ge=0, le=9)
    
    @field_validator('date_0', 'date_1')
    @classmethod
    def validate_dates(cls, v):
        if isinstance(v, str):
            try:
                datetime.strptime(v, '%d.%m.%Y')
                return v
            except ValueError:
                raise ValueError('Дата должна быть в формате DD.MM.YYYY')
        elif isinstance(v, (date, datetime)):
            return v.strftime('%d.%m.%Y')
        else:
            raise ValueError('Неверный тип даты')
