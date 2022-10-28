from dataclasses import dataclass

from avion.model.currency import Currency
from avion.service.fleet.model.engine_type import EngineType
from avion.service.fleet.model.volume import Volume
from avion.service.fleet.model.weight import Weight


@dataclass
class CreateAircraftModelParams:
    # This should be fixed properly, disabling check for now.
    # pylint: disable=too-many-instance-attributes
    manufacturer: str
    model: str
    icao_code: str
    engine_count = 1
    engine_type = EngineType.PISTON
    max_fuel = Volume(0)
    empty_weight = Weight(0)
    max_takeoff_weight = Weight(0)
    max_passengers = 0
    price = Currency(0)
