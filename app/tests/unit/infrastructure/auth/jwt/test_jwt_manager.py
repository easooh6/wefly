from src.infrastructure.auth.JWT.jwt_manager import JWTManager
import pytest
import jwt
from datetime import datetime, timedelta
from src.domain.auth.dto.domain.jwt import TokenDTO
from src.domain.auth.exceptions.jwt import InvalidPayloadError,ExpiredCredentialError, CredentialError

@pytest.mark.parametrize('user_id, email, is_admin, token_type',
                         [
                             (1,'testemail@email.com', True, 'access'),
                             (2,'aboba@email.com',False, 'refresh')
                         ])
def test_create_access_token(user_id, email, is_admin, token_type):
    dto = TokenDTO(user_id=user_id, email=email, is_admin=is_admin, token_type=token_type)
    service = JWTManager()
    token = service.create_access_token(dto)
    assert isinstance(token,str)
    
    decoded = jwt.decode(token, service.secret_key, algorithms = [service.algorithm])
    
    assert decoded['user_id'] == user_id
    assert decoded['email'] == email
    assert decoded['is_admin'] == is_admin
    assert decoded['token_type'] == token_type
    assert 'exp' in decoded
    assert datetime.utcfromtimestamp(decoded["exp"]) > datetime.utcnow()

def test_decode_access_token_success():

    dto = TokenDTO(user_id = 1, email= 'testemail@email.com'
                   , is_admin=True, token_type='access')
    service = JWTManager()
    payload = {**dto.model_dump(), 'exp': datetime.utcnow() + timedelta(minutes=5)}

    token = jwt.encode(payload, service.secret_key, algorithm=service.algorithm)

    result = service.decode_token(token, 'access')

    assert result == dto


def test_decode_access_wrong_type():

    dto = TokenDTO(user_id = 1, email= 'testemail@email.com'
                   , is_admin=True, token_type='access')
    service = JWTManager()
    payload = {'user_id': 1, 'email': 'testemail@email.com'
                   ,'is_admin': True, 'token_type': 'access', 'exp': datetime.utcnow() + timedelta(minutes=5)}
    token = jwt.encode(payload, service.secret_key, algorithm=service.algorithm)

    with pytest.raises(CredentialError):
        service.decode_token(token, 'refresh')

def test_decode_access_invalid():

    service = JWTManager()
    payload = {'user_id': 1, 'token_type': 'access', 'exp': datetime.utcnow() + timedelta(minutes=5)}
    token = jwt.encode(payload, service.secret_key, algorithm=service.algorithm)

    with pytest.raises(InvalidPayloadError):
        service.decode_token(token, 'access')

def test_decode_access_expired():

    service = JWTManager()
    payload = {'user_id': 1, 'email': 'testemail@email.com'
                   ,'is_admin': True, 'token_type': 'access', 'exp': datetime.utcnow() - timedelta(minutes=5)}
    
    token = jwt.encode(payload, service.secret_key, algorithm=service.algorithm)

    with pytest.raises(ExpiredCredentialError):
        service.decode_token(token, 'access')





