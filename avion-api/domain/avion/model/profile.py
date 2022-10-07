import datetime
from typing import Optional


class Profile:
    """ A Profile represents an in-game person with its details. This is different
    from a User Account in that a User may play using several Profiles. """
    def __init__(self, firstname: str, lastname: str):
        self._id: Optional[int] = None
        self._created_at: Optional[datetime.datetime] = None
        self._owner_id: Optional[int] = None
        self._firstname = firstname
        self._lastname = lastname

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
    def owner_id(self) -> Optional[int]:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: int) -> None:
        self._owner_id = value
