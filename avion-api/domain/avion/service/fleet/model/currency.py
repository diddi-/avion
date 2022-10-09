

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
