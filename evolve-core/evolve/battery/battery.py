""" Module for managing energy storage model."""

# standard imports
from typing import Callable


# third-party models
from pydantic import BaseModel, confloat, Field, PositiveFloat


class GenericBatteryParams(BaseModel):
    """Interface for Generic Battery."""

    maximum_dod: PositiveFloat = Field(
        ..., description="Maximum depth of discharge for battery."
    )
    energy_capacity_kwhr: PositiveFloat = Field(
        ..., description="Battery capacity in kWh."
    )
    initial_soc: confloat(ge=0, le=100) = Field(
        100, description="Initial state of charge for the battery."
    )
    discharge_func: Callable[[float], float] = Field(
        ...,
        description="Function that would return discharge "
         "percenatge based on current state of charge.",
    )
    charging_efficiency: confloat(ge=0.1, le=1.0) = Field(
        1.0, description="Charging efficiency for the battery."
    )
    discharging_efficiency: confloat(ge=0.1, le=1.0) = Field(
        1.0, description="Discharging efficiency for the battery."
    )


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

        self.battery_power_profile: list[float] = []
        self.battery_soc_profile: list[float] = []
        self.battery_since_last_charged: float = 0
        self.battery_current_soc:float = battery_params.initial_soc

    def get_power_profile(self) -> list[float]:
        """ Returns an array of power values in kW for battery. """
        return self.battery_power_profile

    def get_soc_profile(self) -> list[float]:
        """ Returns an array of state of charges for battery."""
        return self.battery_soc_profile

    def handle_battery_idling(self, discharging_period: float) -> None:
        """ Internal function to handle battery idling. """
        self_discharge_energy = self.compute_self_discharge_energy(discharging_period)

        actual_rate = self_discharge_energy / discharging_period

        if self.battery_params.maximum_dod < actual_rate:
            actual_rate = self.battery_params.maximum_dod

        self.update_soc_power(actual_rate, discharging_period)

    def update_soc_power(self, rate: float, period: float):
        """ Internal function to handle power and state of charge for the battery. """
        self.battery_soc_profile.append(round(self.battery_current_soc, 3))

        # available energy
        available_energy = (
            self.battery_current_soc * self.battery_params.energy_capacity_kwhr
        )

        self.battery_power_profile.append(rate)

        # Next available energy
        eff = (
            self.battery_params.charging_efficiency
            if rate < 0
            else self.battery_params.discharging_efficiency
        )

        next_available_energy = available_energy - rate * period * eff

        # Update soc for next time step
        self.battery_current_soc = (
            next_available_energy
        ) / self.battery_params.energy_capacity_kwhr

    def compute_self_discharge_energy(self, discharging_period: float):
        """ Methd to compute energy wasted when siting idle (self discharge). """
        available_energy = (
            self.battery_current_soc * self.battery_params.energy_capacity_kwhr
        )

        self_discharge = self.battery_params.discharge_func(
            self.battery_since_last_charged + discharging_period
        ) - self.battery_params.discharge_func(self.battery_since_last_charged)

        return available_energy * self_discharge / 100
