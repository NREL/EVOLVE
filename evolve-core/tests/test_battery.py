""" Module for managing tests associated with battery."""

# standard tests
import datetime
from pathlib import Path

# Third-party imports
import numpy as np
import polars
import pandas as pd

# internal imports
from evolve.battery.battery import GenericBattery, GenericBatteryParams
from evolve.battery.timed_strategy import (
    TimeBasedCDStrategyInputModel,
    TimeBasedCDStrategy,
)
from evolve.battery.peak_shaving_strategy import (
    PeakShavingBasedCDStrategy,
    PeakShavingCDStrategyInputModel,
    LoadProfileModel
)


def default_discharge_func(time_: float) -> float:
    """ Default function for modeling self discharge of battery when idling."""
    dischargecurve = np.polyfit([0, 24, 720], [0, 5, 7], 2)

    return (
        (dischargecurve[0] ** 2) * time_ + dischargecurve[1] * time_ + dischargecurve[2]
    )

def test_timebased_strategy():
    """ Test for week long battery simulation using timebased strategy. """
    battery_params = GenericBatteryParams(
        maximum_dod=5,
        energy_capacity_kwhr=13.5,
        initial_soc=0.5,
        discharge_func=default_discharge_func,
    )

    battery_instance = GenericBattery(battery_params)
    timecdmodel = TimeBasedCDStrategyInputModel(
        charging_hours=[16, 17, 18, 19, 20],
        discharging_hours=[3, 4, 5, 6, 7],
        c_rate_charging=0.2,
        c_rate_discharging=0.2
    )

    time_based_cd_instance = TimeBasedCDStrategy(config=timecdmodel)

    timestamps = [
        datetime.datetime(2022, 1, 1, 0, 0, 0) + datetime.timedelta(minutes=15 * i)
        for i in range(96 * 7)
    ]
    time_based_cd_instance.simulate(timestamps, battery_instance)

    polars.from_dict(
        {
            "timestamps": timestamps,
            "battery_power": battery_instance.battery_power_profile,
            "battery_soc": battery_instance.battery_soc_profile,
        }
    )


def test_peak_shaving_strategy():
    """ Test peak shaving stragey for battery operation."""
    battery_params = GenericBatteryParams(
        maximum_dod=5,
        energy_capacity_kwhr=13.5,
        initial_soc=0.5,
        discharge_func=default_discharge_func,
    )

    battery_instance = GenericBattery(battery_params)
    peakshaving_model = PeakShavingCDStrategyInputModel(
        charging_threshold=0.4, discharging_threshold=0.7
    )

    peak_instance = PeakShavingBasedCDStrategy(config=peakshaving_model)

    loads = [LoadProfileModel.model_validate(item) for item in pd.read_csv(
        Path(__file__).parents[0] / "data" / "test_load.csv",
        parse_dates=["timestamp"],
    ).to_dict("records")]

    peak_instance.simulate(loads, battery_instance)

    pd.DataFrame.from_dict(
        {
            "timestamps": list(map(lambda x: x.timestamp, loads)),
            "battery_power": battery_instance.battery_power_profile,
            "battery_soc": battery_instance.battery_soc_profile,
            "loads": list(map(lambda x: x.kw, loads)),
        }
    )
