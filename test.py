import datetime
from evolve.ev.ev_module import TransportationModel, ElectricVehicle, ChargingStations

from evolve.ev.ev_constants import evolve_default_charge_func
from evolve.ev.ev_interfaces import (
    ChargingSOCPreference,
    TravelPreference,
    ChargingLocation,
    ChargingNeedPreference,
    ChargTargetModel,
    ChargStationModel,
    EVModel,
    ElectricCharger,
)

# pylint: disable=missing-function-docstring

level_1_charger = ElectricCharger(
    max_charger_kw=1.2, soc_kw_func=evolve_default_charge_func
)
level_2_charger = ElectricCharger(
    max_charger_kw=7.6, soc_kw_func=evolve_default_charge_func
)
dc_fast_charger = ElectricCharger(
    max_charger_kw=50, soc_kw_func=evolve_default_charge_func
)
soc_preference = ChargingSOCPreference(min_soc=40, max_soc=80)


def get_travel_pref(day: datetime.date):
    if day.weekday() in [0, 1, 2, 3, 4]:
        return TravelPreference(
            daily_travel_hours=[9, 17], daily_travel_minute=120, daily_travel_mile=35
        )
    return TravelPreference(
        daily_travel_hours=[12, 19], daily_travel_minute=500, daily_travel_mile=80
    )


def odd_charge_loc_pref(day: datetime.date):
    if day.weekday() % 2 == 0:
        return ChargingLocation.residence
    return ChargingLocation.charging_station


def even_charge_loc_pref(day: datetime.date):
    if day.weekday() % 2 == 0:
        return ChargingLocation.charging_station
    return ChargingLocation.residence


def charging_need(day: datetime.date):
    if day.weekday() % 2 == 0:
        return ChargingNeedPreference(target=ChargTargetModel.soc_based, desired_soc=80)
    # return ChargingNeedPreference(target=ChargTargetModel.soc_based, desired_soc=80)
    return ChargingNeedPreference(
        target=ChargTargetModel.time_based, desired_duration=9000
    )


electric_vehicles = [
    {
        "id": "EV_1",
        "soc": 100,
        "kwh": 60,
        "max_accepted_kw": 10,
        "mileage_full": 60,  # 30 miles, below average miles,
        "home_charger": level_2_charger,
        "soc_preference": soc_preference,
        "travel_pref": get_travel_pref,
        "charge_loc_pref": odd_charge_loc_pref,
        "charging_need_pref": charging_need,
        "station_category_order": [],  # ["level_2", "level_1"],
    },
    {
        "id": "EV_2",
        "soc": 100,
        "kwh": 60,
        "max_accepted_kw": 40,
        "mileage_full": 300,
        "home_charger": level_2_charger,
        "soc_preference": soc_preference,
        "travel_pref": get_travel_pref,
        "charge_loc_pref": even_charge_loc_pref,
        "charging_need_pref": charging_need,
        "station_category_order": ["level_2", "dc_fast", "level_1"],
    },
    {
        "id": "EV_3",
        "soc": 100,
        "kwh": 60,
        "max_accepted_kw": 20,
        "mileage_full": 300,
        "home_charger": level_1_charger,
        "soc_preference": soc_preference,
        "travel_pref": get_travel_pref,
        "charge_loc_pref": odd_charge_loc_pref,
        "charging_need_pref": charging_need,
        "station_category_order": ["dc_fast", "level_1"],
    },
    {
        "id": "EV_4",
        "soc": 100,
        "kwh": 50,
        "max_accepted_kw": 40,
        "mileage_full": 250,
        "home_charger": level_2_charger,
        "soc_preference": soc_preference,
        "travel_pref": get_travel_pref,
        "charge_loc_pref": even_charge_loc_pref,
        "charging_need_pref": charging_need,
        "station_category_order": ["dc_fast", "level_2"],
    },
    {
        "id": "EV_5",
        "soc": 100,
        "kwh": 50,
        "max_accepted_kw": 20,
        "mileage_full": 280,
        "home_charger": level_1_charger,
        "soc_preference": soc_preference,
        "travel_pref": get_travel_pref,
        "charge_loc_pref": odd_charge_loc_pref,
        "charging_need_pref": charging_need,
        "station_category_order": ["level_2"],
    },
    {
        "id": "EV_6",
        "soc": 100,
        "kwh": 60,
        "max_accepted_kw": 40,
        "mileage_full": 350,
        "home_charger": level_2_charger,
        "soc_preference": soc_preference,
        "travel_pref": get_travel_pref,
        "charge_loc_pref": even_charge_loc_pref,
        "charging_need_pref": charging_need,
        "station_category_order": ["level_2"],
    },
]


charging_stations = [
    ChargStationModel(
        num_of_slots=2,
        charger=ElectricCharger(
            max_charger_kw=50, soc_kw_func=evolve_default_charge_func
        ),
        category_name="dc_fast",
        id="DC Fast Station",
    ),
    ChargStationModel(
        num_of_slots=2,
        charger=ElectricCharger(
            max_charger_kw=7.2, soc_kw_func=evolve_default_charge_func
        ),
        category_name="level_2",
        id="Level 2 Station",
    ),
    ChargStationModel(
        num_of_slots=1,
        charger=ElectricCharger(
            max_charger_kw=2.5, soc_kw_func=evolve_default_charge_func
        ),
        category_name="level_2",
        id="Level 3 Station",
    ),
]

stations = ChargingStations(stations=charging_stations)
ev_models = [EVModel(**item) for item in electric_vehicles]
vehicles = [ElectricVehicle(config=model, stations=stations) for model in ev_models]

trans_model = TransportationModel(
    vehicles=vehicles,
    stations=stations,
    start_time=datetime.datetime(2021, 1, 1, 0, 0, 0),
    resolution_min=60,
    steps=8760,
)
trans_model.simulate()
print(trans_model.get_ev_residence_charging_df())