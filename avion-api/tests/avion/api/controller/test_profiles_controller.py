from http import HTTPStatus
from typing import cast, Dict, Any, List
from unittest import TestCase

from avion.domain.testutils.flask_test_client import FlaskTestClient

from avion.domain.service.account.user_account_service import UserAccountService

from avion.domain.service.account.model.create_user_account_params import CreateUserAccountParams


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

    def test_list_of_profiles_can_be_retrieved(self) -> None:
        password = "secret"
        user = self.account_service.register(CreateUserAccountParams("John", "Doe", "john@example.com", password))
        self.client.login(user.username, password)
        response = self.client.post("/profiles", {"firstname": "Captain", "lastname": "Sunglasses"})
        profile1_data = cast(Dict[str, Any], response.json)
        response = self.client.post("/profiles", {"firstname": "Jake", "lastname": "Peralta"})
        profile2_data = cast(Dict[str, Any], response.json)

        response = self.client.get("/profiles")
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json = cast(List[Dict[str, Any]], response.json)
        self.assertListEqual([profile1_data, profile2_data], json)

    def test_empty_list_is_returned_when_no_profiles_exist_for_user(self) -> None:
        password = "secret"
        user = self.account_service.register(CreateUserAccountParams("John", "Doe", "john@example.com", password))
        self.client.login(user.username, password)
        response = self.client.get("/profiles")
        profiles = cast(List[Dict[str, Any]], response.json)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertListEqual([], profiles)
