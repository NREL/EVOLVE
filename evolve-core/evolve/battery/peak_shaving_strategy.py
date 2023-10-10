""" Module for managing time based charging discharging strategy. """

# standard imports
import datetime

# third-party imports
from pydantic import BaseModel, PositiveFloat, Field, model_validator

# internal imports
from evolve.battery.battery import GenericBattery


class PeakShavingCDStrategyInputModel(BaseModel):
    """Interface for parameters to simulate peak shaving strategy for battery."""

    charging_threshold: PositiveFloat = Field(
        ...,
        description="Percentage charging threshold below which "
        "if load falls battery starts charging.",
    )
    discharging_threshold: PositiveFloat = Field(
        ...,
        description="Percenateg discharging threshold above which "
        "battery starts discharging.",
    )

    @model_validator(mode="after")
    def validate_thresholds(self) -> "PeakShavingCDStrategyInputModel":
        """Method to validate parameters for peak shaving strategy."""

        if self.charging_threshold >= self.discharging_threshold:
            raise ValueError(
                f"Charging threshold ({self.charging_threshold}) "
                f"must be greater than discharging threshold ({self.discharging_threshold})."
            )

        return self


class LoadProfileModel(BaseModel):
    """Interface for load profile model needed in peak shaving strategy."""

    timestamp: datetime.datetime = Field(..., description="Timestamp")
    kw: float = Field(..., description="kW load at this time.")


class PeakShavingBasedCDStrategy:
    """Implements peak shaving based charging discharging strategy."""

    def __init__(self, config: PeakShavingCDStrategyInputModel):
        self.config = config

    def handle_battery_charging(
        self,
        battery: GenericBattery,
        charging_period: float,
        peak_load: float,
        actual_load: float,
    ):
        """Method to handle battery charging."""
        # available energy
        available_energy = (
            battery.battery_current_soc * battery.battery_params.energy_capacity_kwhr
        )
        energy_required_for_full_charge = (
            battery.battery_params.energy_capacity_kwhr - available_energy
        )

        charging_rate = peak_load * self.config.charging_threshold - actual_load

        if charging_rate <= 0:
            raise ValueError("Charging rate can not be negative or zero.")

        if battery.battery_params.maximum_dod < charging_rate:
            charging_rate = battery.battery_params.maximum_dod

        charging_rate_expected = energy_required_for_full_charge / charging_period

        actual_rate = (
            charging_rate_expected
            if charging_rate > charging_rate_expected
            else charging_rate
        )

        battery.update_soc_power(-actual_rate, charging_period)

    def handle_battery_discharging(
        self,
        battery: GenericBattery,
        discharging_period: float,
        peak_load: float,
        actual_load: float,
    ):
        """Method to handle battery discharging."""
        available_energy = (
            battery.battery_current_soc * battery.battery_params.energy_capacity_kwhr
        )
        self_discharge_energy = battery.compute_self_discharge_energy(
            discharging_period
        )

        discharging_rate = actual_load - peak_load * self.config.discharging_threshold

        if discharging_rate <= 0:
            raise ValueError("Discharging rate can not be negative or zero.")

        if battery.battery_params.maximum_dod < discharging_rate:
            discharging_rate = battery.battery_params.maximum_dod

        discharging_rate_expected = (
            available_energy - self_discharge_energy
        ) / discharging_period

        actual_rate = (
            discharging_rate_expected
            if discharging_rate > discharging_rate_expected
            else discharging_rate
        )
        battery.update_soc_power(actual_rate, discharging_period)

    def simulate(self, load_profile: list[LoadProfileModel], battery: GenericBattery):
        """Method to simulate battery."""
        # Sorting timestamps into ascending order
        load_profile.sort(key=lambda x: x.timestamp)
        max_load = max(load_profile, key=lambda x: x.kw).kw

        # Loop over all the timestamps except last timestamp
        for index, load in enumerate(load_profile[:-1]):
            # Compute time in hr for next CD cycle
            delta_time_in_hr = (
                load_profile[index + 1].timestamp - load.timestamp
            ).seconds / 3600

            if delta_time_in_hr == 0:
                # Add the last timestep power to power profile if
                # this is the first time then add 0
                battery.battery_power_profile.append(
                    battery.battery_power_profile[-1]
                    if battery.battery_power_profile
                    else 0
                )
                continue

            if load.kw < self.config.charging_threshold * max_load:
                # Reset battery self discharge hour
                battery.battery_since_last_charged = 0
                self.handle_battery_charging(
                    battery, delta_time_in_hr, max_load, load.kw
                )

            elif load.kw > self.config.discharging_threshold * max_load:
                self.handle_battery_discharging(
                    battery, delta_time_in_hr, max_load, load.kw
                )
                battery.battery_since_last_charged += delta_time_in_hr
            else:
                battery.handle_battery_idling(delta_time_in_hr)
                battery.battery_since_last_charged += delta_time_in_hr

        if load_profile:
            # Add current soc as final SOC for the battery
            battery.battery_soc_profile.append(battery.battery_current_soc)
            battery.battery_power_profile.append(battery.battery_power_profile[-1])
