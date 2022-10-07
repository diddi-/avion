import datetime
from unittest import TestCase

from avion.model.company import Company


class TestCompany(TestCase):
    def test_id_cant_be_changed(self) -> None:
        company = Company("SAS")
        company.id = 123
        with self.assertRaises(ValueError):
            company.id = 456

    def test_created_at_cant_be_changed(self) -> None:
        company = Company("SAS")
        company.created_at = datetime.datetime.utcnow()
        with self.assertRaises(ValueError):
            company.created_at = datetime.datetime.utcnow()
