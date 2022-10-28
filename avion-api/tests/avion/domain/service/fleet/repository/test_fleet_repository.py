from unittest import TestCase

from avion.domain.service.company.model.create_company_params import CreateCompanyParams
from avion.domain.service.company.repository.company_repository import CompanyRepository
from avion.domain.service.fleet.model.create_aircraft_model_params import CreateAircraftModelParams
from avion.domain.service.fleet.repository.fleet_repository import FleetRepository
from avion.domain.testutils.db_initializer import DbInitializer


class TestFleetRepository(TestCase):
    def setUp(self) -> None:
        self.initializer = DbInitializer()
        self.initializer.run()
        self.tested_repository = FleetRepository(database=self.initializer.db_path)
        self.company_repository = CompanyRepository(database=self.initializer.db_path)

    def test_aircraft_model_can_be_created(self) -> None:
        params = CreateAircraftModelParams("Cessna", "172 Skyhawk", "C172")
        model = self.tested_repository.create_aircraft_model(params)
        self.assertIsNotNone(model.id)

    def test_aircraft_can_be_added_to_fleet(self) -> None:
        params = CreateAircraftModelParams("Cessna", "172 Skyhawk", "C172")
        model = self.tested_repository.create_aircraft_model(params)
        company = self.company_repository.create(123, CreateCompanyParams("SAS", 1))
        assert company.id is not None  # Mypy..
        assert model.id is not None  # Mypy..
        self.tested_repository.add_to_fleet(company.id, model.id)
