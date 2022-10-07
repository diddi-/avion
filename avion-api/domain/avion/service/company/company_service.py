from avion.model.company import Company
from avion.parameters.create_company_params import CreateCompanyParams
from avion.repository.company_repository import CompanyRepository
from avion.repository.profile_repository import ProfileRepository


class CompanyService:
    def __init__(self, company_repository: CompanyRepository = CompanyRepository(),
                 profile_repository: ProfileRepository = ProfileRepository()):
        self._profile_repo = profile_repository
        self._company_repo = company_repository

    def create_company(self, account_id: int, params: CreateCompanyParams) -> Company:
        if not self._profile_repo.account_has_profile(account_id, params.owner_id):
            raise ValueError(f"Account '{account_id}' is not the owner of profile '{params.owner_id}'")

        return self._company_repo.create(params)
