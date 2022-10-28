import json
from unittest import TestCase

from mockito import mock

from avion.api.controller.status_controller import StatusController


class TestStatusController(TestCase):

    def setUp(self) -> None:
        self.stubbed_request = mock()
        self.tested_controller = StatusController(self.stubbed_request)

    def test_status_returns_OK(self) -> None:
        response = self.tested_controller.get()
        res = json.loads(response.content)
        self.assertEqual("OK", res["status"])
