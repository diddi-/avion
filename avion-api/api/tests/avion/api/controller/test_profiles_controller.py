from http import HTTPStatus
from typing import cast, Dict
from unittest import TestCase

from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.user_account_service import UserAccountService
from avion.testutils.flask_test_client import FlaskTestClient


class TestProfilesController(TestCase):

    def setUp(self) -> None:
        self.client = FlaskTestClient()
        self.account_service = self.client.container.get_instance(UserAccountService)

    def test_profile_can_be_created_after_loggging_in(self) -> None:
        password = "secret"
        user = self.account_service.register(CreateUserAccountParams("John", "Doe", "john@example.com", password))
        profile_params = {
            "firstname": "Captain",
            "lastname": "Sunglasses"
        }
        self.client.login(user.username, password)
        response = self.client.post("/profiles", profile_params)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_Unauthorized_is_returned_when_attempting_to_create_profile_without_logging_in(self) -> None:
        profile_params = {"firstname": "Captain", "lastname": "Sunglasses"}
        response = self.client.post("/profiles", profile_params)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_BadRequest_is_returned_when_attempting_to_create_profile_with_invalid_payload(self) -> None:
        password = "secret"
        user = self.account_service.register(CreateUserAccountParams("John", "Doe", "john@example.com", password))
        self.client.login(user.username, password)
        response = self.client.post("/profiles", {"this": "that"})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertIn("Missing data for required field", response.text)

    def test_BadRequest_is_returned_when_attempting_to_create_two_profiles_with_same_names(self) -> None:
        password = "secret"
        user = self.account_service.register(CreateUserAccountParams("John", "Doe", "john@example.com", password))
        self.client.login(user.username, password)
        profile_params = {"firstname": "Captain", "lastname": "Sunglasses"}

        response = self.client.post("/profiles", profile_params)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = self.client.post("/profiles", profile_params)
        json = cast(Dict[str, str], response.json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertIn("Profile already exist", json["error"])
