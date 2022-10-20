
class DuplicateCompanyException(Exception):
    """ Indicates that the name of a company is already in use and cannot be used again. """
    def __init__(self, name: str) -> None:
        super().__init__(f"Company '{name}' already exist")
