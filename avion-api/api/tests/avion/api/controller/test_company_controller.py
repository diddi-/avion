from http import HTTPStatus
from typing import Any, Dict, cast
from unittest import TestCase

from avion.config.config import current_config
from avion.testutils.api_workflow import ApiWorkflow
from avion.testutils.flask_test_client import FlaskTestClient


class TestCompanyController(TestCase):
    def setUp(self) -> None:
        self.client = FlaskTestClient()
        self.flow = ApiWorkflow(self.client)

    def test_company_can_be_created(self) -> None:
        self.flow.register_account().login().create_profile()
        payload = {"name": "SAS"}
        response = self.client.post("/company", payload)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        json = cast(Dict[str, Any], response.json)
        self.assertEqual(payload["name"], json["name"])

    def test_BadRequest_is_returned_when_creating_company_with_invalid_payload(self) -> None:
        self.flow.register_account().login().create_profile()
        payload = {"this": "that"}
        response = self.client.post("/company", payload)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertIn("Missing data for required field", response.text)

    def test_BadRequest_is_returned_when_creating_company_with_duplicate_names(self) -> None:
        current_config.game.company_startup_cost = 0
        self.flow.register_account().login().create_profile()
        payload = {"name": "SAS"}
        response = self.client.post("/company", payload)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        response = self.client.post("/company", payload)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertIn(f"Company '{payload['name']}' already exist", response.text)
