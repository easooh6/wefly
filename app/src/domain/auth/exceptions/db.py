class DBServiceError(Exception):
    pass

class UserAlreadyExists(DBServiceError):
    def __init__(self):
        super().__init__("User's email is already registered")

class UserNotFound(DBServiceError):
    def __init__(self):
        super().__init__("User not found")