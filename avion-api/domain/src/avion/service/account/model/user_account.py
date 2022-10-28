import datetime
from typing import Any


class UserAccount:
    """ A User Account represents a physical user and its personal details. """
    # pylint: disable=too-many-arguments
    def __init__(self, account_id: int, firstname: str, lastname: str, email: str, username: str):
        self._id = account_id
        self._created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        self._firstname = firstname
        self._lastname = lastname
        self._email = email
        self._username = username

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, value: str) -> None:
        self._firstname = value

    @property
    def lastname(self) -> str:
        return self._lastname

    @lastname.setter
    def lastname(self, value: str) -> None:
        self._lastname = value

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, UserAccount) and other.username == self.username
