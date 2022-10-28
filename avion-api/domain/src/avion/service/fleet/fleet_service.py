from avion.service.company.company_service import CompanyService
from avion.service.company.model.company_role import CompanyRole
from avion.service.fleet.exceptions.no_registration_found_exception import NoRegistrationFoundException
from avion.service.fleet.model.aircraft import Aircraft
from avion.service.fleet.model.aircraft_registration import AircraftRegistration
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

    def register_aircraft(self, aircraft_id: int) -> AircraftRegistration:
        # For now we'll just assign N#### registrations. Will be based on country and type later.
        # https://en.wikipedia.org/wiki/List_of_aircraft_registration_prefixes
        aircraft = self._repository.get_aircraft_by_id(aircraft_id)
        try:
            latest = self._repository.get_latest_registration()
        except NoRegistrationFoundException:
            latest = AircraftRegistration("N", 0)
        aircraft.registration = AircraftRegistration(latest.prefix, latest.identifier + 1)
        self._repository.save(aircraft)
        return aircraft.registration

    def buy_aircraft(self, profile: Profile, company_id: int, aircraft_model_id: int) -> Aircraft:
        if not profile.has_company_role(company_id, [CompanyRole.CEO, CompanyRole.FLEET_MGMT]):
            raise ValueError("Unauthorized action")

        model = self._repository.get_aircraft_model_by_id(aircraft_model_id)
        self._company_service.withdraw(company_id, model.price)

        # Really should return money if saving fails.
        aircraft = self._repository.add_to_fleet(company_id, aircraft_model_id)
        aircraft.registration = self.register_aircraft(aircraft.id)
        return aircraft
