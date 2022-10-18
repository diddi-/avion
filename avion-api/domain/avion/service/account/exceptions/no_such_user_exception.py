
class NoSuchUserException(Exception):
    def __init__(self) -> None:
        super().__init__("No such user")
