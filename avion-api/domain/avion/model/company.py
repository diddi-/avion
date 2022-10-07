import datetime
from typing import Optional


class Company:
    def __init__(self, name: str):
        self._id: Optional[int] = None
        self._name = name
        self._created_at: Optional[datetime.datetime] = None
        self._owner_id: Optional[int] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, table_id: int) -> None:
        if self._id is not None:
            raise ValueError("Changing ID is not allowed")
        self._id = table_id

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        return self._created_at

    @created_at.setter
    def created_at(self, date: datetime.datetime) -> None:
        if self._created_at is not None:
            raise ValueError("Changing 'created at' is not allowed")
        self._created_at = date

    @property
    def owner_id(self) -> Optional[int]:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: Optional[int]) -> None:
        self._owner_id = value
