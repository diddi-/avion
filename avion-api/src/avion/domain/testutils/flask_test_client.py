from http import HTTPStatus
from typing import Any, Dict, Optional, cast

from avion.api.app import create_app
from avion.domain.di.container import Container
from avion.domain.service.account.repository.user_account_repository import UserAccountRepository
from avion.domain.service.company.repository.company_repository import CompanyRepository
from avion.domain.service.profile.repository.profile_repository import ProfileRepository
from avion.domain.testutils.db_initializer import DbInitializer
from werkzeug.test import TestResponse


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
        self.container.resolve(CompanyRepository).using(CompanyRepository,
                                                        {"database": self.db_initializer.db_path})
        self._access_token: Optional[str] = None
        self._x_profile_id: Optional[int] = None

    def _request_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json"
        }
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"

        if self._x_profile_id:
            headers["X-PROFILE-ID"] = str(self._x_profile_id)
        return headers

    def switch_profile(self, profile_id: int) -> None:
        self._x_profile_id = profile_id

    def login(self, username: str, password: str) -> None:
        response = self.post("/login", {"username": username, "password": password})
        assert HTTPStatus.OK == response.status_code
        json = cast(Dict[str, str], response.json)
        self._access_token = json["token"]

    def get(self, path: str) -> TestResponse:
        return self.client.get(path, follow_redirects=True, headers=self._request_headers())

    def post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> TestResponse:
        return self.client.post(path, json=payload, headers=self._request_headers())
