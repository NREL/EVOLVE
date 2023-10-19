""" This module contains higher level functions to interact with 
battery model and compute time series metrics.
"""

# Standard imports
from typing import List, Dict
import datetime


# Third-party imports
import numpy as np
import polars


# Internal imports
from evolve.battery.battery import GenericBattery, GenericBatteryParams
from evolve.battery.timed_strategy import (
    TimeBasedCDStrategyInputModel,
    TimeBasedCDStrategy,
)
from evolve.battery.peak_shaving_strategy import (
    PeakShavingCDStrategyInputModel,
    PeakShavingBasedCDStrategy,
)

from evolve.battery.self_consumption_strategy import (
    SelfConsumptionCDStrategy,
)
from common.energy_storage import ESFormData
from agent.helper_functions import populate_sliced_category, sort_metric_dataframe


def default_discharge_func(time_: float):
    """Deafult discharge function for battery."""
    dischargecurve = np.polyfit([0, 24, 720], [0, 5, 7], 2)

    return (dischargecurve[0] ** 2) * time_ + dischargecurve[1] * time_ + dischargecurve[2]


def time2num(time_str: str):
    """Convert time string to integer index."""
    if time_str == "12 AM":
        return 0

    if time_str == "12 PM":
        return 12

    return int(time_str.split(" ")[0]) + 12 if "PM" \
        in time_str else int(time_str.split(" ")[0])


def process_self_discharging_es(
    battery_instance: GenericBattery, battery: ESFormData, load_profiles: List[Dict]
):
    """Process self discharging for battery."""

    selfconsumption_cd_instance = SelfConsumptionCDStrategy()
    selfconsumption_cd_instance.simulate(load_profiles, battery_instance)

    return {
        "battery_power": [round(el, 3) for el in battery_instance.battery_power_profile],
        "battery_soc": [round(el, 3) for el in battery_instance.battery_soc_profile],
    }


def process_peak_shaving_es(
    battery_instance: GenericBattery, battery: ESFormData, load_profiles: List[Dict]
):
    """Process peak shaving strategy for battery."""

    peakshavingcdmodel = PeakShavingCDStrategyInputModel(
        charging_threshold=battery.chargingPowerThreshold / 100,
        discharging_threshold=battery.dischargingPowerThreshold / 100,
    )

    peakshaving_cd_instance = PeakShavingBasedCDStrategy(config=peakshavingcdmodel)
    peakshaving_cd_instance.simulate(load_profiles, battery_instance)

    return {
        "battery_power": [round(el, 3) for el in battery_instance.battery_power_profile],
        "battery_soc": [round(el, 3) for el in battery_instance.battery_soc_profile],
    }


def process_time_based_es(
    battery_instance: GenericBattery, battery: ESFormData, timestamps: List[datetime.datetime]
):
    """Process a single battery."""

    timecdmodel = TimeBasedCDStrategyInputModel(
        charging_hours=[time2num(el) for el in battery.chargingHours],
        discharging_hours=[time2num(el) for el in battery.disChargingHours],
        c_rate_charging=1 / battery.esChargingRate if battery.esChargingRate else 0.25,
        c_rate_discharging=1 / battery.esDischargingRate if battery.esDischargingRate else 0.25,
    )

    time_based_cd_instance = TimeBasedCDStrategy(config=timecdmodel)
    time_based_cd_instance.simulate(timestamps, battery_instance)

    return {
        "battery_power": [round(el, 3) for el in battery_instance.battery_power_profile],
        "battery_soc": [round(el, 3) for el in battery_instance.battery_soc_profile],
    }


def compute_es_energy_metric(battery_power_df: polars.DataFrame, resolution: int):
    """ Compute energy storage metric. """
    df = populate_sliced_category(battery_power_df)

    charging_new_df = polars.DataFrame()
    discharging_new_df = polars.DataFrame()

    for column in df.columns:
        if column not in ["timestamp", "category"]:
            charging_df = (
                df.filter(polars.col(column) < 0)
                .groupby("category")
                .agg(polars.col(column).sum())
                .with_column((polars.col(column) * (-resolution / 60)).alias(column))
                .select([column, "category"])
            )

            discharging_df = (
                df.filter(polars.col(column) > 0)
                .groupby("category")
                .agg(polars.col(column).sum())
                .with_column((polars.col(column) * (resolution / 60)).alias(column))
                .select([column, "category"])
            )

            if not len(charging_new_df):
                charging_new_df = charging_df
                discharging_new_df = discharging_df
            else:
                charging_new_df = charging_df.join(charging_new_df, on="category", how="left")
                discharging_new_df = discharging_df.join(
                    discharging_new_df, on="category", how="left"
                )
    return (charging_new_df, discharging_new_df)


def compute_energy_storage_metrics(
    battery_power_df: polars.DataFrame, resolution: int, base_path: str
):
    charging_energy_df, discharging_energy_df = compute_es_energy_metric(
        battery_power_df, resolution
    )

    charging_energy_df_sorted = sort_metric_dataframe(charging_energy_df)
    discharging_energy_df_sorted = sort_metric_dataframe(discharging_energy_df)
    charging_energy_df_sorted.write_csv(base_path / "es_charging_energy_metrics.csv")
    discharging_energy_df_sorted.write_csv(base_path / "es_discharging_energy_metrics.csv")


def process_energy_storage(
    batteries: List[ESFormData],
    load_df: polars.DataFrame,
    base_path: str,
    resolution: int,
):
    """Simulates battery."""

    battery_output = {}

    for battery in batteries:
        battery_params = GenericBatteryParams(
            maximum_dod=battery.esPowerCapacity,
            energy_capacity_kwhr=battery.esEnergyCapacity,
            initial_soc=battery.esInitialSOC if battery.esInitialSOC else 1.0,
            discharge_func=default_discharge_func,
            charging_efficiency=battery.esChargingEff if battery.esChargingEff else 1,
            discharging_efficiency=battery.esDischargingEff if battery.esDischargingEff else 1,
        )
        battery_instance = GenericBattery(battery_params)

        if battery.esStrategy == "time":
            battery_output[battery.name] = process_time_based_es(
                battery_instance, battery, load_df["timestamp"].to_list()
            )

        elif battery.esStrategy == "peak_shaving":
            battery_output[battery.name] = process_peak_shaving_es(
                battery_instance, battery, load_df.to_dicts()
            )

        elif battery.esStrategy == "self_consumption":
            battery_output[battery.name] = process_self_discharging_es(
                battery_instance, battery, load_df.to_dicts()
            )

    timestamps = load_df["timestamp"].to_list()
    timestamps.sort()

    battery_power_dict = {bname: bdict["battery_power"] for bname, bdict in battery_output.items()}
    battery_power_dict.update({"timestamp": timestamps})
    battery_power_df = polars.from_dict(battery_power_dict)

    battery_soc_dict = {bname: bdict["battery_soc"] for bname, bdict in battery_output.items()}
    battery_soc_dict.update({"timestamp": timestamps})
    battery_soc_df = polars.from_dict(battery_soc_dict)

    compute_energy_storage_metrics(battery_power_df, resolution, base_path)

    battery_power_df.write_csv(base_path / "battery_power_timeseries.csv")
    battery_soc_df.write_csv(base_path / "battery_soc_timeseries.csv")

    return battery_power_df

    # merged_df = load_df.join(battery_power_df, on='timestamp', how='left')
    # net_power = list(merged_df.select(polars.col('*').exclude('timestamp')).sum(axis=1))

    # return merged_df.with_columns(polars.Series(name='kW', values=net_power)).select(
    #     ['timestamp', 'kW']
    # )
