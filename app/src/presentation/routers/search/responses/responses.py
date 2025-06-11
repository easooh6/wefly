from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time
from typing import Optional, List, Dict, Any

class SearchResponse(BaseModel):

    id: str = Field(..., description="id рейса")
    name: str = Field(..., description="Название рейса")
    race_number: str = Field(..., alias="racenumber", description="Номер рейса")
    
    # Отправление
    departure_date: str = Field(..., alias="departuredate", description="Дата отправления")
    departure_time: str = Field(..., alias="departuretime", description="Время отправления")
    origin_port: str = Field(..., alias="originport", description="Аэропорт отправления")
    origin_city_name: str = Field(..., alias="origincityName", description="Город отправления")
    
    # Прибытие
    arrival_date: str = Field(..., alias="arrivaldate", description="Дата прибытия")
    arrival_time: str = Field(..., alias="arrivaltime", description="Время прибытия")
    destination_port: str = Field(..., alias="destinationport", description="Аэропорт назначения")
    destination_city_name: str = Field(..., alias="destinationcityName", description="Город назначения")
    
    # Дополнительная информация
    flight_time: str = Field(..., alias="flighttime", description="Время полета")
    price_light: Optional[int] = Field(None, alias="price_light", description="Базовый тариф")
    price_optimal: Optional[int] = Field(None, alias="price_optimal", description="Оптимальный тариф")
    price_comfort: Optional[int] = Field(None, alias="price_comfort", description="Комфорт тариф")
    
    @field_validator('race_number')
    @classmethod
    def validate_race_number(cls, v):
        """Валидация номера рейса"""
        return str(v).strip() if v else ""
    
    @field_validator('departure_date', 'arrival_date')
    @classmethod
    def validate_date_format(cls, v):
        """Валидация и нормализация формата даты"""
        if not v:
            raise ValueError("Дата не может быть пустой")
        
        # Если уже строка в правильном формате
        if isinstance(v, str):
            # Проверяем разные форматы входящих данных
            date_formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y']
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(v, fmt)
                    # Возвращаем в формате DD.MM.YYYY
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            raise ValueError(f"Неподдерживаемый формат даты: {v}")
        
        # Если datetime объект
        elif isinstance(v, datetime):
            return v.strftime('%Y-%m-%d')
        
        else:
            raise ValueError(f"Неверный тип даты: {type(v)}")
    
    @field_validator('departure_time', 'arrival_time')
    @classmethod
    def validate_time_format(cls, v):
        """Валидация и нормализация формата времени"""
        if not v:
            raise ValueError("Время не может быть пустым")
        
        # Если уже строка
        if isinstance(v, str):
            # Проверяем разные форматы времени
            time_formats = ['%H:%M', '%H.%M', '%H-%M']
            
            for fmt in time_formats:
                try:
                    parsed_time = datetime.strptime(v, fmt).time()
                    # Возвращаем в формате HH:MM
                    return parsed_time.strftime('%H:%M')
                except ValueError:
                    continue
            
            # Если формат уже правильный HH:MM
            if len(v.split(':')) == 2:
                hours, minutes = v.split(':')
                try:
                    h, m = int(hours), int(minutes)
                    if 0 <= h <= 23 and 0 <= m <= 59:
                        return f"{h:02d}:{m:02d}"
                except ValueError:
                    pass
            
            raise ValueError(f"Неподдерживаемый формат времени: {v}")
        
        # Если time объект
        elif isinstance(v, time):
            return v.strftime('%H:%M')
        
        else:
            raise ValueError(f"Неверный тип времени: {type(v)}")
    
    @field_validator('flight_time')
    @classmethod
    def validate_flight_time(cls, v):
        """Валидация времени полета"""
        if not v:
            return "00:00"
        
        if isinstance(v, str):
            # Проверяем формат HH:MM
            if ':' in v:
                try:
                    hours, minutes = v.split(':')
                    h, m = int(hours), int(minutes)
                    if h >= 0 and 0 <= m <= 59:
                        return f"{h:02d}:{m:02d}"
                except ValueError:
                    pass
            
            raise ValueError(f"Неверный формат времени полета: {v}")
        
        return str(v)
    
    @field_validator('origin_port', 'destination_port')
    @classmethod
    def validate_airport_code(cls, v):
        """Валидация кода аэропорта"""
        if not v:
            raise ValueError("Код аэропорта не может быть пустым")
        
        code = str(v).strip().upper()
        if len(code) != 3:
            raise ValueError(f"Код аэропорта должен содержать 3 символа: {code}")
        
        return code
    
    @field_validator('price_light', 'price_optimal', 'price_comfort')
    @classmethod
    def validate_price(cls, v):
        """Валидация цены"""
        if v is None:
            return None
        
        # Если строка, преобразуем в число
        if isinstance(v, str):
            try:
                # Убираем пробелы и запятые
                cleaned = v.replace(' ', '').replace(',', '')
                return int(float(cleaned))
            except ValueError:
                raise ValueError(f"Неверный формат цены: {v}")
        
        if isinstance(v, (int, float)):
            return int(v)
        
        raise ValueError(f"Неверный тип цены: {type(v)}")

    class Config:
        populate_by_name = True
        str_strip_whitespace = True
        validate_assignment = True

class SearchResponseMany(BaseModel):
    flights: List[SearchResponse]

    class Config:
        populate_by_name = True
