from src.infrastructure.redis.redis_limiter import RedisLimiter
from fastapi import Depends
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.dto.response.email_code import EmailCodeDTO
from src.domain.auth.exceptions.exceptions_email import WrongVerificationCodeError, VerificationCodeTimeExceeded


class VerifyEmailCode:

    def __init__(self, redis: RedisLimiter = Depends()):
        self.redis = redis


    async def verify_code(self, user: VerifyCodeDTO) -> EmailCodeDTO:
        code = await self.redis.get_code(user.email)
        if code != user.code:
            raise WrongVerificationCodeError

        if code is None:
            raise VerificationCodeTimeExceeded
        
        await self.redis.delete_code(user.email)
        
        return EmailCodeDTO(code=user.code)

        
    

        