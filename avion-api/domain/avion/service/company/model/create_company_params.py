from dataclasses import dataclass


@dataclass
class CreateCompanyParams:
    name: str
    owner_id: int  # Profile id!
    balance: int = 0
