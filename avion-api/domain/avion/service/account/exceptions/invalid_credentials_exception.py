
class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Invalid credentials")
