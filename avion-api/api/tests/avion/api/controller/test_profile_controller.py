from http import HTTPStatus
from typing import cast, Dict, Any
from unittest import TestCase

from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.user_account_service import UserAccountService
from avion.testutils.flask_test_client import FlaskTestClient


class TestProfileController(TestCase):

    def setUp(self) -> None:
        self.client = FlaskTestClient()
        self.account_service = self.client.container.get_instance(UserAccountService)

    def test_active_profile_can_be_retrieved(self) -> None:
        password = "secret"
        user = self.account_service.register(CreateUserAccountParams("John", "Doe", "john@example.com", password))
        profile_params = {"firstname": "Captain", "lastname": "Sunglasses"}
        self.client.login(user.username, password)
        response = self.client.post("/profiles", profile_params)
        self.client.switch_profile(int(cast(Dict[str, Any], response.json)["id"]))
        response = self.client.get("/profile")
        profile = cast(Dict[str, Any], response.json)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(profile_params["firstname"], profile["firstname"])
        self.assertEqual(profile_params["lastname"], profile["lastname"])
