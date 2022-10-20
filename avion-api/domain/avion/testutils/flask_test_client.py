from http import HTTPStatus
from typing import Any, Dict, Optional, cast

from werkzeug.test import TestResponse

from avion.api.app import create_app
from avion.di.container import Container
from avion.service.account.repository.user_account_repository import UserAccountRepository
from avion.service.profile.repository.profile_repository import ProfileRepository
from avion.testutils.db_initializer import DbInitializer


class FlaskTestClient:
    def __init__(self) -> None:
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()
        self.db_initializer = DbInitializer()
        self.db_initializer.run(include_seeds=True)
        self.container = cast(Container, self.app.config.get("DIContainer"))
        self.container.resolve(UserAccountRepository).using(UserAccountRepository,
                                                            {"database": self.db_initializer.db_path})
        self.container.resolve(ProfileRepository).using(ProfileRepository,
                                                        {"database": self.db_initializer.db_path})
        self._access_token: Optional[str] = None

    def _request_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json"
        }
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        return headers

    def login(self, username: str, password: str) -> None:
        response = self.post("/login", {"username": username, "password": password})
        assert HTTPStatus.OK == response.status_code
        json = cast(Dict[str, str], response.json)
        self._access_token = json["token"]

    def get(self, path: str) -> TestResponse:
        return self.client.get(path, follow_redirects=True, headers=self._request_headers())

    def post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> TestResponse:
        return self.client.post(path, json=payload, headers=self._request_headers())
