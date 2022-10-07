from avion.config.config import current_config
from avion.model.company import Company
from avion.parameters.create_company_params import CreateCompanyParams
from avion.repository.company_repository import CompanyRepository
from avion.service.profile.profile_service import ProfileService


class CompanyService:
    def __init__(self, company_repository: CompanyRepository = CompanyRepository(),
                 profile_repository: ProfileService = ProfileService()):
        self._profile_service = profile_repository
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
