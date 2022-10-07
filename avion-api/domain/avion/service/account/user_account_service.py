import hashlib
import secrets
import string

from flask_jwt_extended import create_access_token

from avion.model.user_account import UserAccount
from avion.parameters.create_user_account_params import CreateUserAccountParams
from avion.repository.user_account_repository import UserAccountRepository
from avion.service.account.access_token import JwtAccessToken
from avion.service.account.login_request import LoginRequest
from avion.service.account.login_response import LoginResponse


class UserAccountService:
    def __init__(self, repository: UserAccountRepository = UserAccountRepository()):
        self._repository = repository

    def register(self, params: CreateUserAccountParams) -> UserAccount:
        alphabet = string.ascii_letters + string.digits
        salt = ''.join(secrets.choice(alphabet) for _ in range(20))
        hashed_password = hashlib.sha256(bytes(params.password + salt, "utf-8")).hexdigest()
        params.password = None  # Don't want to accidentally pass the cleartext around
        return self._repository.create(params, hashed_password, salt)

    def login(self, request: LoginRequest) -> LoginResponse:
        salt = self._repository.get_salt(request.username)
        hashed_password = hashlib.sha256(bytes(request.password + salt, "utf-8")).hexdigest()
        request.password = None  # Don't want to accidentally pass the cleartext around
        if not self._repository.validate_credentials(request.username, hashed_password):
            raise ValueError("Invalid credentials")
        return LoginResponse(create_access_token(identity=request.username))

    def parse_token(self, string_token: str) -> JwtAccessToken:
        return JwtAccessToken.from_string(string_token)
