import datetime
from typing import Optional

from avion.model.currency import Currency


class Company:
    def __init__(self, company_id: int, name: str):
        self._id = company_id
        self._name = name
        self._created_at: Optional[datetime.datetime] = None
        self._owner_id: Optional[int] = None
        self._balance = Currency(0)

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

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

    @property
    def balance(self) -> Currency:
        return self._balance

    @balance.setter
    def balance(self, value: Currency) -> None:
        self._balance = value
