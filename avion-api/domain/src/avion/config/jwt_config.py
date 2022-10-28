from __future__ import annotations

import datetime
from configparser import SectionProxy
from typing import Optional


class JwtConfig:
    SECTION_NAME = "Jwt"

    def __init__(self) -> None:
        self._access_token_lifetime = datetime.timedelta(hours=1)
        self._issuer: Optional[str] = None
        self._secret_key = "1234567890secret"

    @staticmethod
    def from_section(section: SectionProxy) -> JwtConfig:
        config = JwtConfig()
        config.secret_key = section["SecretKey"]
        config.access_token_lifetime = datetime.timedelta(seconds=float(section["AccessTokenLifetimeSeconds"]))
        config.issuer = section["Issuer"]
        return config

    @property
    def access_token_lifetime(self) -> datetime.timedelta:
        return self._access_token_lifetime

    @access_token_lifetime.setter
    def access_token_lifetime(self, value: datetime.timedelta) -> None:
        self._access_token_lifetime = value

    @property
    def secret_key(self) -> str:
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value: str) -> None:
        self._secret_key = value

    @property
    def issuer(self) -> Optional[str]:
        return self._issuer

    @issuer.setter
    def issuer(self, value: Optional[str]) -> None:
        self._issuer = value
