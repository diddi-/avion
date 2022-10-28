import contextlib
import datetime
import sqlite3

from avion.domain.model.currency import Currency
from avion.domain.service.fleet.exceptions.no_registration_found_exception import NoRegistrationFoundException
from avion.domain.service.fleet.model.aircraft import Aircraft
from avion.domain.service.fleet.model.aircraft_model import AircraftModel
from avion.domain.service.fleet.model.aircraft_registration import AircraftRegistration
from avion.domain.service.fleet.model.create_aircraft_model_params import CreateAircraftModelParams
from avion.domain.service.fleet.model.engine_type import EngineType
from avion.domain.service.fleet.model.volume import Volume
from avion.domain.service.fleet.model.weight import Weight


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

    def get_aircraft_model_by_id(self, model_id: int) -> AircraftModel:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * from aircraft_model where id=?", (model_id,))
            return self._row_to_aircraft_model(cur.fetchone())

    def add_to_fleet(self, company_id: int, aircraft_model_id: int) -> Aircraft:
        purchased_at = datetime.datetime.now(datetime.timezone.utc)
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO company_aircraft (company_id, aircraft_model_id, purchased_at)"
                        " VALUES(?,?,?)",
                        (company_id, aircraft_model_id, purchased_at))
            conn.commit()
            aircraft_id = cur.lastrowid
            assert aircraft_id is not None
            aircraft = Aircraft(aircraft_id, aircraft_model_id, company_id)
            aircraft.purchased_at = purchased_at
            return aircraft

    def get_aircraft_by_id(self, aircraft_id: int) -> Aircraft:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * from company_aircraft where id=?", (aircraft_id,))
            return self._row_to_aircraft(cur.fetchone())

    def save(self, aircraft: Aircraft) -> None:
        reg_prefix = aircraft.registration.prefix if aircraft.registration else None
        reg_identifier = aircraft.registration.identifier if aircraft.registration else None

        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("UPDATE company_aircraft SET company_id=?, registration_prefix=?, registration_identifier=? "
                        " WHERE id=?", (aircraft.company_id, reg_prefix,
                                        reg_identifier, aircraft.id))
            conn.commit()

    def get_latest_registration(self) -> AircraftRegistration:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # We cheat a little by just looking at the latest registered aircraft right now. This will not hold in the
            # future when we have different registration prefixes.
            cur.execute("SELECT id, registration_prefix, registration_identifier FROM company_aircraft"
                        " WHERE registration_prefix IS NOT NULL ORDER BY id LIMIT 1")
            row = cur.fetchone()
            if not row:
                raise NoRegistrationFoundException()
            return AircraftRegistration(row["registration_prefix"], row["registration_identifier"])

    @staticmethod
    def _row_to_aircraft_model(row: sqlite3.Row) -> AircraftModel:
        model = AircraftModel(row["manufacturer"], row["model"], row["icao_code"])
        model.id = row["id"]
        model.empty_weight = Weight(int(row["empty_weight"]))
        model.engine_count = int(row["engine_count"])
        model.engine_type = EngineType(row["engine_type"])
        model.max_fuel = Volume(int(row["max_fuel"]))
        model.max_passengers = int(row["max_passengers"])
        model.max_takeoff_weight = Weight(int(row["max_takeoff_weight"]))
        model.price = Currency(int(row["price"]))
        return model

    @staticmethod
    def _row_to_aircraft(row: sqlite3.Row) -> Aircraft:
        aircraft = Aircraft(int(row["id"]), int(row["aircraft_model_id"]), int(row["company_id"]))
        if "registration_prefix" in row.keys():
            aircraft.registration = AircraftRegistration(row["registration_prefix"], row["registration_identifier"])
        aircraft.purchased_at = datetime.datetime.fromisoformat(row["purchased_at"])
        return aircraft
