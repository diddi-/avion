import datetime
from unittest import TestCase

from avion.domain.service.company.model.company import Company


class TestCompany(TestCase):
    def test_created_at_cant_be_changed(self) -> None:
        company = Company(1, "SAS")
        company.created_at = datetime.datetime.utcnow()
        with self.assertRaises(ValueError):
            company.created_at = datetime.datetime.utcnow()
