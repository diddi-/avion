import contextlib
import datetime
import sqlite3
from sqlite3 import Row
from typing import List

from avion.service.company.exceptions.company_not_found_exception import CompanyNotFoundException
from avion.service.company.model.company import Company
from avion.service.company.model.create_company_params import CreateCompanyParams
from avion.model.currency import Currency


class CompanyRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create(self, params: CreateCompanyParams) -> Company:
        created_at = datetime.datetime.now(datetime.timezone.utc)
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO company (created_at, profile_id, name, balance) "
                        "VALUES (?,?,?,?)",
                        (created_at, params.owner_id, params.name, params.balance))
            conn.commit()
            company_id = cur.lastrowid
            assert company_id is not None
            company = Company(company_id, params.name)
            company.owner_id = params.owner_id
            company.balance = Currency(params.balance)
            company.created_at = created_at
        return company

    def get_all_companies(self) -> List[Company]:
        companies: List[Company] = []
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM company")
            rows = cur.fetchall()
            for row in rows:
                companies.append(self._row_to_company(row))
        return companies

    def get_company_by_name(self, name: str) -> Company:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM company WHERE name=:name LIMIT 1", {"name": name})
            rows = cur.fetchall()
            if rows:
                return self._row_to_company(rows[0])
        raise CompanyNotFoundException(f"No company with name '{name}' found.")

    def get_company_by_id(self, c_id: int) -> Company:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM company WHERE id=?", (c_id,))
            rows = cur.fetchall()
            if rows:
                return self._row_to_company(rows[0])
        raise CompanyNotFoundException(f"No company with id '{c_id}' found.")

    def save(self, company: Company) -> None:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("UPDATE company SET name=?, balance=? WHERE id=?",
                        (company.name, company.balance.amount, company.id))
            conn.commit()

    @staticmethod
    def _row_to_company(row: Row) -> Company:
        company = Company(row["id"], row["name"])
        company.created_at = datetime.datetime.fromisoformat(row["created_at"])
        company.balance = Currency(int(row["balance"]))
        return company
