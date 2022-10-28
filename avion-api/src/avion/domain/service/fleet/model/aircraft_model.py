from typing import Optional

from avion.domain.model.currency import Currency
from avion.domain.service.fleet.model.engine_type import EngineType
from avion.domain.service.fleet.model.volume import Volume
from avion.domain.service.fleet.model.weight import Weight


class AircraftModel:
    # This should be fixed properly, disabling check for now.
    # pylint: disable=too-many-instance-attributes
    def __init__(self, manufacturer: str, model: str, icao_code: str):
        self.id: Optional[int] = None
        self.manufacturer = manufacturer
        self.model = model
        self.icao_code = icao_code
        self.engine_count = 1
        self.engine_type = EngineType.PISTON
        self.max_fuel = Volume(0)
        self.empty_weight = Weight(0)  # Without fuel, pax, cargo
        self.max_takeoff_weight = Weight(0)  # Including fuel, pax, cargo
        self.max_passengers = 0
        self.price = Currency(0)
