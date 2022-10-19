from http import HTTPStatus
from unittest import TestCase

from avion.testutils.flask_test_client import FlaskTestClient


class TestLoginController(TestCase):
    def setUp(self) -> None:
        self.client = FlaskTestClient()

    def test_login_returns_Unauthorized_when_wrong_credentials_are_entered(self) -> None:
        response = self.client.post("/login", {"username": "john@example.com", "password": "secret"})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_successful_login(self) -> None:
        response = self.client.post("/login", {"username": "admin", "password": "admin"})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("token", response.json.keys())

    def test_login_returns_BadRequest_when_invalid_payload_is_passed(self) -> None:
        response = self.client.post("/login", {"this": "that"})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
