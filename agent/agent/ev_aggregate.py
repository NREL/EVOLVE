""" Module for handling high level inputs and creating ev level 
objects. """

from pydantic import BaseModel, Field, conint, confloat
from uuid import UUID, uuid4
from typing import List, Sequence, Tuple
import datetime
import random


import numpy as np
import polars as pl

from evolve.ev.ev_interfaces import (
    EVModel,
    ChargStationModel,
    ElectricCharger,
    ChargingSOCPreference,
    TravelPreference,
    ChargingLocation,
    ChargingNeedPreference,
    ChargTargetModel,
)
from evolve.ev.ev_constants import evolve_default_charge_func
from evolve.ev.ev_module import TransportationModel, ElectricVehicle, ChargingStations
from common.electric_vehicle import ElectricVehiclesForm, ChargingStationsForm


# class EVUIConfigInput(BaseModel):
#     """UI config input model for evolve."""

#     id: UUID = Field(default_factory=uuid4)
#     vehicle_type: str
#     num_of_vehicles: conint(gt=0)
#     kwh_range: Sequence[float]
#     kw_range: Sequence[float]
#     mileage_range: Sequence[float]
#     weekday_travel_miles: Sequence[float]
#     weekend_travel_miles: Sequence[float]
#     home_charger_kw: float = 1.2
#     average_mile_per_hour: confloat(gt=0)
#     weekday_travel_hours: Sequence[confloat(ge=0, le=23)]
#     weekend_travel_hours: Sequence[confloat(ge=0, le=23)]
#     start_soc: Sequence[float]


# class EVStationUIConfigInput(BaseModel):
#     """UI config input model for evolve."""

#     id: UUID = Field(default_factory=uuid4)
#     station_type: str
#     number_of_stations: conint(gt=0)
#     number_of_slot_per_station: Sequence[float]
#     charger_max_kw: confloat(gt=0)


class SimulationInputConfig(BaseModel):
    """Simulation config model for electric vehicles and stations."""

    start_time: datetime.datetime
    resolution_min: conint(gt=0)
    steps: conint(gt=0)


def get_travel_func(item: ElectricVehiclesForm):
    """Function to return travel preference func."""

    def get_travel_pref(day: datetime.date):
        if day.weekday() in [0, 1, 2, 3, 4]:
            travel_mile = np.random.randint(*item.weekdayMiles, 1)[0]
            return TravelPreference(
                daily_travel_hours=list(np.sort(item.weekdayTravelHours)),
                daily_travel_minute=int(travel_mile * 60 / item.avergeMileage),
                daily_travel_mile=travel_mile,
            )

        travel_mile = np.random.randint(*item.weekendMiles, 1)[0]
        return TravelPreference(
            daily_travel_hours=list(np.sort(item.weekendTravelHours)),
            daily_travel_minute=int(travel_mile * 60 / item.avergeMileage),
            daily_travel_mile=travel_mile,
        )

    return get_travel_pref


def get_charge_loc_func():
    """Function to return charge location function."""

    def get_charge_loc_pref(day: datetime.date):
        station_days = list(np.random.choice(range(7), 3, replace=False))
        if day.weekday() in station_days:
            return ChargingLocation.charging_station
        return ChargingLocation.residence

    return get_charge_loc_pref


def get_charge_need_func():
    """Function to return charge location function."""

    def get_charge_need_pref(day: datetime.date):
        soc_days = list(np.random.choice(range(7), 3, replace=False))

        if day.weekday() in soc_days:
            return ChargingNeedPreference(
                target=ChargTargetModel.soc_based, desired_soc=80
            )
        # TODO Assumed 2.5 hours
        return ChargingNeedPreference(
            target=ChargTargetModel.time_based, desired_duration=9000
        )

    return get_charge_need_pref


class EVTypeMapper(BaseModel):
    id: str
    type_: str


def random_electric_vehicles_builder_v1(
    vehicles: List[ElectricVehiclesForm], station_types: List[str]
) -> Tuple[List[EVModel], List[EVTypeMapper]]:
    """Builds a list of electric vehicles."""

    electric_vehicles: List[EVModel] = []
    electric_vehicle_type_mapper: List[EVTypeMapper] = []
    for item in vehicles:
        for id_ in range(item.numberOfEV):
            vehicle_id = f"{item.id}_{id_}"
            electric_vehicle_type_mapper.append(
                EVTypeMapper(id=vehicle_id, type_=item.evCategoryName)
            )
            electric_vehicles.append(
                EVModel(
                    id=vehicle_id,
                    soc=np.random.uniform(*item.intialSocs, 1)[0],
                    kwh=np.random.uniform(*item.acceptedkWh, 1)[0],
                    max_accepted_kw=np.random.uniform(*item.acceptedkW, 1)[0],
                    mileage_full=np.random.uniform(*item.mileage, 1)[0],
                    home_charger=ElectricCharger(
                        max_charger_kw=item.homeCharger,
                        soc_kw_func=evolve_default_charge_func,
                    ),
                    soc_preference=ChargingSOCPreference(min_soc=40, max_soc=80),
                    travel_pref=get_travel_func(item),
                    charge_loc_pref=get_charge_loc_func(),
                    charging_need_pref=get_charge_need_func(),
                    station_category_order=random.sample(
                        station_types, len(station_types)
                    ),
                )
            )

    return (electric_vehicles, electric_vehicle_type_mapper)


def random_charging_stations_builder_v1(
    stations: List[ChargingStationsForm],
) -> Tuple[List[ChargingStations], List[EVTypeMapper]]:
    """Function to build charging stations."""

    charging_stations: List[ChargStationModel] = []
    stations_type_mapper: List[EVTypeMapper] = []

    for item in stations:
        for id_ in range(item.numberOfStations):
            station_id: str = f"{item.id}_{id_}"
            stations_type_mapper.append(
                EVTypeMapper(id=station_id, type_=item.stationCategoryName)
            )
            charging_stations.append(
                ChargStationModel(
                    id=station_id,
                    num_of_slots=np.random.randint(*item.numberOfSlots, 1)[
                        0
                    ],
                    category_name=item.stationCategoryName,
                    charger=ElectricCharger(
                        max_charger_kw=item.maxSlotkW,
                        soc_kw_func=evolve_default_charge_func,
                    ),
                )
            )
    return (ChargingStations(stations=charging_stations), stations_type_mapper)


class LargeScaleEVSimulatorV1:
    """Class to simulate the electric vehicles and charging stations
    based on high level parameters."""

    def __init__(
        self, vehicles: List[ElectricVehiclesForm], stations: List[ChargingStationsForm]
    ):
        """Constructor for ev simulator."""

        self.station_types: List[str] = [item.stationCategoryName for item in stations]
        self.vehicle_types: List[str] = [item.evCategoryName for item in vehicles]

        (
            self.electric_vehicles,
            self.vehicle_mapper,
        ) = random_electric_vehicles_builder_v1(vehicles, self.station_types)
        (
            self.charging_stations,
            self.station_mapper,
        ) = random_charging_stations_builder_v1(stations)

    def simulate(self, sim_config: SimulationInputConfig):
        """Method to simulate large scale simulations."""

        vehicles = [
            ElectricVehicle(config=model, stations=self.charging_stations)
            for model in self.electric_vehicles
        ]

        trans_model = TransportationModel(
            vehicles=vehicles,
            stations=self.charging_stations,
            start_time=sim_config.start_time,
            resolution_min=sim_config.resolution_min,
            steps=sim_config.steps,
        )
        trans_model.simulate()
        return trans_model

    def aggregate_vehicle_results(
        self, trans_model: TransportationModel
    ) -> pl.DataFrame:
        """Internal method to aggregate results for various vehicle types."""

        vehicle_df = trans_model.get_ev_residence_charging_df()
        aggregated_data = {"timestamp": vehicle_df["Timestamps"]}

        for vehicle_type in self.vehicle_types:
            filtered_vehicles = [
                el.id for el in self.vehicle_mapper if el.type_ == vehicle_type
            ]
            aggregated_data[vehicle_type] = vehicle_df[filtered_vehicles].sum(axis=1)

        return pl.DataFrame(aggregated_data)

    def aggregate_station_results(
        self, trans_model: TransportationModel
    ) -> pl.DataFrame:
        """Internal method to aggregate results for various stattion types."""

        station_df = trans_model.get_stations_consumption_df()
        aggregated_data = {"timestamp": station_df["Timestamps"]}

        for station_type in self.station_types:
            filtered_stations = [
                el.id for el in self.station_mapper if el.type_ == station_type
            ]
            aggregated_data[station_type] = station_df[filtered_stations].sum(axis=1)
        return pl.DataFrame(aggregated_data)
