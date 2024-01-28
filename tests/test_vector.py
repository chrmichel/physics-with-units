import pytest
from math import sqrt, pi

from classes import Vector, Quantity, Unit


@pytest.fixture
def vec1():
    return Vector(1, 2, 3)


@pytest.fixture
def vec2():
    return Vector(4, 5, 6)


@pytest.fixture
def vec_m(meter):
    return Vector(1, 2, 3, meter)


def test_vec_properties(vec1, vec2):
    assert vec1.unit == None
    assert vec1.x == 1
    assert vec1.y == 2
    assert vec1.z == 3
    assert vec1.length == sqrt(14)
    assert vec1.magnitude == sqrt(14)
    assert str(vec1) == "<1.00 2.00 3.00>"
    vec1.x, vec1.y, vec1.z = 4, 5, 6
    assert vec1 == vec2


def test_vec_properties_units(vec_m, meter):
    assert vec_m.unit == meter
    assert vec_m.x == Quantity(1, meter)
    assert vec_m.y == Quantity(2, meter)
    assert vec_m.z == Quantity(3, meter)
    assert vec_m.length == sqrt(14)
    assert vec_m.magnitude == Quantity(sqrt(14), meter)
    assert str(vec_m) == "<1.00 2.00 3.00> m"


def test_add_sub(vec1, vec2, vec_m):
    assert vec1 + vec2 == Vector(5, 7, 9)
    with pytest.raises(Exception):
        _ = vec1 + vec_m
    assert vec2 - vec1 == Vector(3, 3, 3)
    with pytest.raises(Exception):
        _ = vec1 - vec_m


def test_mul_div(vec1, vec_m, one_kilo, meter):
    assert 3 * vec1 == Vector(3, 6, 9)
    assert vec_m / 2 == Vector(0.5, 1.0, 1.5, meter)
    kv = one_kilo * vec1
    assert str(kv) == "<1.00 2.00 3.00> kg"
    mk = vec_m / one_kilo
    eqcheck = Vector(1, 2, 3, Unit([-1, 1]))
    assert str(eqcheck) == str(mk)
    assert str(mk) == "<1.00 2.00 3.00> kg^-1 m"


def test_normalize(vec1, vec_m, meter):
    v1n = vec1.normalize()
    assert v1n.length == 1
    vmn = vec_m.normalize()
    assert vmn.length == 1
    assert vmn.unit == meter


def test_dot(vec1, vec2, vec_m, meter):
    dot12 = vec1.dot(vec2)
    assert dot12 == 32
    assert type(dot12) == int
    dot1m = vec1.dot(vec_m)
    assert type(dot1m) == Quantity
    assert dot1m.value == 14
    assert dot1m.unit == meter


def test_angle(vec1, vec2, vec_m):
    a1 = vec1.angle(vec2)
    assert 0 <= a1 <= pi
    a2 = vec1.angle(vec_m)
    assert round(a2, 6) == 0


def test_project(vec1, vec2):
    p = vec1.project(vec2)
    assert round(p.angle(vec2), 6) == 0.0
    q = vec2.project(vec1)
    assert round(q.angle(vec1), 6) == 0.0


def test_split(vec1, vec2):
    p1, o1 = vec1.split_parallel_orthogonal(vec2)
    assert p1 + o1 == vec1
    assert round(p1.dot(o1), 6) == 0
    assert round(p1.angle(vec2), 6) == 0
    assert round(o1.dot(vec2), 6) == 0


def test_cross(vec1, vec2):
    cp = vec1.cross(vec2)
    assert round(cp.dot(vec1), 6) == 0
    assert round(cp.dot(vec2), 6) == 0
    assert vec2.cross(vec1) == -cp
