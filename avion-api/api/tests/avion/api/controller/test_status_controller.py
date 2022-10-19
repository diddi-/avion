import json
from unittest import TestCase

from avion.testutils.flask_client import FlaskClient


class TestStatusController(TestCase):

    def setUp(self) -> None:
        self.client = FlaskClient()

    def test_status_returns_OK(self) -> None:
        response = self.client.get("/status")
        res = json.loads(response.data.decode('utf-8'))
        self.assertEqual("OK", res["status"])
