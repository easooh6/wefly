from src.infrastructure.parser.parser import ParseFly
from src.domain.parsing.dto.requests import SearchOneWayRequestDTO, SearchRoundTripRequestDTO
from src.domain.parsing.dto.responses import SearchResponseDTO, SearchResponseManyDTO
from src.domain.parsing.exceptions import APIRequestError, FlightNotFoundError, InvalidAPIResponseError
from fastapi import Depends
import logging

logger = logging.getLogger('wefly.fly_service')

class FlyService:
        
        def __init__(self, parser: ParseFly):
             self.parser = parser

        async def search_one_way(self, request: SearchOneWayRequestDTO) -> SearchResponseDTO | None:
            text = await self.parser.search_one_way(request)
            
            if text is None:
                raise APIRequestError

            if text.get('result') != 'ok':
                raise FlightNotFoundError
            
            try:

                flight = text.get("flights", [{}])[0].get("flights", [{}])[0]
                flight_id = flight.get("id")

                name = flight.get("company", {}).get("name")
                race_number = flight.get("racenumber")

                departuredate = flight.get('departuredate')
                departuretime = flight.get('departuretime')
                originport = flight.get('originport')
                origincityName = flight.get('origincityName')

                arrivaldate = flight.get('arrivaldate')
                arrivaltime = flight.get('arrivaltime')
                destinationport = flight.get('destinationport')
                destinationcityName = flight.get('destinationcityName')

                flighttime = flight.get('flighttime')

                price_list = text.get('prices', [{}])[0].get(str(flight_id), [])
                price_light = None
                price_optimal = None
                price_comfort = None
                flight_id = str(flight_id)
                if len(price_list) > 0 and price_list[0].get('price'):
                    try:
                        price_light = int(float(price_list[0].get('price')))
                    except (ValueError, TypeError):
                        pass
                    
                if len(price_list) > 1 and price_list[1].get('price'):
                    try:
                        price_optimal = int(float(price_list[1].get('price')))
                    except (ValueError, TypeError):
                        pass
                        
                if len(price_list) > 2 and price_list[2].get('price'):
                    try:
                        price_comfort = int(float(price_list[2].get('price')))
                    except (ValueError, TypeError):
                        pass

            except Exception as e:
                raise InvalidAPIResponseError

            text_dict = {
                'id': flight_id,
                'name': name,
                'racenumber': race_number,

                'departuredate': departuredate,
                'departuretime': departuretime,
                'originport': originport,
                'origincityName': origincityName,

                'arrivaldate': arrivaldate,
                'arrivaltime': arrivaltime,
                'destinationport': destinationport,
                'destinationcityName': destinationcityName,

                'flighttime': flighttime,

                'price_light': price_light,
                'price_optimal': price_optimal,
                'price_comfort': price_comfort
                    }
                
            return SearchResponseDTO(**text_dict)



        async def search_round_trip(self, request: SearchRoundTripRequestDTO) -> SearchResponseManyDTO | None:

            text = await self.parser.search_round_trip(request)

            if text is None:
                raise APIRequestError

            if text.get('result') != 'ok':
                raise FlightNotFoundError
            
            try:
                
                flights = text.get('flights')
                temp = []
                
                for one in flights:
                    
                    flight = one.get("flights", [{}])[0]  
                    flight_id = flight.get("id")

                    name = flight.get("company", {}).get("name")
                    race_number = flight.get("racenumber")

                    departuredate = flight.get('departuredate')
                    departuretime = flight.get('departuretime')
                    originport = flight.get('originport')
                    origincityName = flight.get('origincityName')

                    arrivaldate = flight.get('arrivaldate')
                    arrivaltime = flight.get('arrivaltime')
                    destinationport = flight.get('destinationport')
                    destinationcityName = flight.get('destinationcityName')

                    flighttime = flight.get('flighttime')

                  
                    price_light = None
                    price_optimal = None
                    price_comfort = None
                    
                    # ✅ Перебираем все объекты в массиве prices
                    prices_array = text.get('prices', [])
                    flight_id_str = str(flight_id)
                    
                    for price_obj in prices_array:
                        if flight_id_str in price_obj:
                            price_list = price_obj[flight_id_str]
                            
                            if len(price_list) > 0 and price_list[0].get('price'):
                                try:
                                    price_light = int(float(price_list[0].get('price')))
                                except (ValueError, TypeError):
                                    pass
                            
                            if len(price_list) > 1 and price_list[1].get('price'):
                                try:
                                    price_optimal = int(float(price_list[1].get('price')))
                                except (ValueError, TypeError):
                                    pass
                                    
                            if len(price_list) > 2 and price_list[2].get('price'):
                                try:
                                    price_comfort = int(float(price_list[2].get('price')))
                                except (ValueError, TypeError):
                                    pass
                            
                            break  # ✅ Нашли цены для этого рейса, выходим
                    
                    text_dict = {
                        'id': flight_id_str,
                        'name': name,
                        'racenumber': race_number,

                        'departuredate': departuredate,
                        'departuretime': departuretime,
                        'originport': originport,
                        'origincityName': origincityName,

                        'arrivaldate': arrivaldate,
                        'arrivaltime': arrivaltime,
                        'destinationport': destinationport,
                        'destinationcityName': destinationcityName,

                        'flighttime': flighttime,

                        'price_light': price_light,
                        'price_optimal': price_optimal,
                        'price_comfort': price_comfort
                            }
                    
                    temp.append(SearchResponseDTO(**text_dict))
                    
            except Exception as e:
                raise InvalidAPIResponseError

            return SearchResponseManyDTO(flights=temp)


