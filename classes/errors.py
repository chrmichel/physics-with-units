class IncompatibleUnitsError(Exception):
    def __init__(self, operator: str, unit1: str, unit2: str, *args: object) -> None:
        self.message = f"Incompatible Units: cannot {operator} {unit1} and {unit2}"
        super().__init__(self.message, *args)
