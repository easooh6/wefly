import bcrypt
import hashlib

def hash_password(password):
    # Конвертируем пароль в байты
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

def verify_hash(password, hashed_password):
    # Конвертируем пароль в байты
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Конвертируем хеш в байты, так как он был сохранен как строка
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

def hash_token(token: str):
    hashed_refresh = hashlib.sha256(token.encode()).hexdigest()
    return hashed_refresh