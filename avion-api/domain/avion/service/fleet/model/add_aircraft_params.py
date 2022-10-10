from dataclasses import dataclass

from avion.model.currency import Currency
from avion.service.fleet.model.engine_type import EngineType
from avion.service.fleet.model.volume import Volume
from avion.service.fleet.model.weight import Weight


@dataclass
class AddAircraftParams:
    company_id: int
    aircraft_model_id: int
