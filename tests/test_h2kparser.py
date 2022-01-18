from src.h2kparser import ParseH2K
import pytest
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


@pytest.fixture
def validation_obj():
    validation_h2k = os.path.join(os.path.dirname(
        __file__), "ASHRAE_Standard_140/H2K/Standard140-Class2 L100 Cooling.h2k")
    validation_schema = os.path.join(os.path.dirname(
        __file__), "schema/H2K Schema.xsd")

    return ParseH2K(validation_h2k, validation_schema)


def test_get_version(validation_obj):
    version = validation_obj.get_version()
    assert version['@major'] == 11
    assert version['@minor'] == 3


def test_get_climate_Prov(validation_obj):
    province = validation_obj.get_climate_Prov()
    assert province == "BEST TEST"
