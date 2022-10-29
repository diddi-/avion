from __future__ import annotations

from typing import Optional

from avion.domain.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.domain.service.account.model.user_account import UserAccount
from avion.domain.service.account.user_account_service import UserAccountService
from avion.domain.service.profile.model.create_profile_params import CreateProfileParams
from avion.domain.service.profile.model.profile import Profile
from avion.domain.service.profile.profile_service import ProfileService
from avion.domain.testutils.flask_test_client import FlaskTestClient


class ApiWorkflow:
    """ Simplify common workflows when working with the API. This is because Flask require an app context to exist
     to work in most cases, which in turn require a lot of operations to be made via the controllers rather than using
     services directly in tests. """

    def __init__(self, client: FlaskTestClient):
        self._client = client
        self._account: Optional[UserAccount] = None
        self._account_password: Optional[str] = None
        self._profile: Optional[Profile] = None

    def register_account(self, firstname: str = "John", lastname: str = "Doe", email: str = "john@example.com",
                         password: str = "secret") -> ApiWorkflow:
        service = self._client.container.get_instance(UserAccountService)
        self._account = service.register(CreateUserAccountParams(firstname, lastname, email, password))
        self._account_password = password
        return self

    def login(self, username: str = "john@example.com", password: str = "secret") -> ApiWorkflow:
        self._client.login(username, password)
        return self

    def create_profile(self, firstname: str = "Captain", lastname: str = "Sunglasses") -> ApiWorkflow:
        """ Create and automatically switch to using the new profile """
        service = self._client.container.get_instance(ProfileService)
        if self._account is None:
            raise ValueError("Can't create profile without first creating an account")
        self._profile = service.create_profile(CreateProfileParams(firstname, lastname, owner_id=self._account.id))
        self._client.switch_profile(self._profile.id)
        return self
