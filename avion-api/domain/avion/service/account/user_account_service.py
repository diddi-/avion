from avion.model.user_account import UserAccount
from avion.parameters.create_user_account_params import CreateUserAccountParams
from avion.repository.user_account_repository import UserAccountRepository


class UserAccountService:
    def __init__(self, repository: UserAccountRepository = UserAccountRepository()):
        self._repository = repository

    def register(self, params: CreateUserAccountParams) -> UserAccount:
        return self._repository.create(params)
