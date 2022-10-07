from dataclasses import dataclass


@dataclass
class CreateCompanyParams:
    name: str
    owner_id: int
