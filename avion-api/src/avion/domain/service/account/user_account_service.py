from avion.domain.service.account.exceptions.login_failed_exception import LoginFailedException
from avion.domain.service.account.exceptions.no_such_user_exception import NoSuchUserException
from avion.domain.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.domain.service.account.model.hashed_password import HashedPassword
from avion.domain.service.account.model.jwt_access_token import JwtAccessToken
from avion.domain.service.account.model.login_request import LoginRequest
from avion.domain.service.account.model.login_response import LoginResponse
from avion.domain.service.account.model.user_account import UserAccount
from avion.domain.service.account.repository.user_account_repository import UserAccountRepository
from flask_jwt_extended import create_access_token


class UserAccountService:
    def __init__(self, repository: UserAccountRepository = UserAccountRepository()):
        self._repository = repository

    def register(self, params: CreateUserAccountParams) -> UserAccount:
        password = HashedPassword(params.password)
        return self._repository.create(params, password)

    def login(self, request: LoginRequest) -> LoginResponse:
        try:
            salt = self._repository.get_salt(request.username)
        except NoSuchUserException as e:
            raise LoginFailedException() from e

        password = HashedPassword(request.password, salt)
        if not self._repository.validate_credentials(request.username, password):
            raise LoginFailedException()

        # Having create_access_token here is not good. We do not want anything to do with Flask and its context here.
        return LoginResponse(create_access_token(identity=request.username))

    def parse_token(self, string_token: str) -> JwtAccessToken:
        return JwtAccessToken.from_string(string_token)
