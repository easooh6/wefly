import pytest
from unittest.mock import AsyncMock, patch, Mock
from src.domain.auth.services.email_service import EmailService
from src.domain.auth.dto.request.user_create import UserCreateDTO
from src.infrastructure.db.models.user_model import User
from src.domain.auth.exceptions.db import UserAlreadyExists
from src.domain.auth.exceptions.email import RateLimitExceededError

@pytest.mark.unit
@pytest.mark.asyncio
@patch("src.domain.auth.services.email_service.send_verification_email")  # 👈 patch точку импорта
async def test_email_service(mock_send_email):
    # 1. Моки зависимостей
    mock_user = AsyncMock()
    mock_crud = AsyncMock()
    mock_limiter = AsyncMock()

    # 2. Поведение зависимостей
    mock_crud.select_user.return_value = None
    mock_limiter.check_rate_limit.return_value = True
    mock_send_email.delay.return_value = Mock(id="mocked-task-id")

    # 3. Подготовка данных
    dto = UserCreateDTO(name="test", email="test@email.com", password="password123", code=0)

    # 4. Сервис с зависимостями
    service = EmailService(user=mock_user, limiter=mock_limiter, crud=mock_crud)

    # 5. Вызов
    result = await service.send_verification_code(dto)

    # 6. Проверки
    assert result == {"task_id": "mocked-task-id"}
    mock_crud.select_user.assert_awaited_once_with(dto.email)
    mock_limiter.check_rate_limit.assert_awaited_once_with(dto.email)
    mock_limiter.save_code.assert_awaited_once()
    mock_send_email.delay.assert_called_once()
    mock_user.save_user_data.assert_awaited_once()

@pytest.mark.unit
@pytest.mark.asyncio
async def test_email_service_exists():

    mock_limiter = AsyncMock()
    mock_user = AsyncMock()
    mock_crud = AsyncMock()

    service = EmailService(mock_user, mock_limiter, mock_crud)

    mock_crud.select_user.return_value = User(  
        id=1,
        name='test',
        email='test@email.com',
        hashed_password='testpass',
        created_at="2024-01-01 12:00:00")
    
    dto = UserCreateDTO(name='test',
        email='test@email.com',
        password='testpass',
        code=0)

    with pytest.raises(UserAlreadyExists):
        await service.send_verification_code(dto)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_email_service_exceeded():

    mock_limiter = AsyncMock()
    mock_user = AsyncMock()
    mock_crud = AsyncMock()

    mock_limiter.check_rate_limit.return_value = False
    mock_crud.select_user.return_value = None

    service = EmailService(mock_user, mock_limiter, mock_crud)

    dto = UserCreateDTO(name='test',
        email='test@email.com',
        password='testpass',
        code=0)

    with pytest.raises(RateLimitExceededError):
        await service.send_verification_code(dto)