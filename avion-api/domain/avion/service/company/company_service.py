from avion.config.config import current_config
from avion.service.company.model.company import Company
from avion.service.company.model.create_company_params import CreateCompanyParams
from avion.service.company.repository.company_repository import CompanyRepository
from avion.model.currency import Currency
from avion.service.profile.profile_service import ProfileService


class CompanyService:
    def __init__(self, company_repository: CompanyRepository = CompanyRepository(),
                 profile_service: ProfileService = ProfileService()):
        self._profile_service = profile_service
        self._company_repo = company_repository
        self._config = current_config

    def create_company(self, account_id: int, params: CreateCompanyParams) -> Company:
        if not self._profile_service.account_has_profile(account_id, params.owner_id):
            raise ValueError(f"Account '{account_id}' is not the owner of profile '{params.owner_id}'")

        self._profile_service.withdraw(params.owner_id, self._config.game.company_startup_cost)
        if self._config.game.transfer_company_startup_cost:
            params.balance = self._config.game.company_startup_cost

        # Need to refund profile balance if this fails.
        return self._company_repo.create(params)

    def withdraw(self, company_id: int, amount: Currency) -> None:
        company = self._company_repo.get_company_by_id(company_id)
        if company.balance < amount:
            raise ValueError("Insufficient funds")
        company.balance -= amount
        self._company_repo.save(company)
