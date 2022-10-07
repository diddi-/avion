from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateProfileParams:
    firstname: str
    lastname: str
    owner_id: Optional[int] = None
