import pytest
from src.domain.auth.services.verify_email import VerifyEmailCode
from unittest.mock import AsyncMock
from src.domain.auth.dto.request.verify_code import VerifyCodeDTO
from src.domain.auth.dto.response.email_code import EmailCodeDTO
from src.domain.auth.exceptions.email import WrongVerificationCodeError, VerificationCodeTimeExceeded

@pytest.mark.unit
@pytest.mark.asyncio
async def test_verify_email():
    mock_redis = AsyncMock()

    verify_code = VerifyCodeDTO(email='test@email.com', code=123456)

    mock_redis.get_code.return_value = 123456

    service = VerifyEmailCode(mock_redis)
    result = await service.verify_code(verify_code)

    assert isinstance(result, EmailCodeDTO)

    assert result.code == verify_code.code
    mock_redis.delete_code.assert_awaited_once_with(verify_code.email)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_verify_email_exceeded():
    
    mock_redis = AsyncMock()

    verify_code = VerifyCodeDTO(email='test@email.com', code=123456)

    mock_redis.get_code.return_value = None

    service = VerifyEmailCode(mock_redis)

    with pytest.raises(VerificationCodeTimeExceeded):
        await service.verify_code(verify_code)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_verify_email_invalid_code():
    mock_redis = AsyncMock()

    mock_redis.get_code.return_value = 999999

    verify_code = VerifyCodeDTO(email='test@email.com', code = 123456)

    service = VerifyEmailCode(mock_redis)

    with pytest.raises(WrongVerificationCodeError):
        await service.verify_code(verify_code)

