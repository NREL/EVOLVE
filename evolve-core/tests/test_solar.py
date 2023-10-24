""" Module for testing solar panel modeling in evolve."""

# standard imports
from pathlib import Path

# third-party imports
import pandas as pd
import pytest
from evolve.solar.solar import (
    FixedAxisModel,
    InverterModel,
    SolarBasicModel,
    FixedAxisSolarModel,
)

@pytest.fixture
def get_irradiance() -> pd.DataFrame:
    """ Fixture for fetching solar irradiance data. """
    return pd.read_csv(
        Path(__file__).parents[0] / "data" / "irradiance.csv", parse_dates=["timestamp"]
    )

# pylint:disable=redefined-outer-name
def test_fixed_axis_solar(get_irradiance):
    """Function to test fixed axis solar modeling."""


    solar_instance = FixedAxisSolarModel(
        solar_basic_model=SolarBasicModel(
            longitude=9.0, latitude=36.0, kw=5.0, irradiance=get_irradiance
        ),
        axis_model=FixedAxisModel(surface_azimuth=180, surface_tilt=20),
        inv_model=InverterModel(acdcratio=1.0),
    )

    solar_instance.get_inverter_ac_output()
