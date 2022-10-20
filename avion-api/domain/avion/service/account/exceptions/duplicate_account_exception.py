class DuplicateAccountException(Exception):
    """ Indicates that a user already exists and can't be created again. """

    def __init__(self, username: str):
        super().__init__(f"Username {username} already exist")
