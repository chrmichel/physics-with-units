from .unit import Unit, IncompatibleUnitsError, NO_UNIT


class Quantity:
    """Quantity with value and unit"""

    def __new__(
        cls,
        value: int | float | complex,
        unit: Unit | str | None,
        name: str | None = None,
    ) -> None:
        if unit == NO_UNIT or unit is None:
            return value
        instance = super().__new__(cls)
        return instance

    def __init__(
        self,
        value: int | float | complex,
        unit: Unit | str | None,
        name: str | None = None,
    ) -> None:
        """
        value: value of the quantity
        unit: unit of the quantity; if str is given use Unit.from_dict to determine unit; if no unit is given
              no quantity will be created but instead only the value is returned
        name: name of the quantity; if None the dictionary will be checked to find a suitable name
        """
        self.value = value
        if type(unit) == Unit:
            self.unit = unit
            if name:
                self.name = name
            else:
                self.name = unit.get_name()
        elif type(unit) == str:
            self.unit = Unit.from_dict(unit)
            self.name = unit

    def __str__(self) -> str:
        s = ""
        if self.name:
            s += f"{self.name}: "
        s += f"{self.value} {str(self.unit)}"
        return s

    def __add__(self, other: "Quantity") -> "Quantity":
        if type(other) != Quantity:
            raise TypeError
        return Quantity(self.value + other.value, self.unit + other.unit)

    def __sub__(self, other: "Quantity") -> "Quantity":
        if type(other) != Quantity:
            raise TypeError
        return Quantity(self.value - other.value, self.unit - other.unit)

    def __mul__(self, other) -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        elif type(other) in [int, float, complex]:
            return Quantity(self.value * other, self.unit)
        else:
            return NotImplemented

    def __truediv__(self, other) -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        return Quantity(self.value / other, self.unit)

    def __rmul__(self, other) -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        return Quantity(self.value * other, self.unit)

    def __rtruediv__(self, other) -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(other.value / self.value, other.unit / self.unit)
        return Quantity(other / self.value, self.unit.invert())

    def __eq__(self, other) -> bool:
        if type(other) != Quantity:
            raise TypeError
        if not self.unit == other.unit:
            raise IncompatibleUnitsError("compare", str(self.unit), str(other.unit))
        return self.value == other.value

    def __gt__(self, other) -> bool:
        if type(other) != Quantity:
            raise TypeError
        if not self.unit == other.unit:
            raise IncompatibleUnitsError("compare", str(self.unit), str(other.unit))
        return self.value > other.value

    def __lt__(self, other) -> bool:
        if type(other) != Quantity:
            raise TypeError
        if not self.unit == other.unit:
            raise IncompatibleUnitsError("compare", str(self.unit), str(other.unit))
        return self.value < other.value

    def __ge__(self, other) -> bool:
        if type(other) != Quantity:
            raise TypeError
        if not self.unit == other.unit:
            raise IncompatibleUnitsError("compare", str(self.unit), str(other.unit))
        return self.value >= other.value

    def __le__(self, other) -> bool:
        if type(other) != Quantity:
            raise TypeError
        if not self.unit == other.unit:
            raise IncompatibleUnitsError("compare", str(self.unit), str(other.unit))
        return self.value <= other.value

    def __pow__(self, exponent: int | float) -> "Quantity":
        return Quantity(self.value**exponent, self.unit**exponent)

    def __round__(self, ndigits: int = 0) -> "Quantity":
        return Quantity(round(self.value, ndigits), self.unit)
