class EmailServiceError(Exception):
    """Базовый класс для ошибок email-сервиса"""
    pass

class RateLimitExceededError(EmailServiceError):
    """Превышен лимит запросов"""
    def __init__(self):
        super().__init__("Rate limit exceeded for email verification")

class WrongVerificationCodeError(EmailServiceError):
    def __init__(self):
        super().__init__('Wrong verifaction code was got from user')

class VerificationCodeTimeExceeded(EmailServiceError):
    def __init__(self):
        super().__init__("User's verification code time live exceeded")


