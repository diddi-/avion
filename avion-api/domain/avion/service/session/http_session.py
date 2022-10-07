from flask_jwt_extended import get_jwt_identity

from avion.model.user_account import UserAccount
from avion.repository.user_account_repository import UserAccountRepository


# Rename to HttpContext?
class HttpSession:
    def __init__(self, repository: UserAccountRepository = UserAccountRepository()):
        self._repository = repository

    def get_current_user(self) -> UserAccount:
        return self._repository.get_user_by_username(get_jwt_identity())
