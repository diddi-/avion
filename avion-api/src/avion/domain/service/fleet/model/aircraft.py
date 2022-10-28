import datetime
from typing import Optional

from avion.domain.service.fleet.model.aircraft_registration import AircraftRegistration


class Aircraft:
    def __init__(self, aircraft_id: int, aircraft_model_id: int, company_id: int):
        self.id = aircraft_id
        self.model_id = aircraft_model_id
        self.company_id = company_id
        self.registration: Optional[AircraftRegistration] = None
        self.purchased_at = datetime.datetime.now(datetime.timezone.utc)
