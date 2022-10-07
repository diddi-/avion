from dataclasses import dataclass


@dataclass
class CreateAirlineParams:
    name: str
    owner_id: int
