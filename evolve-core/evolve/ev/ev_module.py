""" Module for modeling electric vehicles. """

# standard imports
import datetime
from typing import List, Dict
import math

# third-party imports
import numpy as np
import polars as pl

# internal imports
from evolve.ev.ev_interfaces import (
    EVModel,
    ChargTargetModel,
    ChargStationModel,
    ChargingLocation,
)

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name


class ChargingStations:
    """Class for managing charging stations."""

    def __init__(self, stations: List[ChargStationModel]):
        self.stations = stations
        self.vehicle_id_station: Dict[str, ChargStationModel] = {}

        self.station_pct_occupied = {station.id: {} for station in self.stations}
        self.station_kw_consumed = {station.id: {} for station in self.stations}

    def attach_to_station(self, ev_id: str, category_pref: List[str]):
        """Method to attach electric vehicle to charging station."""

        if ev_id not in self.vehicle_id_station:
            filtered_stations = []
            for cat in category_pref:
                filtered_stations = [
                    station
                    for station in self.stations
                    if (station.category_name == cat) and (not station.is_full())
                ]
                if filtered_stations:
                    break

            if filtered_stations:
                # We found a station where you can charge

                chosen_station = filtered_stations[0]
                chosen_station.n_occupied += 1
                self.vehicle_id_station[ev_id] = chosen_station
                return chosen_station.id

    def _collect_results(self, charging_kw: float, station_id: str, timestamp: datetime.datetime):
        for station in self.stations:
            self.station_pct_occupied[station.id][timestamp] = round(
                station.n_occupied * 100 / station.num_of_slots, 3
            )

            if timestamp not in self.station_kw_consumed[station.id]:
                self.station_kw_consumed[station.id][timestamp] = 0

            if station_id == station.id:
                self.station_kw_consumed[station.id][timestamp] += charging_kw

    def get_charging_kw_for_ev(
        self,
        ev_id: str,
        max_accepted_kw: float,
        current_soc: float,
        timestamp: datetime.datetime,
    ):
        charging_kw = 0
        if ev_id in self.vehicle_id_station:
            station_ = self.vehicle_id_station[ev_id]

            charging_kw = min(
                self.vehicle_id_station[ev_id].charger.get_charging_kw(current_soc),
                max_accepted_kw,
            )

            self._collect_results(charging_kw, station_.id, timestamp)

        return charging_kw

    def detach_from_substation(self, ev_id: str):
        if ev_id in self.vehicle_id_station:
            self.vehicle_id_station[ev_id].n_occupied -= 1
            self.vehicle_id_station.pop(ev_id)


class ElectricVehicle:
    def __init__(self, config: EVModel, stations: ChargingStations):
        self.ev = config
        self.is_charging = False
        self.charging_duration_sec = 0
        self.stations = stations

        self.timestamps = []
        self.residence_charge_profile = []
        self.station_charg_profile = []
        self.discharge_kw = []
        self.socs = []

    def _get_travel_start_hours(self, day: datetime.date):
        """Internal method to get daily travel hours."""
        return self.ev.travel_pref(day).daily_travel_hours

    def _start_reset_charging(self):
        """Internal method to reset variables for next round of charging."""
        self.is_charging = True
        self.charging_duration_sec = 0

    def _end_reset_charging(self):
        """Internal method to reset variables for next round of charging."""
        self.is_charging = False
        self.charging_duration_sec = 0

    def get_station_charging_hours(self, day: datetime.date):
        """Method for getting hours to charge electric vehicle."""

        travel_hours = self._get_travel_all_hours(day)
        return list(set(list(range(min(travel_hours), max(travel_hours) + 1))) - set(travel_hours))

    def _get_travel_all_hours(self, day: datetime.date):
        """Method to get travel hours."""

        travel_start_hours = self._get_travel_start_hours(day)
        trip_duration_hour = math.ceil(self._get_trip_duration(day) / 60)
        return np.sort(
            np.array(
                [list(range(hr, hr + trip_duration_hour + 1)) for hr in travel_start_hours]
            ).flatten()
        )

    def _get_ntrips(self, day: datetime.date):
        """Method for getting number of trips for electric vehicle."""

        return len(self._get_travel_start_hours(day))

    def _get_trip_duration(self, day: datetime.date):
        """Method for getting trip duration."""

        # TODO: For now assuming trip duration and
        # trip miles are same for all trips in future we need to treat this
        # in a proportionate manner - Aug 28, 2023 (Kapil Duwadi)

        n_trips = self._get_ntrips(day)
        return int(self.ev.travel_pref(day).daily_travel_minute / n_trips)

    def get_house_arrival_hour(self, day: datetime.date):
        """Method for getting arrival hour for the electric vehicle."""
        arrival_hour = max(self._get_travel_all_hours(day)) + 1
        if arrival_hour > 23:
            raise ValueError(f"Arrival hour can not be greater than 23. {arrival_hour}")
        return arrival_hour

    def get_travel_kwhr(self, day: datetime.date, timestep_sec: float):
        """Method to compute energy consumed in one hour of travel."""

        travel_mile = (
            self.ev.travel_pref(day).daily_travel_mile
            / len(self._get_travel_all_hours(day))
            * timestep_sec
            / 3600
        )

        if travel_mile > self.ev.mileage_full:
            raise ValueError(f"Travel mile = {travel_mile}, Full Mileage = {self.ev.mileage_full}")

        return (self.ev.kwh * travel_mile) / self.ev.mileage_full

    def get_discharging_kw(self, day: datetime.date, timestep_sec: float):
        """Method to get discharging kw for electric vehicle."""
        energy_req_to_travel = self.get_travel_kwhr(day, timestep_sec)
        available_energy = self.ev.kwh * self.ev.soc / 100

        if available_energy < energy_req_to_travel:
            energy_req_to_travel = available_energy

        return -energy_req_to_travel / (timestep_sec / 3600)

    def get_hours_for_residence_charging(self, day: datetime.date):
        """Method for getting hours for residence charging."""

        return np.array(
            list(
                set(list(range(0, 24)))
                - set(self._get_travel_all_hours(day))
                - set(self.get_station_charging_hours(day))
            )
        )

    def _get_home_charging_kw(self):
        """Internal method to return home charging kW."""

        return min(
            [
                self.ev.home_charger.get_charging_kw(min(self.ev.soc, 100)),
                self.ev.max_accepted_kw,
            ]
        )

    def handle_residence_charging(self, day: datetime.date):
        """Method to take care of charging at residence."""

        # The electric vehicle is already charging
        # should continue charging until target is met
        # if self.is_charging and not self.is_charging_complete(day):
        if self.is_charging and self.ev.soc < self.ev.soc_preference.max_soc:
            return self._get_home_charging_kw()

        # The SOC dropped below desired soc so should be
        # charging now
        elif self.ev.soc <= self.ev.soc_preference.min_soc and not self.is_charging:
            self._start_reset_charging()
            return self._get_home_charging_kw()

        return 0

    def handle_station_charging(self, timestamp: datetime.datetime):
        """Handle electric vehicle charging at station."""
        # print(
        #     f"{timestamp} {self.is_charging} {self.is_charging_complete(timestamp.date())} {self.ev.soc, self.ev.soc_preference.min_soc}"
        # )
        if self.is_charging and not self.is_charging_complete(timestamp.date()):
            return self.stations.get_charging_kw_for_ev(
                self.ev.id, self.ev.max_accepted_kw, min(self.ev.soc, 100), timestamp
            )

        elif self.ev.soc <= self.ev.soc_preference.min_soc and not self.is_charging:
            self._start_reset_charging()
            station_id = self.stations.attach_to_station(self.ev.id, self.ev.station_category_order)
            print(f"EV {self.ev.id} attached to Station {station_id}")

            return self.stations.get_charging_kw_for_ev(
                self.ev.id, self.ev.max_accepted_kw, min(self.ev.soc, 100), timestamp
            )

        self.stations.detach_from_substation(self.ev.id)
        return 0

    def check_hour_for_residence_charging(self, timestamp: datetime.datetime):
        """Method for checking whether the hour
        is valid for residential charging."""

        is_cd_charg_loc_res = (
            self.ev.charge_loc_pref(timestamp.date()) == ChargingLocation.residence
        )
        is_pd_charg_loc_res = (
            self.ev.charge_loc_pref(timestamp.date() - datetime.timedelta(1))
            == ChargingLocation.residence
        )

        res_hours = self.get_hours_for_residence_charging(timestamp.date())
        evening_hours = res_hours[res_hours > 12]
        morning_hours = res_hours[res_hours < 12]

        if is_cd_charg_loc_res and timestamp.hour in evening_hours:
            if self.ev.preferred_charge_hour:
                return (
                    timestamp.hour >= self.ev.preferred_charge_hour
                    if self.ev.preferred_charge_hour > 12
                    else False
                )
            return True

        if is_pd_charg_loc_res and timestamp.hour in morning_hours:
            if self.ev.preferred_charge_hour:
                return (
                    timestamp.hour >= self.ev.preferred_charge_hour
                    if self.ev.preferred_charge_hour <= 12
                    else True
                )
            return True

        return False

    def _update_profile(self, charg_loc: ChargingLocation, charg_kw: float):
        self.discharge_kw.append(charg_kw if charg_kw < 0 else 0)
        self.residence_charge_profile.append(
            charg_kw if charg_loc == ChargingLocation.residence else 0
        )
        self.station_charg_profile.append(
            charg_kw if charg_loc == ChargingLocation.charging_station else 0
        )
        self.socs.append(self.ev.soc)

    # pylint: disable=arguments-differ
    def step(self, timestep_sec: float, timestamp: datetime.datetime):
        """Updates state of charge for the battery."""

        self.timestamps.append(timestamp)

        if timestep_sec <= 0:
            raise ValueError(f"Timestep must be greater than 0 {timestep_sec}")

        charging_kw = 0

        charging_location = None
        if timestamp.hour in self._get_travel_all_hours(timestamp.date()):
            charging_kw = self.get_discharging_kw(timestamp.date(), timestep_sec)
            self.stations.detach_from_substation(self.ev.id)

        if self.check_hour_for_residence_charging(timestamp):
            charging_kw = self.handle_residence_charging(timestamp.date())
            charging_location = ChargingLocation.residence
            self.stations.detach_from_substation(self.ev.id)

        if (timestamp.hour in self.get_station_charging_hours(timestamp.date())) and (
            (self.ev.charge_loc_pref(timestamp.date()) == ChargingLocation.charging_station)
        ):
            charging_kw = self.handle_station_charging(timestamp)
            charging_location = ChargingLocation.charging_station

        charging_kwh = charging_kw * timestep_sec / 3600
        self.ev.soc += charging_kwh * 100 / self.ev.kwh

        if self.ev.soc > 100:
            excess_kwh = (self.ev.soc-100)*(self.ev.kwh/100)
            charging_kw = (charging_kwh - excess_kwh)*3600/timestep_sec
            self.ev.soc = 100

        self._update_profile(charging_location, charging_kw)

        if charging_kw > 0:
            self.charging_duration_sec += timestep_sec
        else:
            self._end_reset_charging()

        return charging_kw

    def is_charging_complete(self, day: datetime.date) -> bool:
        """Method to get charging complete status."""

        if self.ev.soc >= self.ev.soc_preference.max_soc:
            return True

        ch_need = self.ev.charging_need_pref(day)
        if ch_need.target == ChargTargetModel.soc_based:
            return self.ev.soc >= ch_need.desired_soc

        if ch_need.target == ChargTargetModel.time_based:
            return self.charging_duration_sec >= ch_need.desired_duration


class TransportationModel:
    """Class for defining transportation model."""

    def __init__(
        self,
        vehicles: List[ElectricVehicle],
        stations: ChargingStations,
        start_time: datetime.datetime,
        resolution_min: int,
        steps: int,
    ):
        self.vehicles = vehicles
        self.vehicles_consumption = pl.DataFrame()
        self.vehicles_socs = pl.DataFrame()
        self.stations = stations

        self.timestamps = [
            start_time + datetime.timedelta(minutes=resolution_min * i) for i in range(steps)
        ]
        self.resolution_min = resolution_min

    def simulate(self):
        """Method to simulate electric vehicles."""

        for timestamp in self.timestamps:
            for vehicle in self.vehicles:
                vehicle.step(self.resolution_min * 60, timestamp)

    def get_ev_residence_charging_df(self) -> pl.DataFrame:
        """Method to gather dataframe storing the results of
        charging power for all electric vehicles."""

        data = {"Timestamps": self.timestamps}
        for vehicle in self.vehicles:
            data[vehicle.ev.id] = np.float16(vehicle.residence_charge_profile)

        return pl.DataFrame(data)

    def get_ev_station_charging_df(self) -> pl.DataFrame:
        """Method to gather dataframe storing the results of
        charging power for all electric vehicle charging stations."""

        data = {"Timestamps": self.timestamps}
        for vehicle in self.vehicles:
            data[vehicle.ev.id] = np.float16(vehicle.station_charg_profile)

        return pl.DataFrame(data)

    def get_ev_total_charging_df(self) -> pl.DataFrame:
        """Method to get total charging for electric vehicle."""
        data = {"Timestamps": self.timestamps}
        for vehicle in self.vehicles:
            data[vehicle.ev.id] = np.float16(vehicle.station_charg_profile) + np.float16(
                vehicle.residence_charge_profile
            )

        return pl.DataFrame(data)

    def get_ev_discharging_df(self) -> pl.DataFrame:
        """Method to gather dataframe storing the results of
        discharging power for all electric vehicles."""

        data = {"Timestamps": self.timestamps}
        for vehicle in self.vehicles:
            data[vehicle.ev.id] = vehicle.discharge_kw

        return pl.DataFrame(data)

    def get_ev_socs_df(self) -> pl.DataFrame:
        """Method to gather dataframe storing
        state of charges for all electric vehicles."""

        data = {"Timestamps": self.timestamps}
        for vehicle in self.vehicles:
            data[vehicle.ev.id] = vehicle.socs

        return pl.DataFrame(data)

    def get_stations_capacity_df(self) -> pl.DataFrame:
        """Method to gather the percentage
        station capacities."""

        data = {"Timestamps": self.timestamps}
        for station, subdict in self.stations.station_pct_occupied.items():
            zero_dict = dict(zip(self.timestamps, np.zeros(len(self.timestamps))))
            zero_dict.update(subdict)
            data[station] = list(zero_dict.values())

        return pl.DataFrame(data)

    def get_stations_consumption_df(self) -> pl.DataFrame:
        """Method to gather the percentage
        station capacities."""

        data = {"Timestamps": self.timestamps}
        # TODO : There is a better way for creating this dataframe
        for station, subdict in self.stations.station_kw_consumed.items():
            zero_dict = dict(zip(self.timestamps, np.zeros(len(self.timestamps))))
            zero_dict.update(subdict)
            data[station] = list(zero_dict.values())

        return pl.DataFrame(data)
