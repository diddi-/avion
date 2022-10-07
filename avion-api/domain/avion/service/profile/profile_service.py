from avion.model.profile import Profile
from avion.parameters.create_profile_params import CreateProfileParams
from avion.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository = ProfileRepository()):
        self._repository = repository

    def create_profile(self, params: CreateProfileParams) -> Profile:
        return self._repository.create(params)
