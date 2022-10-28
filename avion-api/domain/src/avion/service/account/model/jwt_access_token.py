from __future__ import annotations
from typing import Optional

from flask_jwt_extended import decode_token


class JwtAccessToken:
    def __init__(self) -> None:
        self._sub: Optional[str] = None
        self._iss: Optional[str] = None

    @staticmethod
    def from_string(string_token: str) -> JwtAccessToken:
        decoded = decode_token(string_token)
        token = JwtAccessToken()
        token.sub = decoded.get("sub", None)
        token.iss = decoded.get("iss", None)
        return token

    @property
    def sub(self) -> Optional[str]:
        return self._sub

    @sub.setter
    def sub(self, value: str) -> None:
        self._sub = value

    @property
    def iss(self) -> Optional[str]:
        return self._iss

    @iss.setter
    def iss(self, value: Optional[str]) -> None:
        self._iss = value
