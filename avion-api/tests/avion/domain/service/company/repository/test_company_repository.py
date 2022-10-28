from unittest import TestCase

from avion.domain.service.company.exceptions.duplicate_company_exception import DuplicateCompanyException
from avion.domain.service.company.model.create_company_params import CreateCompanyParams
from avion.domain.service.company.repository.company_repository import CompanyRepository
from avion.domain.testutils.db_initializer import DbInitializer


class TestCompanyRepository(TestCase):
    def setUp(self) -> None:
        self.initializer = DbInitializer()
        self.initializer.run()
        self.tested_repo = CompanyRepository(database=self.initializer.db_path)

    def test_two_companies_with_same_name_is_not_allowed(self) -> None:
        params = CreateCompanyParams("SAS")
        self.tested_repo.create(1, params)
        with self.assertRaises(DuplicateCompanyException):
            self.tested_repo.create(1, params)
