class JWTServiceError(Exception):
    pass

class CredentialError(JWTServiceError):
    def __init__(self):
        super().__init__('Could not validate credentials')

class InvalidPayloadError(JWTServiceError):
    def __init__(self):
        super().__init__("Invalid user's payload")

class ExpiredCredentialError(JWTServiceError):
    def __init__(self):
        super().__init__('Token is expired')

class RefreshNotFoundError(JWTServiceError):
    def __init__(self):
        super().__init__('Refresh token was not found')