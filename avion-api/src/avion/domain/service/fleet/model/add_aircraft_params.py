from dataclasses import dataclass


@dataclass
class AddAircraftParams:
    company_id: int
    aircraft_model_id: int
