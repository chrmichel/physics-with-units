from .unit import Unit, IncompatibleUnitsError, NO_UNIT


class Quantity:
    """Quantity with value and unit"""

    def __new__(cls, value: int | float | complex, unit: Unit | None, name: str|None = None) -> None:
        if unit == NO_UNIT or unit is None:
            return value
        instance = super().__new__(cls)
        return instance

    def __init__(self, value: int | float | complex, unit: Unit, name: str|None = None) -> None:
        self.value = value
        self.unit = unit
        if name:
            self.name = name
        else:
            self.name = unit.get_name()

    def __str__(self) -> str:
        return f"{self.value} {str(self.unit)}"

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


if __name__ == "__main__":
    from unit import KILO, METER

    a = Quantity(1, KILO)
    b = Quantity(2, KILO)
    c = Quantity(1, METER)
    d = Quantity(6.9, NO_UNIT)
    d2 = Quantity(6.9, Unit([]))
    d3 = Quantity(6.9, Unit([], ""))

    print(a == b)
    print(a <= b)
    print(a >= b)
    print(a < b)
    print(a > b)
    print(a != b)
    print(a + b)
    print(a * b)
    print(a / c)
    print(3 * a)
    print(5 / b)
    print(c / 5)
    print(type(d))
    print(type(d2))
    print(type(d3))
    print(a / b)
