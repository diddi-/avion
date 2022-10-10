from avion.service.company.company_service import CompanyService
from avion.service.company.model.company_role import CompanyRole
from avion.service.fleet.repository.fleet_repository import FleetRepository
from avion.service.profile.model.profile import Profile
from avion.service.profile.profile_service import ProfileService


class FleetService:

    def __init__(self, repository: FleetRepository = FleetRepository(),
                 profile_service: ProfileService = ProfileService(),
                 company_service: CompanyService = CompanyService()):
        self._repository = repository
        self._profile_service = profile_service
        self._company_service = company_service

    def buy_aircraft(self, profile: Profile, company_id: int, aircraft_model_id: int) -> None:
        if not profile.has_company_role(company_id, [CompanyRole.CEO, CompanyRole.FLEET_MGMT]):
            raise ValueError("Unauthorized action")

        model = self._repository.get_aircraft_model_by_id(aircraft_model_id)
        self._company_service.withdraw(company_id, model.price)

        # Really should return money if saving fails.
        self._repository.add_to_fleet(company_id, aircraft_model_id)
