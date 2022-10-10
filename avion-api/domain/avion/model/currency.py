from __future__ import annotations
from typing import Any


class Currency:
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError(f"{amount} is not a valid amount of currency (min. 0)")
        self._amount = amount

    @property
    def amount(self) -> int:
        return self._amount

    def __int__(self) -> int:
        return self._amount

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Currency) and other.amount == self.amount

    def __gt__(self, other: Any) -> bool:
        return isinstance(other, Currency) and self.amount > other.amount

    def __lt__(self, other: Any) -> bool:
        return isinstance(other, Currency) and self.amount < other.amount

    def __add__(self, other: Any) -> Currency:
        if not isinstance(other, Currency):
            raise ValueError(f"{type(other)} is not a Currency")
        return Currency(self.amount + other.amount)

    def __sub__(self, other: Any) -> Currency:
        if not isinstance(other, Currency):
            raise ValueError(f"{type(other)} is not a Currency")
        return Currency(self.amount - other.amount)

    def __mul__(self, other: Any) -> Currency:
        if not isinstance(other, Currency):
            raise ValueError(f"{type(other)} is not a Currency")
        return Currency(self.amount * other.amount)

    def __truediv__(self, other: Any) -> Currency:
        if not isinstance(other, Currency):
            raise ValueError(f"{type(other)} is not a Currency")
        return Currency(int(self.amount / other.amount))
