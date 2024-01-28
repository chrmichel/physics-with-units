import pytest

from classes import Unit, Quantity


@pytest.fixture
def kilo():
    return Unit([1])


@pytest.fixture
def meter():
    return Unit([0, 1])


@pytest.fixture
def second():
    return Unit([0, 0, 1])


@pytest.fixture
def hertz():
    return Unit([0, 0, -1])


@pytest.fixture
def one_kilo(kilo):
    return Quantity(1, kilo)
