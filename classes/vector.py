from math import sqrt, acos, degrees

from .quantity import Quantity
from .unit import Unit


class Vector:
    """3D Vector"""

    def __init__(self, x, y, z, unit: Unit | None = None) -> None:
        self._x = x
        self._y = y
        self._z = z
        self.unit = unit

    @property
    def x(self) -> Quantity:
        return Quantity(self._x, self.unit)

    @x.setter
    def x(self, value) -> None:
        self._x = value

    @property
    def y(self) -> Quantity:
        return Quantity(self._y, self.unit)

    @y.setter
    def y(self, value) -> None:
        self._y = value

    @property
    def z(self) -> Quantity:
        return Quantity(self._z, self.unit)

    @z.setter
    def z(self, value) -> None:
        self._z = value

    @property
    def length(self) -> float:
        """Length of the vector, no unit"""
        return sqrt(self._x**2 + self._y**2 + self._z**2)

    @property
    def magnitude(self) -> Quantity:
        """Magnitude of the vector with unit"""
        if self.unit:
            return Quantity(self.length, self.unit)
        return self.length

    def __neg__(self) -> "Vector":
        return Vector(-self._x, -self._y, -self._z, self.unit)

    def __str__(self) -> str:
        s = f"<{self._x:.2f} {self._y:.2f} {self._z:.2f}>"
        if self.unit:
            s += f" {str(self.unit)}"
        return s

    def __add__(self, other: "Vector") -> "Vector":
        if not self.unit and not other.unit:
            unit = None
        else:
            unit = self.unit + other.unit

        return Vector(self._x + other._x, self._y + other._y, self._z + other._z, unit)

    def __sub__(self, other: "Vector") -> "Vector":
        if not self.unit and not other.unit:
            unit = None
        else:
            unit = self.unit - other.unit

        return Vector(self._x - other._x, self._y - other._y, self._z - other._z, unit)

    def __mul__(self, number) -> "Vector":
        if type(number) == Quantity:
            return Vector(
                self._x * number.value,
                self._y * number.value,
                self._z * number.value,
                self.unit * number.unit,
            )

        return Vector(self._x * number, self._y * number, self._z * number, self.unit)

    def __truediv__(self, number) -> "Vector":
        if type(number) == Quantity:
            return Vector(
                self._x / number.value,
                self._y / number.value,
                self._z / number.value,
                self.unit / number.unit,
            )

        return Vector(self._x / number, self._y / number, self._z / number, self.unit)

    def __rmul__(self, number) -> "Vector":
        if type(number) == Quantity:
            return Vector(
                self._x * number.value,
                self._y * number.value,
                self._z * number.value,
                self.unit * number.unit,
            )

        return Vector(self._x * number, self._y * number, self._z * number, self.unit)

    def __eq__(self, other: "Vector") -> bool:
        """check for equality"""
        checks = [
            self._x == other._x,
            self._y == other._y,
            self._z == other._z,
            self.unit == other.unit,
        ]
        return all(checks)

    def __round__(self, ndigits: int = 0) -> "Vector":
        """Elementwise rounding"""
        new_x = round(self._x, ndigits)
        new_y = round(self._y, ndigits)
        new_z = round(self._z, ndigits)
        return Vector(new_x, new_y, new_z, unit=self.unit)

    def normalize(self) -> "Vector":
        """Normalize vector to unit length"""
        return self / self.length

    def dot(self, other: "Vector") -> float:
        """Dot product"""
        dot_v = self._x * other._x + self._y * other._y + self._z * other._z
        if self.unit or other.unit:
            dot_u = self.unit * other.unit
            return Quantity(dot_v, dot_u)
        return dot_v

    def angle(self, other: "Vector", degs: bool = False) -> float:
        """Angle between two vectors"""
        rad = acos(self.dot(other) / self.magnitude / other.magnitude)
        if degs:
            return degrees(rad)
        return rad

    def project(self, other: "Vector") -> "Vector":
        """Projection of vector onto another"""
        if other.unit:
            b = Vector(other._x, other._y, other._z)
        else:
            b = other
        return self.dot(b) / b.length**2 * b

    def split_parallel_orthogonal(self, other: "Vector") -> tuple["Vector", "Vector"]:
        """split vector in two parts parallel and orthogonal to other vector"""
        parallel = self.project(other)
        orthogonal = self - parallel
        return parallel, orthogonal

    def cross(self, other: "Vector") -> "Vector":
        """Cross product"""
        if not self.unit and not other.unit:
            unit = None
        else:
            unit = self.unit - other.unit

        x = self._y * other._z - self._z * other._y
        y = self._z * other._x - self._x * other._z
        z = self._x * other._y - self._y * other._x
        return Vector(x, y, z, unit)
