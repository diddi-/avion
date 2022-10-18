from avion.config.config import current_config
from avion.service.company.model.company import Company
from avion.service.company.model.company_role import CompanyRole
from avion.service.company.model.create_company_params import CreateCompanyParams
from avion.service.company.repository.company_repository import CompanyRepository
from avion.model.currency import Currency
from avion.service.profile.model.profile import Profile
from avion.service.profile.profile_service import ProfileService


class CompanyService:
    def __init__(self, company_repository: CompanyRepository = CompanyRepository(),
                 profile_service: ProfileService = ProfileService()):
        self._profile_service = profile_service
        self._company_repo = company_repository
        self._config = current_config

    def create_company(self, profile: Profile, params: CreateCompanyParams) -> Company:
        self._profile_service.withdraw(profile.id, self._config.game.company_startup_cost)
        if self._config.game.transfer_company_startup_cost:
            params.balance = self._config.game.company_startup_cost

        # Need to refund profile balance if this fails.
        company = self._company_repo.create(profile.id, params)
        self._profile_service.add_company_role(profile.id, company.id, CompanyRole.CEO)
        return company

    def withdraw(self, company_id: int, amount: Currency) -> None:
        company = self._company_repo.get_company_by_id(company_id)
        if company.balance < amount:
            raise ValueError("Insufficient funds")
        company.balance -= amount
        self._company_repo.save(company)
