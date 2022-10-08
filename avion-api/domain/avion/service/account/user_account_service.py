from flask_jwt_extended import create_access_token

from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.model.hashed_password import HashedPassword
from avion.service.account.model.jwt_access_token import JwtAccessToken
from avion.service.account.model.login_request import LoginRequest
from avion.service.account.model.login_response import LoginResponse
from avion.service.account.model.user_account import UserAccount
from avion.service.account.repository.user_account_repository import UserAccountRepository


class UserAccountService:
    def __init__(self, repository: UserAccountRepository = UserAccountRepository()):
        self._repository = repository

    def register(self, params: CreateUserAccountParams) -> UserAccount:
        password = HashedPassword(params.password)
        params.password = None  # Don't want to accidentally pass the cleartext around
        return self._repository.create(params, password)

    def login(self, request: LoginRequest) -> LoginResponse:
        salt = self._repository.get_salt(request.username)
        password = HashedPassword(request.password, salt)
        request.password = None  # Don't want to accidentally pass the cleartext around
        if not self._repository.validate_credentials(request.username, password):
            raise ValueError("Invalid credentials")
        return LoginResponse(create_access_token(identity=request.username))

    def parse_token(self, string_token: str) -> JwtAccessToken:
        return JwtAccessToken.from_string(string_token)
