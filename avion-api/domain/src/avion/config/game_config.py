from __future__ import annotations

from configparser import SectionProxy


class GameConfig:
    SECTION_NAME = "Game"

    def __init__(self) -> None:
        self._default_profile_start_money = 50000
        self._company_startup_cost = 50000
        self._transfer_company_startup_cost = True

    @staticmethod
    def from_section(section: SectionProxy) -> GameConfig:
        config = GameConfig()
        if "DefaultProfileStartMoney" in section:
            config.default_profile_start_money = int(section.get("DefaultProfileStartMoney"))
        if "CompanyStartupCost" in section:
            config.company_startup_cost = int(section.get("CompanyStartupCost"))
        if "TransferCompanyStartupCost" in section:
            config.transfer_company_startup_cost = section.getboolean("TransferCompanyStartupCost")
        return config

    @property
    def default_profile_start_money(self) -> int:
        return self._default_profile_start_money

    @default_profile_start_money.setter
    def default_profile_start_money(self, value: int) -> None:
        self._default_profile_start_money = value

    @property
    def transfer_company_startup_cost(self) -> bool:
        return self._transfer_company_startup_cost

    @transfer_company_startup_cost.setter
    def transfer_company_startup_cost(self, value: bool) -> None:
        self._transfer_company_startup_cost = value

    @property
    def company_startup_cost(self) -> int:
        return self._company_startup_cost

    @company_startup_cost.setter
    def company_startup_cost(self, value: int) -> None:
        self._company_startup_cost = value
