import configparser
import os

from avion.config.jwt_config import JwtConfig


class Config:
    def __init__(self) -> None:
        self.jwt = JwtConfig()

    def load(self) -> None:
        parser = configparser.ConfigParser()
        parser.read(self.get_config_path())

        for section in parser.sections():
            if section == JwtConfig.SECTION_NAME:
                self.jwt = JwtConfig.from_section(parser[section])
            else:
                raise ValueError(f"'{section}' is not a valid configuration section")

    @staticmethod
    def get_config_path() -> str:
        return os.environ.get("AVION_CONFIG", "avion.conf")


# This really should be singleton instead of global.
current_config = Config()
