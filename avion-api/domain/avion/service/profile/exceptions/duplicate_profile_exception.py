
class DuplicateProfileException(Exception):
    def __init__(self, firstname: str, lastname: str) -> None:
        super().__init__(f"Profile already exist: {firstname} {lastname}")
