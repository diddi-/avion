from dataclasses import dataclass


@dataclass
class CreateUserAccountParams:
    firstname: str
    lastname: str
    email: str
    password: str
