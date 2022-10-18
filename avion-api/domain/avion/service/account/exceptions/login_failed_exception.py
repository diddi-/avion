
class LoginFailedException(Exception):
    def __init__(self) -> None:
        super().__init__("Login failed")
