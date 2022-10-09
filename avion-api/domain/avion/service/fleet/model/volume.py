

class Volume:
    def __init__(self, liter: int):
        if liter < 0:
            raise ValueError(f"{liter} is not a valid volume (liter)")
        self._liter = liter

    @property
    def liter(self) -> int:
        return self._liter
