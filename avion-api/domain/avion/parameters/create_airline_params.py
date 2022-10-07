from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateAirlineParams:
    name: str
    owner_id: Optional[int] = None
