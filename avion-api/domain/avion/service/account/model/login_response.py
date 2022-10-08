from dataclasses import dataclass


@dataclass
class LoginResponse:
    token: str
