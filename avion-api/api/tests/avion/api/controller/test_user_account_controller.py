from http import HTTPStatus
from typing import Any, Dict, cast
from unittest import TestCase

from avion.testutils.flask_test_client import FlaskTestClient


class TestUserAccountController(TestCase):
    def setUp(self) -> None:
        self.client = FlaskTestClient()

    def test_account_can_be_created(self) -> None:
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
            "password": "secret"
        }
        response = self.client.post("/account", payload)
        json = cast(Dict[str, Any], response.json)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(payload.get("firstname"), json["firstname"])

    def test_BadRequest_is_returned_when_payload_is_invalid(self) -> None:
        payload = {"invalid": "payload"}
        response = self.client.post("/account", payload)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertIn("Missing data for required field.", response.text)

    def test_something_returned_when_user_is_duplicate(self) -> None:
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
            "password": "secret"
        }
        response = self.client.post("/account", payload)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = self.client.post("/account", payload)
        json = cast(Dict[str, Any], response.json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertIn(f"Username {payload.get('email')} already exist", json["error"])
