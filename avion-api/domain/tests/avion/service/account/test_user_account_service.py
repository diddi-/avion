from unittest import TestCase

from mockito import when, mock

from avion.model.user_account import UserAccount
from avion.parameters.create_user_account_params import CreateUserAccountParams
from avion.service.account.user_account_service import UserAccountService


class TestUserAccountService(TestCase):

    def setUp(self) -> None:
        self.stubbed_repo = mock()
        self.tested_service = UserAccountService(repository=self.stubbed_repo)

    def test_user_account_is_returned_after_registration(self) -> None:
        params = CreateUserAccountParams("John", "Doe", "john@example.com")
        expected_account = UserAccount(params.firstname, params.lastname)
        expected_account.email = params.email
        when(self.stubbed_repo).create(params).thenReturn(expected_account)
        actual_account = self.tested_service.register(params)
        self.assertEqual(expected_account, actual_account)
