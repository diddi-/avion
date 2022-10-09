

class Weight:
    def __init__(self, kilograms: int):
        if kilograms < 0:
            raise ValueError(f"{kilograms} is not a valid weight (kg)")
        self._kilograms = kilograms
        
    @property
    def kilograms(self) -> int:
        return self._kilograms
