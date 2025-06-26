from src.domain.auth.services.verify_email import VerifyEmailCode
import pytest
from src.infrastructure.auth.redis.redis_limiter import RedisLimiter
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.dto.response.email_code import EmailCodeDTO
from src.infrastructure.common.redis.settings_redis import settings
import redis.asyncio as redis
from src.domain.auth.exceptions.email import WrongVerificationCodeError, VerificationCodeTimeExceeded

@pytest.mark.integration
@pytest.mark.asyncio
async def test_verify_email(clean_redis):
        
    redis_limiter = RedisLimiter(clean_redis)
    service = VerifyEmailCode(redis_limiter)

    dto = VerifyCodeDTO(email='test@email.com',code=123456)

    await redis_limiter.save_code(email=dto.email, code=dto.code)
    result = await service.verify_code(dto)

    assert isinstance(result,EmailCodeDTO)

    assert result.code == dto.code
    assert result.success == True
    assert await redis_limiter.get_code(dto.email) is None

@pytest.mark.integration
@pytest.mark.asyncio
async def test_verify_email_exceeded(clean_redis):
    redis_limiter = RedisLimiter(clean_redis)
    service = VerifyEmailCode(redis_limiter)
    dto = VerifyCodeDTO(email='test@email.com',code=123456)

    with pytest.raises(VerificationCodeTimeExceeded):
        await service.verify_code(dto)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_verify_email_invalid_code(clean_redis):
    
    redis_limiter = RedisLimiter(clean_redis)
    service = VerifyEmailCode(redis_limiter)
    dto = VerifyCodeDTO(email='test@email.com',code=123456)

    await redis_limiter.save_code(email=dto.email, code=654321)

    with pytest.raises(WrongVerificationCodeError):
        await service.verify_code(dto)