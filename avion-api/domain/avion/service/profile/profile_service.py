from avion.config.config import current_config
from avion.model.profile import Profile
from avion.parameters.create_profile_params import CreateProfileParams
from avion.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository = ProfileRepository()):
        self._repository = repository
        self._config = current_config

    def create_profile(self, params: CreateProfileParams) -> Profile:
        params.balance = self._config.game.default_profile_start_money
        return self._repository.create(params)

    def account_has_profile(self, account_id: int, profile_id: int) -> bool:
        return self._repository.account_has_profile(account_id, profile_id)

    def withdraw(self, profile_id: int, amount: int):
        profile = self._repository.get_profile_by_id(profile_id)
        if profile.balance < amount:
            raise ValueError("Insufficient funds")

        profile.balance -= amount
        self._repository.save(profile)
