from http import HTTPStatus
from unittest import TestCase

from avion.testutils.flask_test_client import FlaskTestClient


class TestUserAccountController(TestCase):
    def setUp(self) -> None:
        self.client = FlaskTestClient()

    def test_account_can_be_created(self) -> None:
        response = self.client.post("/account", {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
            "password": "secret"
        })
        self.assertEqual(HTTPStatus.OK, response.status_code)
