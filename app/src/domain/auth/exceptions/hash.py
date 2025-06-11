class WrongPasswordError(Exception):
    def __init__(self):
        super().__init__("Password not correct")
