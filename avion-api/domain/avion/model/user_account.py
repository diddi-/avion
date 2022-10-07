import datetime
from typing import Optional


class UserAccount:
    """ A User Account represents a physical user and its personal details. """
    def __init__(self, firstname: str, lastname: str):
        self._id: Optional[int] = None
        self._created_at: Optional[datetime.datetime] = None
        self._firstname = firstname
        self._lastname = lastname
        self._email: Optional[str] = None
        self._username = self._email

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
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value
