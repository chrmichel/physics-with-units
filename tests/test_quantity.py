import pytest

from classes import IncompatibleUnitsError, Quantity


@pytest.fixture
def two_kilos(kilo):
    return Quantity(2, kilo)


@pytest.fixture
def one_meter(meter):
    return Quantity(1, meter)


def test_string(one_kilo):
    assert str(one_kilo) == "1 kg"


def test_add_kilos(one_kilo, two_kilos, kilo):
    three_kilos = one_kilo + two_kilos
    assert three_kilos.value == 3
    assert three_kilos.unit == kilo


def test_add_kilo_meter(one_kilo, one_meter):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = one_kilo + one_meter
    assert "cannot add" in str(e.value)


def test_add_unit_number(one_kilo):
    with pytest.raises(TypeError):
        _ = one_kilo + 6


def test_sub_kilos(one_kilo, two_kilos, kilo):
    neg_kilos = one_kilo - two_kilos
    assert neg_kilos.value == -1
    assert neg_kilos.unit == kilo


def test_sub_kilo_meter(one_kilo, one_meter):
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = one_kilo - one_meter
    assert "cannot subtract" in str(e.value)


def test_sub_unit_number(one_kilo):
    with pytest.raises(TypeError):
        _ = one_kilo - 6


def test_multiply_units(one_kilo, one_meter):
    km = one_kilo * one_meter
    assert km.value == 1
    assert km.unit._nums == [1, 1] + [0] * 5
    assert str(km) == "1 kg m"


def test_multiply_number(one_kilo):
    three_kilos = 3 * one_kilo
    assert three_kilos.value == 3
    reverse = one_kilo * 3
    assert reverse.value == 3


def test_divide_units(one_kilo, one_meter):
    km = one_kilo / one_meter
    assert km.value == 1
    assert km.unit._nums == [1, -1] + [0] * 5
    assert str(km) == "1.0 kg m^-1"


def test_divide_number(one_kilo):
    three_per_kg = 3 / one_kilo
    assert three_per_kg.value == 3
    assert str(three_per_kg) == "3.0 kg^-1"
    reverse = one_kilo / 3
    assert reverse.value == 1 / 3


def test_divide_same_unit(one_kilo, two_kilos):
    half = one_kilo / two_kilos
    assert type(half) == float
    assert half == 0.5


def test_compare(one_kilo, two_kilos, one_meter):
    assert one_kilo < two_kilos
    assert not one_kilo > two_kilos
    assert not one_kilo == two_kilos
    assert one_kilo != two_kilos
    assert one_kilo <= two_kilos
    assert not one_kilo >= two_kilos
    with pytest.raises(TypeError):
        _ = one_kilo == 1
    with pytest.raises(IncompatibleUnitsError) as e:
        _ = one_kilo == one_meter
    assert "cannot compare" in str(e.value)


def test_round(two_kilos, kilo):
    assert round(Quantity(2.4, kilo)) == two_kilos
