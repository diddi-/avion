from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateProfileParams:
    firstname: str
    lastname: str
    balance: int = 0
    owner_id: Optional[int] = None
