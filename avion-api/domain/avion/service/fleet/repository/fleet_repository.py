import contextlib
import datetime
import sqlite3

from avion.service.fleet.model.aircraft_model import AircraftModel
from avion.service.fleet.model.create_aircraft_model_params import CreateAircraftModelParams


class FleetRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create_aircraft_model(self, params: CreateAircraftModelParams) -> AircraftModel:
        model = AircraftModel(params.manufacturer, params.model, params.icao_code)
        model.engine_count = params.engine_count
        model.engine_type = params.engine_type
        model.max_fuel = params.max_fuel
        model.empty_weight = params.empty_weight
        model.max_takeoff_weight = params.max_takeoff_weight
        model.max_passengers = params.max_passengers
        model.price = params.price

        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO aircraft_model (manufacturer, model, icao_code, engine_count, engine_type, max_fuel,"
                " empty_weight, max_takeoff_weight, max_passengers, price) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (model.manufacturer, model.model, model.icao_code, model.engine_count, str(model.engine_type),
                 int(model.max_fuel), int(model.empty_weight), int(model.max_takeoff_weight), model.max_passengers,
                 int(model.price)))
            conn.commit()
            model.id = cur.lastrowid
        return model

    def add_to_fleet(self, company_id: int, aircraft_model_id: int) -> None:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO company_aircraft (company_id, aircraft_model_id, purchased_at)"
                        " VALUES(?,?,?)",
                        (company_id, aircraft_model_id, datetime.datetime.now(datetime.timezone.utc)))
            conn.commit()
