""" Module for managing time based charging discharging strategy. """

# standard imports
import datetime
from typing import TypeAlias

# third-party imports
from pydantic import BaseModel, confloat, conint, model_validator, Field

# internal imports
from evolve.battery.battery import GenericBattery

DayHoursType: TypeAlias = list[conint(le=23, ge=0)]
PctFloatType: TypeAlias = confloat(ge=0, le=10)


class TimeBasedCDStrategyInputModel(BaseModel):
    """Interface for time based charging discharging strategy for battery."""

    charging_hours: DayHoursType = Field(
        ..., description="List of hours for charging the battery."
    )
    discharging_hours: DayHoursType = Field(
        ..., description="List of hours for discharging the battery."
    )
    c_rate_charging: PctFloatType = Field(
        ..., description="C Rate for charging the battery"
    )
    c_rate_discharging: PctFloatType = Field(
        ..., description="C Rate for discharging the battery"
    )

    @model_validator(mode="after")
    def test_charging_discharging_hours(self) -> "TimeBasedCDStrategyInputModel":
        """Method to test charging discharging hours."""
        if set(self.charging_hours) & set(self.discharging_hours):
            raise ValueError(
                "Charging hours and discharging hours can not have \
                common value"
            )

        return self


class TimeBasedCDStrategy:
    """Implements time based charging discharging strategy."""

    def __init__(self, config: TimeBasedCDStrategyInputModel):
        self.config = config

    def handle_battery_charging(
        self, battery: GenericBattery, charging_period: float
    ) -> None:
        """Method to handle battery charging."""

        # available energy
        available_energy = (
            battery.battery_current_soc * battery.battery_params.energy_capacity_kwhr
        )
        energy_required_for_full_charge = (
            battery.battery_params.energy_capacity_kwhr - available_energy
        )

        # Let's convert c rate into power
        c_rate_to_kw = (
            self.config.c_rate_charging * battery.battery_params.energy_capacity_kwhr
        )

        if battery.battery_params.maximum_dod < c_rate_to_kw:
            c_rate_to_kw = battery.battery_params.maximum_dod

        charging_rate_expected = energy_required_for_full_charge / charging_period

        actual_rate = (
            charging_rate_expected
            if c_rate_to_kw > charging_rate_expected
            else c_rate_to_kw
        )

        battery.update_soc_power(-actual_rate, charging_period)

    def handle_battery_discharging(
        self, battery: GenericBattery, discharging_period: float
    ) -> None:
        """Method to handle discharging a battery."""
        available_energy = (
            battery.battery_current_soc * battery.battery_params.energy_capacity_kwhr
        )
        self_discharge_energy = battery.compute_self_discharge_energy(
            discharging_period
        )

        c_rate_to_kw = (
            self.config.c_rate_discharging * battery.battery_params.energy_capacity_kwhr
        )

        if battery.battery_params.maximum_dod < c_rate_to_kw:
            c_rate_to_kw = battery.battery_params.maximum_dod

        discharging_rate_expected = (
            available_energy - self_discharge_energy
        ) / discharging_period

        actual_rate = (
            discharging_rate_expected
            if c_rate_to_kw > discharging_rate_expected
            else c_rate_to_kw
        )
        battery.update_soc_power(actual_rate, discharging_period)

    def simulate(self, timestamps: list[datetime.datetime], battery: GenericBattery):
        """Method to handle time series simulation for the battery/"""

        # Sorting timestamps into ascending order
        timestamps.sort()

        # Loop over all the timestamps
        for id_, timestamp in enumerate(timestamps[:-1]):
            # Compute time in hr for next CD cycle
            delta_time_in_hr = (timestamps[id_ + 1] - timestamp).seconds / 3600

            if delta_time_in_hr == 0:
                # Add the last timestep power to power profile if
                # this is the first time then add 0
                battery.battery_power_profile.append(
                    battery.battery_power_profile[-1]
                    if battery.battery_power_profile
                    else 0
                )
                continue

            if timestamp.hour in self.config.charging_hours:
                # Reset battery self discharge hour
                battery.battery_since_last_charged = 0
                self.handle_battery_charging(battery, delta_time_in_hr)

            elif timestamp.hour in self.config.discharging_hours:
                self.handle_battery_discharging(battery, delta_time_in_hr)
                battery.battery_since_last_charged += delta_time_in_hr
            else:
                battery.handle_battery_idling(delta_time_in_hr)
                battery.battery_since_last_charged += delta_time_in_hr

        if timestamps:
            # Add current soc as final SOC for the battery
            battery.battery_soc_profile.append(battery.battery_current_soc)
            battery.battery_power_profile.append(battery.battery_power_profile[-1])
