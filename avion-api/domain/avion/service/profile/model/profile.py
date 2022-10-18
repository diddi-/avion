import datetime
from typing import Optional, List, Dict, Tuple

from avion.service.company.model.company_role import CompanyRole


class Profile:
    """ A Profile represents an in-game person with its details. This is different
    from a User Account in that a User may play using several Profiles. """
    def __init__(self, profile_id: int, firstname: str, lastname: str):
        self._id = profile_id
        self._created_at: Optional[datetime.datetime] = None
        self._owner_id: Optional[int] = None
        self._firstname = firstname
        self._lastname = lastname
        self._balance = 0
        self._company_roles: Dict[int, List[CompanyRole]] = {}

    def has_company_role(self, company_id: int, roles: List[CompanyRole]) -> bool:
        """ Returns True if the Profile has at least one of the supplied roles. """
        if company_id not in self._company_roles.keys():
            return False
        for role in roles:
            if role in self._company_roles[company_id]:
                return True
        return False

    def add_company_role(self, company_id: int, role: CompanyRole) -> None:
        if company_id not in self._company_roles.keys():
            self._company_roles[company_id] = []
        self._company_roles[company_id].append(role)

    @property
    def roles(self) -> List[Tuple[int, CompanyRole]]:
        roles = []
        for company_id, company_roles in self._company_roles.items():
            for role in company_roles:
                roles.append((company_id, role))
        return roles

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, value: str) -> None:
        self._firstname = value

    @property
    def lastname(self) -> str:
        return self._lastname

    @lastname.setter
    def lastname(self, value: str) -> None:
        self._lastname = value

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @property
    def owner_id(self) -> Optional[int]:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: int) -> None:
        self._owner_id = value

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        self._balance = value
