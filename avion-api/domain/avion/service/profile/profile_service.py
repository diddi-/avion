from avion.config.config import current_config
from avion.service.company.model.company_role import CompanyRole
from avion.service.profile.model.profile import Profile
from avion.service.profile.model.create_profile_params import CreateProfileParams
from avion.service.profile.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository = ProfileRepository()):
        self._repository = repository
        self._config = current_config

    def create_profile(self, params: CreateProfileParams) -> Profile:
        params.balance = self._config.game.default_profile_start_money
        return self._repository.create(params)

    def account_has_profile(self, account_id: int, profile_id: int) -> bool:
        return self._repository.account_has_profile(account_id, profile_id)

    def get_profile(self, profile_id: int) -> Profile:
        return self._repository.get_profile_by_id(profile_id)

    def add_company_role(self, profile_id: int, company_id: int, role: CompanyRole) -> None:
        profile = self._repository.get_profile_by_id(profile_id)
        profile.add_company_role(company_id, role)
        self._repository.save(profile)

    def withdraw(self, profile_id: int, amount: int) -> None:
        profile = self._repository.get_profile_by_id(profile_id)
        if profile.balance < amount:
            raise ValueError("Insufficient funds")

        profile.balance -= amount
        self._repository.save(profile)
