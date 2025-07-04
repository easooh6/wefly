from src.infrastructure.auth.redis.redis_limiter import RedisLimiter
from fastapi import Depends
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.dto.response.email_code import EmailCodeDTO
from src.domain.auth.exceptions.email import WrongVerificationCodeError, VerificationCodeTimeExceeded


class VerifyEmailCode:

    def __init__(self, redis: RedisLimiter):
        self.redis = redis


    async def verify_code(self, user: VerifyCodeDTO) -> EmailCodeDTO:
        code = await self.redis.get_code(user.email)

        if code is None:
            raise VerificationCodeTimeExceeded
        
        if code != user.code:
            raise WrongVerificationCodeError
        
        await self.redis.delete_code(user.email)
        
        return EmailCodeDTO(code=user.code)

        
    

        