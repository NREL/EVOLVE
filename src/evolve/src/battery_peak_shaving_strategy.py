""" Module for managing time based charging discharging strategy. """

# standard imports
import datetime
from typing import List, Dict

# third-party imports
from pydantic import BaseModel, confloat, conint, validator

# internal imports
from battery import GenericBattery

class PeakShavingCDStrategyInputModel(BaseModel):
    charging_threshold: confloat(gt=0, lt=0.5)
    discharging_threshold: confloat(ge=0.5, le=1.0)

class LoadProfileModel(BaseModel):
    timestamp: datetime.datetime 
    kw: float 


class PeakShavingBasedCDStrategy:
    """Implements peak shaving based charging discharging strategy."""

    def __init__(self, config: PeakShavingCDStrategyInputModel):
        self.config = config


    def handle_battery_charging(
        self, battery: GenericBattery, charging_period: float,
        peak_load: float, actual_load: float
    ):

        # available energy
        available_energy = (
            battery.battery_current_soc
            * battery.battery_params.energy_capacity_kwhr
        )
        energy_required_for_full_charge = (
            battery.battery_params.energy_capacity_kwhr - available_energy
        )

        charging_rate = peak_load*self.config.charging_threshold - actual_load

        if charging_rate <=0:
            raise ValueError(f"Charging rate can not be negative or zero.")


        if battery.battery_params.maximum_dod < charging_rate:
            charging_rate = battery.battery_params.maximum_dod

        charging_rate_expected = (
            energy_required_for_full_charge / charging_period
        )

        actual_rate = (
            charging_rate_expected
            if charging_rate > charging_rate_expected
            else charging_rate
        )

        battery.update_soc_power(-actual_rate, charging_period)
        

    def handle_battery_discharging(
        self, battery: GenericBattery, discharging_period: float,
        peak_load: float, actual_load: float  
    ):

        available_energy = (
            battery.battery_current_soc
            * battery.battery_params.energy_capacity_kwhr
        )
        self_discharge_energy = battery.compute_self_discharge_energy(
           discharging_period
        )

        discharging_rate = actual_load - peak_load*self.config.discharging_threshold

        if discharging_rate <=0:
            raise ValueError(f"Discharging rate can not be negative or zero.")

        if battery.battery_params.maximum_dod < discharging_rate:
            discharging_rate = battery.battery_params.maximum_dod

        discharging_rate_expected = (available_energy - self_discharge_energy) \
            / discharging_period
            
        actual_rate = (
            discharging_rate_expected
            if discharging_rate > discharging_rate_expected
            else discharging_rate
        )
        battery.update_soc_power(actual_rate, discharging_period)


    def simulate(
        self, load_profile: List[LoadProfileModel], battery: GenericBattery
    ):

        # Sorting timestamps into ascending order
        load_profile.sort(key=lambda x: x['timestamp'])
        max_load = max(load_profile, key=lambda x: x['kw'])['kw']

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

            if load.get('kw') < self.config.charging_threshold * max_load:
                # Reset battery self discharge hour
                battery.battery_since_last_charged = 0
                self.handle_battery_charging(battery, delta_time_in_hr, 
                    max_load, load.get('kw'))

            elif load.get('kw') >  self.config.discharging_threshold * max_load:
                self.handle_battery_discharging(battery, delta_time_in_hr,
                max_load, load.get('kw'))
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
