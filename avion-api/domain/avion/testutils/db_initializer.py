import contextlib
import os
import sqlite3
import tempfile
from pathlib import Path


class DbInitializer:
    def __init__(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.db_path = os.path.join(self.temp_dir.name, "test.db")

    def run(self, include_seeds: bool = False) -> None:
        with contextlib.closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            for file in os.scandir(os.path.join(os.path.dirname(__file__), "../..", "..", "flyway", "sql")):
                if file.is_file():
                    if "seed" in file.name and not include_seeds:
                        continue
                    cur.executescript(Path(file.path).read_text(encoding="utf-8"))
            conn.commit()

    def __del__(self) -> None:
        # The lifetime of our temporary directory is outside control of this class as it must exist for the duration
        # of an entire test. As such, the only way to know when to properly clean up the temp dir is in the destructor.
        self.temp_dir.cleanup()
