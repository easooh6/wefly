import pytest
from unittest.mock import AsyncMock
from src.domain.auth.services.register import RegisterService
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.dto.response.created_user import CreatedUserDTO
from src.domain.auth.dto.response.email_code import EmailCodeDTO
from src.domain.auth.dto.request.user_create import UserCreateDTO
from src.infrastructure.db.models.user_model import User

@pytest.mark.asyncio
async def test_register_user_success():

    mock_redis = AsyncMock()
    mock_email_service = AsyncMock()
    mock_user_repo = AsyncMock()

    verify_dto = VerifyCodeDTO(email="test@email.com", code="123456")

    temp_user = UserCreateDTO( 
        name="Test User",
        email="test@email.com",
        password="hashedpassword123",
        code="123456"
    )
    mock_redis.get_user_data.return_value = temp_user

    saved_user = User(  
        id=1,
        name=temp_user.name,
        email=temp_user.email,
        hashed_password=temp_user.password,
        created_at="2024-01-01 12:00:00"
    )
    mock_user_repo.add_user.return_value = saved_user

    service = RegisterService(
        redis=mock_redis,
        email_service=mock_email_service,
        user=mock_user_repo
    )

    result = await service.register_user(verify_dto)

    assert isinstance(result, CreatedUserDTO)
    assert result.id == saved_user.id
    assert result.email == saved_user.email

    mock_email_service.verify_code.assert_awaited_once_with(verify_dto)
    mock_redis.get_user_data.assert_awaited_once_with(verify_dto.email)
    mock_user_repo.add_user.assert_awaited_once()

