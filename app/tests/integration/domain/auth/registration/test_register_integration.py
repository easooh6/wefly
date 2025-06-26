from src.domain.auth.services.register import RegisterService
from src.infrastructure.auth.redis.redis_user_store import RedisUserStore
from src.infrastructure.db.repositories.user_crud import UserCRUD
from src.domain.auth.services.verify_email import VerifyEmailCode
import pytest
from src.infrastructure.db.models.user_model import User
from src.infrastructure.auth.redis.redis_limiter import RedisLimiter
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.dto.request.user_create import UserCreateDTO
from src.domain.auth.dto.response.created_user import CreatedUserDTO
from src.domain.auth.exceptions.email import VerificationCodeTimeExceeded, WrongVerificationCodeError
from src.domain.auth.exceptions.db import UserAlreadyExists

@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_user(db_session, clean_redis):

    redis_limiter = RedisLimiter(clean_redis)
    service_email = VerifyEmailCode(redis_limiter)
    user = UserCRUD(db_session)
    redis_service = RedisUserStore(clean_redis)

    service = RegisterService(service_email, user, redis_service)

    dto = VerifyCodeDTO(email='test@email.com', code=123456)
    user_dto = UserCreateDTO(name='test',email='test@email.com',password='testpass',code=123456)
    
    await redis_service.save_user_data(user_dto)
    await redis_limiter.save_code(email=dto.email, code=dto.code)

    result = await service.register_user(dto)

    assert isinstance(result, CreatedUserDTO)
    assert await user.select_user(dto.email) is not None

@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_user_exceeded(db_session, clean_redis):
    redis_limiter = RedisLimiter(clean_redis)
    service_email = VerifyEmailCode(redis_limiter)
    user = UserCRUD(db_session)
    redis_service = RedisUserStore(clean_redis)

    service = RegisterService(service_email, user, redis_service)
    dto = VerifyCodeDTO(email='test@email.com', code=123456)

    with pytest.raises(VerificationCodeTimeExceeded):
        await service.register_user(dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_user_wrong_code(db_session, clean_redis):
    redis_limiter = RedisLimiter(clean_redis)
    service_email = VerifyEmailCode(redis_limiter)
    user = UserCRUD(db_session)
    redis_service = RedisUserStore(clean_redis)

    service = RegisterService(service_email, user, redis_service)
    dto = VerifyCodeDTO(email='test@email.com', code=123456)

    await redis_limiter.save_code(dto.email,654321)

    with pytest.raises(WrongVerificationCodeError):
        await service.register_user(dto)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_user_already_exists(db_session, clean_redis):
    redis_limiter = RedisLimiter(clean_redis)
    service_email = VerifyEmailCode(redis_limiter)
    user = UserCRUD(db_session)
    redis_service = RedisUserStore(clean_redis)

    service = RegisterService(service_email, user, redis_service)

    user_model = User(name='test', email='test@email.com', hashed_password= 'testpass')
    dto = VerifyCodeDTO(email='test@email.com', code=123456)
    user_dto = UserCreateDTO(name='test',email='test@email.com',password='testpass',code=123456)
    
    await redis_service.save_user_data(user_dto)
    await redis_limiter.save_code(email=dto.email, code=dto.code)
    await user.add_user(user_model)

    with pytest.raises(UserAlreadyExists):
        await service.register_user(dto)






