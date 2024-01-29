import pytest

from classes import Unit, IncompatibleUnitsError, NO_UNIT


@pytest.fixture
def kilo2():
    return Unit([1])


def test_add_kilos(kilo, kilo2):
    two_kilos = kilo + kilo2
    assert two_kilos._nums == [1, 0, 0, 0, 0, 0, 0]
    assert str(two_kilos) == "kg"


def test_add_different_units(kilo, meter):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = kilo + meter
    assert "cannot add" in str(e.value)


def test_sub_kilos(kilo, kilo2):
    two_kilos = kilo - kilo2
    assert two_kilos._nums == [1, 0, 0, 0, 0, 0, 0]
    assert str(two_kilos) == "kg"


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


def test_equal(kilo, kilo2):
    assert kilo == kilo2


def test_from_dict():
    meters = Unit.from_dict("length")
    assert meters._nums == [0, 1, 0, 0, 0, 0, 0]


def test_update_dict_from_dict():
    nums = [1, -3, 0, 0, 0, 0, 0]
    dic = {"density": nums}
    Unit.update_dimensions(dic)
    assert "density" in Unit.dimensions.keys()
    dens = Unit.from_dict("density")
    assert dens._nums == nums


def test_update_dict_from_json():
    Unit.update_dimensions("mechanics")
    assert "speed" in Unit.dimensions


def test_check_dimensions(meter):
    f = Unit.from_dict("length")
    assert f._nums == [0, 1] + [0] * 5
    f = f * meter
    print(f)
    assert f.check_dimensions() == ["area"]


def test_invert_kilo(kilo):
    inv = kilo.invert()
    assert inv._nums == [-1] + [0] * 6


def test_get_name(kilo):
    assert kilo.get_name() == "mass"
