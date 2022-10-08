import unittest
from unittest import TestCase

from mockito import when, mock, ANY

from avion.service.account.exceptions.invalid_credentials_exception import InvalidCredentialsException
from avion.service.account.model.hashed_password import HashedPassword
from avion.service.account.model.jwt_access_token import JwtAccessToken
from avion.service.account.model.login_request import LoginRequest
from avion.service.account.model.user_account import UserAccount
from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.user_account_service import UserAccountService


class TestUserAccountService(TestCase):

    def setUp(self) -> None:
        self.stubbed_repo = mock()
        self.tested_service = UserAccountService(repository=self.stubbed_repo)

    def test_user_account_is_returned_after_registration(self) -> None:
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        expected_account = UserAccount(params.firstname, params.lastname, params.email, params.email)
        when(self.stubbed_repo).create(params, ANY(HashedPassword)).thenReturn(expected_account)
        actual_account = self.tested_service.register(params)
        self.assertEqual(expected_account, actual_account)

    def test_exception_is_raised_when_login_fails(self) -> None:
        request = LoginRequest("john@example.com", "secret")
        password = HashedPassword(request.password)
        when(self.stubbed_repo).get_salt(request.username).thenReturn(password.salt)
        when(self.stubbed_repo).validate_credentials(request.username, password).thenReturn(False)

        with self.assertRaises(InvalidCredentialsException):
            self.tested_service.login(request)

    @unittest.skip("Access token generation needs an active Flask context. Requires refactor.")
    def test_login_response_with_access_token_is_returned_on_successful_login(self) -> None:
        request = LoginRequest("john@example.com", "secret")
        password = HashedPassword(request.password)
        when(self.stubbed_repo).get_salt(request.username).thenReturn(password.salt)
        when(self.stubbed_repo).validate_credentials(request.username, password).thenReturn(True)

        expected_token = JwtAccessToken()
        expected_token.sub = "john@example.com"
        response = self.tested_service.login(request)
        self.assertEqual(expected_token.sub, JwtAccessToken.from_string(response.token).sub)
