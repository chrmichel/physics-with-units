import json

from .errors import IncompatibleUnitsError


BASE_SI = ["kg", "m", "s", "K", "A", "mol", "cd"]


class Unit:
    """represents the basic SI units"""

    dimensions = {
        "mass": [1, 0, 0, 0, 0, 0, 0],
        "length": [0, 1, 0, 0, 0, 0, 0],
        "area": [0, 2, 0, 0, 0, 0, 0],
        "volume": [0, 3, 0, 0, 0, 0, 0],
        "time": [0, 0, 1, 0, 0, 0, 0],
        "temperature": [0, 0, 0, 1, 0, 0, 0],
        "current": [0, 0, 0, 0, 1, 0, 0],
        "amount": [0, 0, 0, 0, 0, 1, 0],
        "luminous intensity": [0, 0, 0, 0, 0, 0, 1],
    }

    @staticmethod
    def update_dimensions(dimdict: dict | str, filetype: str = "json") -> None:
        if type(dimdict) == dict:
            Unit.dimensions.update(dimdict)
        elif type(dimdict) == str:
            if filetype == "json":
                try:
                    with open(f"dimensions/{dimdict}.json") as file:
                        dic = json.load(file)
                except FileNotFoundError:
                    print(
                        "No file found, update failed. Please enter a valid file name."
                    )
                    return
                Unit.dimensions.update(dic)
            elif filetype == "yaml":
                raise NotImplementedError
            else:
                raise TypeError("Invalid file type given, use json or yaml instead.")
        else:
            raise TypeError("no valid type given for update")

    @classmethod
    def from_dict(cls, dim):
        if dim in cls.dimensions.keys():
            return Unit(cls.dimensions[dim])
        raise ValueError

    def __init__(self, numbers: list[int]) -> None:
        if len(numbers) > 7:
            raise ValueError
        while len(numbers) < 7:
            numbers.append(0)
        self._nums = numbers
        # self.rename()

    def __str__(self) -> str:
        """If name is given, return name, else base SI composition"""
        # if self.name:
        #     return self.name
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
        u = Unit(nums)
        print(u)
        return u

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
        new_nums = [i * exponent for i in self._nums]
        return Unit(new_nums)

    def __eq__(self, other) -> bool:
        """compare two units if equal"""
        if other is None:
            return self is None
        if type(other) != Unit:
            return False
        if self._nums != other._nums:
            return False
        return True

    def check_dimensions(self, dims: dict = dimensions) -> list[str]:
        answer = []
        for k, v in dims.items():
            if self._nums == v:
                answer.append(k)
        return answer

    def invert(self) -> "Unit":
        nums = [-i for i in self._nums]
        return Unit(nums)

    def get_name(self, dimdict: dict | None = None) -> str | None:
        if dimdict:
            dims = self.check_dimensions(dimdict)
        else:
            dims = self.check_dimensions()
        if len(dims) == 1:
            return dims[0]
        elif len(dims) == 0:
            return None
        else:
            for i, d in enumerate(dims):
                print(f"{i+1}: {d}")
            num = int(input("Enter the number of the chosen dimension: ")) - 1
            return dims[num]


NO_UNIT = Unit([])
