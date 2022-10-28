from dataclasses import dataclass


@dataclass
class CreateCompanyParams:
    name: str
    balance: int = 0
