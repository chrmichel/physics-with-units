import pytest

from classes import Unit, IncompatibleUnitsError, NO_UNIT


@pytest.fixture
def kilo2():
    return Unit([1])


@pytest.fixture
def kilo3():
    return Unit([1], "kilo with another name")


def test_add_kilos(kilo, kilo2):
    two_kilos = kilo + kilo2
    assert two_kilos._nums == [1, 0, 0, 0, 0, 0, 0]
    assert two_kilos.name == kilo.name
    assert str(two_kilos) == "kg"


def test_add_different_kilos(kilo, kilo3):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = kilo + kilo3
    assert "cannot add" in str(e.value)


def test_add_different_units(kilo, meter):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = kilo + meter
    assert "cannot add" in str(e.value)


def test_sub_kilos(kilo, kilo2):
    two_kilos = kilo - kilo2
    assert two_kilos._nums == [1, 0, 0, 0, 0, 0, 0]
    assert two_kilos.name == kilo.name
    assert str(two_kilos) == "kg"


def test_sub_different_kilos(kilo, kilo3):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = kilo - kilo3
    assert "cannot subtract" in str(e.value)


def test_sub_different_units(kilo, meter):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = kilo - meter
    assert "cannot subtract" in str(e.value)


def test_multiply_units(kilo, meter):
    km = kilo * meter
    assert km._nums == [1, 1, 0, 0, 0, 0, 0]
    assert str(km) == "kg m"


def test_multiply_same_unit(kilo):
    km = kilo * kilo
    assert km._nums == [2, 0, 0, 0, 0, 0, 0]
    assert str(km) == "kg^2"


def test_multiply_inverses(second, hertz):
    n = second * hertz
    assert n._nums == [0] * 7
    assert str(n) == ""


def test_divide_units(kilo, meter):
    km = kilo / meter
    assert km._nums == [1, -1, 0, 0, 0, 0, 0]
    assert str(km) == "kg m^-1"


def test_divide_same_unit(kilo):
    km = kilo / kilo
    assert km == NO_UNIT


def test_power_int(kilo):
    k2 = kilo**2
    assert k2._nums == [2] + [0] * 6
    assert str(k2) == "kg^2"
    k5 = kilo**5
    assert k5._nums == [5] + [0] * 6
    assert str(k5) == "kg^5"
    k1 = kilo**-1
    assert k1._nums == [-1] + [0] * 6
    assert str(k1) == "kg^-1"


def test_power_float(kilo):
    k2 = kilo**2.5
    assert k2._nums == [2.5] + [0] * 6
    assert str(k2) == "kg^2.5"
    k5 = kilo**-0.5
    assert k5._nums == [-0.5] + [0] * 6
    assert str(k5) == "kg^-0.5"


def test_equal(kilo, kilo2, kilo3):
    assert kilo == kilo2
    assert kilo != kilo3


def test_from_dict():
    joule = Unit.from_dict("energy")
    assert joule._nums == [1, 2, -2, 0, 0, 0, 0]
    assert joule.name == "Joule"
    assert str(joule) == "Joule"


def test_update_dict():
    nums = [1, -3, 0, 0, 0, 0, 0]
    name = "kilograms per cubic meter"
    dic = {"density": (nums, name)}
    Unit.update_dimensions(dic)
    assert "density" in Unit.dimensions.keys()
    dens = Unit.from_dict("density")
    assert dens._nums == nums
    assert dens.name == name


def test_check_dimensions(second):
    f = Unit.from_dict("momentum") / second
    assert f.check_dimensions() == ["force"]


def test_invert_kilo(kilo):
    inv = kilo.invert()
    assert inv._nums == [-1] + [0] * 6
    assert inv.name is None
