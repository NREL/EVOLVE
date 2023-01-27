""" Module for managing energy storage model."""

# standard imports
from typing import Callable, List


# third-party models
from pydantic import BaseModel, confloat, conint, validator


class GenericBatteryParams(BaseModel):
    maximum_dod: float
    energy_capacity_kwhr: float
    initial_soc: confloat(ge=0, le=100) = 100
    discharge_func: Callable[[float], float]


class GenericBattery:
    """Generic battery model. Simplified battery model.

    Models battery self discharge. Keeps track of charging and discharging
    of battery.

    Attributes:
        battery_params (GenericBatteryParams): Battery parameter setting
        battery_power_profile (List[float]): Time series battery power profile
            . Positive for discharging, negative for charging.
        battery_soc_profile (List[float]): Timeseries state of charge of battery
    """

    def __init__(self, battery_params: GenericBatteryParams):

        self.battery_params = battery_params
        
        self.battery_power_profile = []
        self.battery_soc_profile = []
        self.battery_since_last_charged = 0
        self.battery_current_soc = battery_params.initial_soc

    def get_power_profile(self):
        return self.battery_power_profile

    def get_soc_profile(self):
        return self.battery_soc_profile

    def handle_battery_idling(
        self, discharging_period: float
    ):
        
        self_discharge_energy = self.compute_self_discharge_energy(
             discharging_period
        )

        actual_rate = self_discharge_energy/discharging_period
        
        if self.battery_params.maximum_dod < actual_rate:
            actual_rate = self.battery_params.maximum_dod

        self.update_soc_power(actual_rate, discharging_period)

    def update_soc_power(self, rate: float, period: float):

        self.battery_soc_profile.append(
                round(self.battery_current_soc, 3)
            )

        # available energy
        available_energy = (
            self.battery_current_soc
            * self.battery_params.energy_capacity_kwhr
        )

        self.battery_power_profile.append(rate)

        # Next available energy
        next_available_energy = available_energy - rate * period

        # Update soc for next time step
        self.battery_current_soc = (
            (next_available_energy) /self.battery_params.energy_capacity_kwhr
        )

    def compute_self_discharge_energy(
        self, discharging_period: float
    ):

        available_energy = (
            self.battery_current_soc
            * self.battery_params.energy_capacity_kwhr
        )

        self_discharge = self.battery_params.discharge_func(
            self.battery_since_last_charged + discharging_period) - self.battery_params.discharge_func(
            self.battery_since_last_charged)

        return available_energy*self_discharge/100

    


