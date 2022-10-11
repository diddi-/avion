

class NoRegistrationFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("No registration found")
