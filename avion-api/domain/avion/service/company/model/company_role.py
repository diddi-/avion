from enum import Enum


class CompanyRole(Enum):
    FLEET_MGMT = "fleet_mgmt"
    HR = "hr"
    CEO = "ceo"

    def __str__(self) -> str:
        return self.value
