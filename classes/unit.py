BASE_SI = ["kg", "m", "s", "K", "A", "mol", "cd"]


class Unit:
    """represents the basic SI units"""

    dimensions = {
        "speed": ([0, 1, -1, 0, 0, 0, 0], "meters per second"),
        "acceleration": ([0, 1, -2, 0, 0, 0, 0], "meters per square second"),
        "energy": ([1, 2, -2, 0, 0, 0, 0], "Joule"),
        "momentum": ([1, 1, -1, 0, 0, 0, 0], "kilograms meter per second"),
        "ang mom": ([1, 2, -1, 0, 0, 0, 0], "kilograms square meter per second"),
        "force": ([1, 1, -2, 0, 0, 0, 0], "Newton"),
        "torque": ([1, 2, -2, 0, 0, 0, 0], "Newton meter"),
        "power": ([1, 2, -3, 0, 0, 0, 0], "Watt"),
        "pressure": ([1, -1, -2, 0, 0, 0, 0], "Pascal"),
    }

    @staticmethod
    def update_dimensions(dimdict: dict[str, list[int]]) -> None:
        Unit.dimensions.update(dimdict)

    @classmethod
    def from_dict(cls, dim):
        if dim in cls.dimensions.keys():
            return Unit(*cls.dimensions[dim])
        raise ValueError

    def __init__(self, numbers: list[int], name: str | None = None) -> None:
        if len(numbers) > 7:
            raise ValueError
        while len(numbers) < 7:
            numbers.append(0)
        self._nums = numbers
        self.name = name

    def __str__(self) -> str:
        """If name is given, return name, else base SI composition"""
        if self.name:
            return self.name
        s = []
        for i, num in enumerate(self._nums):
            if num == 1:
                s.append(BASE_SI[i])
            elif num != 0:
                s.append(BASE_SI[i] + f"^{num}")
        return " ".join(s)

    def __add__(self, other: "Unit") -> "Unit":
        if self == other:
            return self
        raise IncompatibleUnitsError("add", str(self), str(other))

    def __sub__(self, other: "Unit") -> "Unit":
        if self == other:
            return self
        raise IncompatibleUnitsError("subtract", str(self), str(other))

    def __mul__(self, other: "Unit") -> "Unit":
        """multiply two units"""
        if other is None:
            return self
        nums = [i + j for i, j in zip(self._nums, other._nums)]
        return Unit(nums)

    def __truediv__(self, other: "Unit") -> "Unit":
        """divide two units"""
        if other is None:
            return self
        nums = [i - j for i, j in zip(self._nums, other._nums)]
        return Unit(nums)

    def __rmul__(self, other: "Unit") -> "Unit":
        """multiply two units"""
        if other is None:
            return self
        nums = [i + j for i, j in zip(self._nums, other._nums)]
        return Unit(nums)

    def __rtruediv__(self, other: "Unit") -> "Unit":
        """divide two units"""
        if other is None:
            return self.invert()
        nums = [j - i for i, j in zip(self._nums, other._nums)]
        return Unit(nums)

    def __pow__(self, exponent: int | float) -> "Unit":
        new_name = None
        new_nums = [i * exponent for i in self._nums]
        return Unit(new_nums, new_name)

    def __eq__(self, other) -> bool:
        """compare two units if equal"""
        if other is None:
            return self is None
        if type(other) != Unit:
            raise TypeError
        # must have same dimensions
        if self._nums != other._nums:
            return False
        # if both have names, must be the same
        if self.name and other.name:
            return self.name == other.name
        # if neither has a name, return True
        elif self.name is None and other.name is None:
            return True
        # False if only one has a name
        else:
            return False

    def check_dimensions(self, dims: dict = dimensions) -> list[str]:
        answer = []
        for k, v in dims.items():
            if self._nums == v[0]:
                answer.append(k)
        return answer

    def invert(self) -> "Unit":
        nums = [-i for i in self._nums]
        name = "Inverse " + self.name if self.name else None
        return Unit(nums, name)


KILO = Unit([1], "kilogram")
METER = Unit([0, 1], "meter")
SECOND = Unit([0, 0, 1], "second")
KELVIN = Unit([0, 0, 0, 1], "kelvin")
AMPERE = Unit([0, 0, 0, 0, 1], "ampere")
MOL = Unit([0, 0, 0, 0, 0, 1], "mole")
CANDELA = Unit([0, 0, 0, 0, 0, 0, 1], "candela")
NO_UNIT = Unit([])


class IncompatibleUnitsError(Exception):
    def __init__(self, operator: str, unit1: str, unit2: str, *args: object) -> None:
        self.message = f"Incompatible Units: cannot {operator} {unit1} and {unit2}"
        super().__init__(self.message, *args)


if __name__ == "__main__":
    speed = Unit([0, 1, -1], "speed")
    print(speed)
    # momentum = speed * KILO
    # print(momentum)
    # kilo2 = Unit([1], "kilo2")
    # equality = KILO == kilo2
    # print(f"{equality = }")
    vsquare = pow(speed, 2)
    print(vsquare)
    print(vsquare._nums)
    en = KILO * speed**2
    print(en)
    print(en.check_dimensions())
