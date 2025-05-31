import aiohttp
import asyncio
from src.domain.parsing.dto.requests import SearchOneWayRequestDTO, SearchRoundTripRequestDTO
import logging

logger = logging.getLogger('wefly.parser')

class ParseFly:
    """Асинхронный парсер"""
    
    _url = 'https://booking.flyqazaq.com/websky/json/search-variants-mono-brand-cartesian'
    
    def __init__(self):
        self._session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Ленивое создание сессии"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def search_one_way(self, search: SearchOneWayRequestDTO) -> dict | None:
        """Асинхронный поиск рейсов"""
        
        logger.info('Async searching for date %s, from %s to %s', 
                   search.date_0, search.origin_city_code_0, search.destination_city_code_0)

        incoming_data = search.model_dump(by_alias=True)

        try:
            session = await self._get_session()
            
            # ✅ Асинхронный POST запрос
            async with session.post(self._url, data=incoming_data) as response:
                logger.debug('Async request to %s, response: %s', self._url, response.status)
                
                if response.status != 200:
                    logger.error('HTTP error: %d', response.status)
                    return None
                
                # ✅ Асинхронное чтение JSON
                return await response.json()

        except aiohttp.ClientError as e:
            logger.error('Network error: %s', e)
            return None
        except asyncio.TimeoutError:
            logger.error('Request timeout')
            return None
        except ValueError as e:
            logger.error('JSON parsing error: %s', e)
            return None
        except Exception as e:
            logger.error('Unexpected error: %s', e)
            return None
    

    async def search_round_trip(self, search: SearchRoundTripRequestDTO) -> dict| None:
        
        logger.info('Async searching for first date %s, from %s to %s\n' \
            'for second date %s, from %s to %s', 
            search.date_0, search.origin_city_code_0, search.destination_city_code_0,
            search.date_1, search.origin_city_code_1, search.destination_city_code_1)

        incoming_data = search.model_dump(by_alias=True)

        try:
            session = await self._get_session()
            
            # ✅ Асинхронный POST запрос
            async with session.post(self._url, data=incoming_data) as response:
                logger.debug('Async request to %s, response: %s', self._url, response.status)
                
                if response.status != 200:
                    logger.error('HTTP error: %d', response.status)
                    return None
                
                # ✅ Асинхронное чтение JSON
                return await response.json()

        except aiohttp.ClientError as e:
            logger.error('Network error: %s', e)
            return None
        except asyncio.TimeoutError:
            logger.error('Request timeout')
            return None
        except ValueError as e:
            logger.error('JSON parsing error: %s', e)
            return None
        except Exception as e:
            logger.error('Unexpected error: %s', e)
            return None


    async def close(self):
        """Закрытие сессии"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


