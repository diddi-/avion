from avion.service.company.company_service import CompanyService
from avion.service.fleet.repository.fleet_repository import FleetRepository
from avion.service.profile.profile_service import ProfileService


class FleetService:

    def __init__(self, repository: FleetRepository = FleetRepository(),
                 profile_service: ProfileService = ProfileService(),
                 company_service: CompanyService = CompanyService()):
        self._repository = repository
        self._profile_service = profile_service
        self._company_service = company_service

    def buy_aircraft(self, account_id: int, profile_id: int, company_id: int, aircraft_model_id: int) -> None:
        if not self._profile_service.account_has_profile(account_id, profile_id):
            raise ValueError(f"Account '{account_id}' is not allowed to perform action for profile '{profile_id}'")
        pass
