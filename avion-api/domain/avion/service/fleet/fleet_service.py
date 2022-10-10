from avion.service.company.model.company_role import CompanyRole
from avion.service.fleet.repository.fleet_repository import FleetRepository
from avion.service.profile.model.profile import Profile
from avion.service.profile.profile_service import ProfileService


class FleetService:

    def __init__(self, repository: FleetRepository = FleetRepository(),
                 profile_service: ProfileService = ProfileService()):
        self._repository = repository
        self._profile_service = profile_service

    def buy_aircraft(self, profile: Profile, company_id: int, aircraft_model_id: int) -> None:
        if not profile.has_company_role(company_id, [CompanyRole.CEO, CompanyRole.FLEET_MGMT]):
            raise ValueError(f"Unauthorized action")

        # TODO: It costs money!
        self._repository.add_to_fleet(company_id, aircraft_model_id)
