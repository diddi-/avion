from avion.service.company.company_service import CompanyService
from avion.service.company.model.company_role import CompanyRole
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
            raise ValueError("Account doesn't have access to profile.")

        profile = self._profile_service.get_profile(profile_id)
        if not profile.has_company_role(company_id, CompanyRole.FLEET_MGMT):
            raise ValueError(f"Unauthorized action")

        self._repository.add_to_fleet(company_id, aircraft_model_id)
