from src.domain.auth.services.email_service import EmailService
import pytest
from src.infrastructure.auth.redis.redis_user_store import RedisUserStore
from src.infrastructure.auth.redis.redis_limiter import RedisLimiter
from src.infrastructure.db.repositories.user_crud import UserCRUD
from unittest.mock import patch, Mock
from src.domain.auth.dto.request.user_create import UserCreateDTO
from src.domain.auth.utils.hasher import verify_hash

@pytest.mark.integration
@pytest.mark.asyncio
@patch("src.domain.auth.services.email_service.send_verification_email.delay")
async def test_email_service(mock_email_service, db_session, clean_redis):
    
    user = RedisUserStore(clean_redis)
    limiter = RedisLimiter(clean_redis)
    crud = UserCRUD(db_session)

    dto = UserCreateDTO(
        name="TestUser",
        email="test@email.com",
        password="password123",
        code = 0
    )

    service = EmailService(user,limiter,crud)

    plain_password = dto.password

    result = await service.send_verification_code(dto)

    mock_email_service.assert_called_once_with(**dto.model_dump())


    assert 'task_id' in result
    assert await limiter.get_code(dto.email) is not None

    user_data = await user.get_user_data(dto.email)

    assert user_data is not None
    assert isinstance(user_data, UserCreateDTO)

    assert plain_password != user_data.password
    assert verify_hash(plain_password, user_data.password) is True

    assert user_data.code == await limiter.get_code(dto.email)