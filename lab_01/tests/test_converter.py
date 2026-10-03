from decimal import Decimal

import pytest
from toolkit.converter import convert
from toolkit.errors import *


def test_temperature():
    assert convert(0, "c", "k") == 273
    assert convert(32, "f", "c") == 0
    assert convert(300, "k", "f") == Decimal("80.6")

def test_mass():
    assert convert(10, "g", "kg") == Decimal("0.01")
    assert convert(60, "kg", "g") == 60000

def test_length():
    assert convert(1, "m", "cm") == 100
    assert convert(2, "m", "mm") == 2000
    assert convert(30000, "m", "km") == 30

def test_case_insensitivity():
    try:
        convert(1, "km", "m")
        convert(1, "KM", "M")
        convert(1, "kM", "m")

        convert(1, "g", "kg")
        convert(1, "G", "KG")
        convert(1, "g", "Kg")

    except UnitError:
        pytest.fail()

def test_unit_errors():
    with pytest.raises(UnitError):
        convert(1, "aa", "aaaa")

    with pytest.raises(UnitError):
        convert(1, "kg", "km")

def test_conversion_errors():
    with pytest.raises(ConversionError):
        convert(-300, "c", "k")

    with pytest.raises(ConversionError):
        convert(-1, "kg", "g")
        
    with pytest.raises(ConversionError):
        convert(-1, "m", "km")