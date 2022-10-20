from http import HTTPStatus
from typing import cast, Dict, Any
from unittest import TestCase

from avion.testutils.flask_test_client import FlaskTestClient


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.client = FlaskTestClient()

    def test_account_can_login_after_registration(self) -> None:
        account_params = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
            "password": "secret"
        }
        login_params = {
            "username": account_params["email"],
            "password": account_params["password"]
        }

        response = self.client.post("/account", account_params)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = self.client.post("/login", login_params)
        json = cast(Dict[str, Any], response.json)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("token", json.keys())
