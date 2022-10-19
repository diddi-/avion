from http import HTTPStatus
from unittest import TestCase

import pytest
from mockito import mock, when, ANY

from avion.service.account.exceptions.login_failed_exception import LoginFailedException
from avion.service.account.model.login_request import LoginRequest
from avion.testutils.flask_client import FlaskClient


class TestLoginController(TestCase):
    def setUp(self) -> None:
        self.client = FlaskClient()

    @pytest.skip("Waiting for DI support")
    def test_login_returns_Unauthorized_when_wrong_credentials_are_entered(self) -> None:
        stubbed_service = mock()
        when(stubbed_service).login(ANY(LoginRequest)).thenRaise(LoginFailedException)
        response = self.client.post("/login", {"username": "john@example.com", "password": "secret"})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
