from enum import Enum


class EngineType(Enum):
    PISTON = "piston"
    JET = "jet"
    TURBO_PROP = "turboprop"
    ELECTRIC = "electric"
    GLIDER = "glider"

    def __str__(self) -> str:
        return self.value
