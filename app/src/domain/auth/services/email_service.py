from src.infrastructure.auth.celery.email import send_verification_email
from src.infrastructure.auth.redis.redis_limiter import RedisLimiter
from src.domain.auth.dto.request.user_create import UserCreateDTO
from fastapi import Depends
from src.domain.auth.exceptions.email import RateLimitExceededError
from src.domain.auth.exceptions.db import UserAlreadyExists
from src.infrastructure.auth.redis.redis_user_store import RedisUserStore
from ..utils.code import random_code
from ..utils.hasher import hash_password
from src.infrastructure.db.repositories.user_crud import UserCRUD

class EmailService:

    def __init__(self, user: RedisUserStore, limiter: RedisLimiter,
                 crud: UserCRUD):
        self.limiter = limiter
        self.user = user
        self.crud = crud

    async def send_verification_code(self, email_dto: UserCreateDTO):

        if await self.crud.select_user(email_dto.email):
            raise UserAlreadyExists

        if await self.limiter.check_rate_limit(email_dto.email):
           
            verification_code = random_code()
            
            
            await self.limiter.save_code(email_dto.email, verification_code)

            plain_password = email_dto.password
            email_dto.password = hash_password(plain_password)
            
            email_dto.code = verification_code
            task = send_verification_email.delay(**email_dto.model_dump())

            
            await self.user.save_user_data(email_dto)
            
            return {'task_id': task.id}
    
        
        else:
            raise RateLimitExceededError