import contextlib
import datetime
import sqlite3
from sqlite3 import Row
from typing import List

from avion.api.input.create_airline_params import CreateAirlineParams
from avion.model.airline import Airline
from avion.repository.exceptions.airline_not_found_exception import AirlineNotFoundException


class AirlineRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create(self, params: CreateAirlineParams) -> Airline:
        airline = Airline(params.name)
        airline.created_at = datetime.datetime.now(datetime.timezone.utc)
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO airline (created_at, name) "
                        "VALUES (?,?)",
                        (airline.created_at, params.name))
            conn.commit()
            airline.id = cur.lastrowid
        return airline

    def get_all_airlines(self) -> List[Airline]:
        airlines: List[Airline] = []
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM airline")
            rows = cur.fetchall()
            for row in rows:
                airlines.append(self._row_to_airline(row))
        return airlines

    def get_airline_by_name(self, name: str) -> Airline:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM airline WHERE name=:name LIMIT 1", {"name": name})
            rows = cur.fetchall()
            if rows:
                return self._row_to_airline(rows[0])
        raise AirlineNotFoundException(f"No airline with name '{name}' found.")

    @staticmethod
    def _row_to_airline(row: Row) -> Airline:
        airline = Airline(row["name"])
        airline.created_at = datetime.datetime.fromisoformat(row["created_at"])
        airline.id = row["id"]
        return airline
