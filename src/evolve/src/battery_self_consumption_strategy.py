""" Module for managing time based charging discharging strategy. """

# standard imports
import datetime
from typing import List, Dict

# third-party imports
from pydantic import BaseModel, confloat, conint, validator

# internal imports
from battery import GenericBattery

class SelfConsumptionCDStrategyModel(BaseModel):
    discharging_threshold: confloat(ge=0, le=1.0)

class SelfConsumptionDataModel(BaseModel):
    timestamp: datetime.datetime 
    kW: float 


class SelfConsumptionCDStrategy:
    """Implements self consumption based charging discharging strategy."""

    def __init__(self, config: SelfConsumptionCDStrategyModel):
        self.config = config


    def handle_battery_charging(
        self, battery: GenericBattery, charging_period: float,
        kw_rate: float
    ):

        # available energy
        available_energy = (
            battery.battery_current_soc
            * battery.battery_params.energy_capacity_kwhr
        )
        energy_required_for_full_charge = (
            battery.battery_params.energy_capacity_kwhr - available_energy
        )

        if battery.battery_params.maximum_dod < kw_rate:
            kw_rate = battery.battery_params.maximum_dod

        rate_expected = (
            energy_required_for_full_charge / charging_period
        )

        actual_rate = (
            rate_expected
            if kw_rate > rate_expected
            else kw_rate
        )

        battery.update_soc_power(-actual_rate, charging_period)
        

    def handle_battery_discharging(
        self, battery: GenericBattery, discharging_period: float,
        kw_rate: float
    ):

        available_energy = (
            battery.battery_current_soc
            * battery.battery_params.energy_capacity_kwhr
        )
        self_discharge_energy = battery.compute_self_discharge_energy(
           discharging_period
        )

        if battery.battery_params.maximum_dod < kw_rate:
            kw_rate = battery.battery_params.maximum_dod

        rate_expected = (available_energy - self_discharge_energy) \
            / discharging_period
            
        actual_rate = (
            rate_expected
            if kw_rate > rate_expected
            else kw_rate
        )
        battery.update_soc_power(actual_rate, discharging_period)


    def simulate(
        self, load_profile: List[SelfConsumptionDataModel], battery: GenericBattery
    ):

        # Sorting timestamps into ascending order
        load_profile.sort(key=lambda x: x['timestamp'])

        # Loop over all the timestamps except last timestamp
        for id, load in enumerate(load_profile[:-1]):

            # Compute time in hr for next CD cycle
            delta_time_in_hr = (load_profile[id + 1].get('timestamp') 
                - load.get('timestamp')).seconds / 3600

            if delta_time_in_hr == 0:

                # Add the last timestep power to power profile if
                # this is the first time then add 0
                battery.battery_power_profile.append(
                    battery.battery_power_profile[-1]
                    if battery.battery_power_profile
                    else 0
                )
                continue

            if load.get('kW') < 0:
                # Reset battery self discharge hour
                battery.battery_since_last_charged = 0
                self.handle_battery_charging(battery, delta_time_in_hr, 
                    abs(load.get('kW')))

            elif load.get('kW') >  0:
                self.handle_battery_discharging(battery, delta_time_in_hr,
                    load.get('kW'))
                battery.battery_since_last_charged += delta_time_in_hr
            else:
                battery.handle_battery_idling(delta_time_in_hr)
                battery.battery_since_last_charged += delta_time_in_hr

        if load_profile:
            # Add current soc as final SOC for the battery
            battery.battery_soc_profile.append(battery.battery_current_soc)
            battery.battery_power_profile.append(
                battery.battery_power_profile[-1]
            )
