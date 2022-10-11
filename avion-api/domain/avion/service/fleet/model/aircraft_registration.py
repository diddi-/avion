

class AircraftRegistration:
    """ An AircraftRegistration is the registration code to uniquely identify a single aircraft.
    It is composed of a Prefix (country specific) and a value including both numbers and letters.
    Depending on the country, a separator may or may not be used between the prefix and the identifier.
    Example:
            Sweden - SE-CMO, SE-A4M
            USA    - N12345, N123AK """
    def __init__(self, prefix: str, identifier: int):
        # This is very much simplified for now using only ints as identifier. This is because they are much easier
        # to increment.
        self.prefix = prefix
        self.identifier = identifier

    def __str__(self) -> str:
        return f"{self.prefix}{self.identifier:05}"
