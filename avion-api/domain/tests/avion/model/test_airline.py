import datetime
from unittest import TestCase

from avion.model.airline import Airline


class TestAirline(TestCase):
    def test_id_cant_be_changed(self):
        airline = Airline("SAS")
        airline.id = 123
        with self.assertRaises(ValueError):
            airline.id = 456

    def test_created_at_cant_be_changed(self):
        airline = Airline("SAS")
        airline.created_at = datetime.datetime.utcnow()
        with self.assertRaises(ValueError):
            airline.created_at = datetime.datetime.utcnow()
