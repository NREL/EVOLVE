# standard imports
from typing import Callable, Optional, List
from enum import Enum
import datetime

# third-party imports
# pylint: disable=no-name-in-module
from pydantic import (
    BaseModel,
    confloat,
    conint,
    PositiveFloat,
    NonNegativeInt,
    Field,
    PositiveInt,
    StrictStr,
    model_validator,
    NonNegativeFloat,
)


class ElectricCharger(BaseModel):
    """Class for modeling abstract electric charger."""

    max_charger_kw: PositiveFloat = Field(..., description="Maximum kW output for this charger.")
    soc_kw_func: Callable[[float], float]

    def get_charging_kw(self, soc: float) -> float:
        """Returns charging kw for a given soc level"""
        return float(self.soc_kw_func(soc) * self.max_charger_kw)


# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
class ChargTargetModel(str, Enum):
    time_based = "time_based"
    soc_based = "soc_based"


class ChargingLocation(str, Enum):
    residence = "residence"
    charging_station = "charging_station"


# pylint: disable=missing-function-docstring
# pylint: disable=no-self-argument


class ChargStationModel(BaseModel):
    """Interface for Charging Station Model configuration."""

    num_of_slots: PositiveInt = Field(..., description="Number of slots in this charging station.")
    charger: ElectricCharger = Field(..., description="Electric charger interface instance.")
    n_occupied: conint(ge=0) = Field(
        0, description="Internally updated number of slots occupied for this station."
    )
    category_name: StrictStr = Field(..., description="Category name for this station.")
    id: StrictStr = Field(..., description="Unique identifier for this station.")

    def is_full(self) -> bool:
        """Method to indicate whether the station is full or not."""

        return self.n_occupied >= self.num_of_slots


class TravelPreference(BaseModel):
    """Interface for defining travel preference for
    electric vehicle."""

    daily_travel_mile: NonNegativeInt = Field(..., description="Miles travelled in a day.")
    daily_travel_minute: NonNegativeInt = Field(..., description="Minutes travelled in a day.")
    daily_travel_hours: List[conint(ge=0, le=23)] = Field(
        ..., description="List of day hours indicating start of travel."
    )


class ChargingSOCPreference(BaseModel):
    """Interface for defining charging preference
    for electric vehicle."""

    min_soc: NonNegativeInt = Field(
        ..., description="Minimum state of charge allowed for the battery."
    )
    max_soc: NonNegativeInt = Field(
        ..., description="Maximum state of charge allowed for the battery."
    )

    @model_validator(mode="after")
    def validate_socs(self) -> "ChargingSOCPreference":
        """Method to validate state of charges."""
        if self.min_soc >= self.max_soc:
            raise ValueError(
                f"Max SOC ({self.max_soc}) must be greater " f"than Min SOC ({self.min_soc})"
            )
        return self


class ChargingNeedPreference(BaseModel):
    """Interface for defining charging need preference."""

    target: ChargTargetModel = Field(..., description="Target for charging need.")
    desired_soc: Optional[float] = Field(None, description="Desired state of charge in percentage.")
    desired_duration: Optional[float] = Field(
        None, description="Desired charging duration if target is duration."
    )

    @model_validator(mode="after")
    def validated_desired_soc(self) -> "ChargingNeedPreference":
        if self.target == "soc_based" and self.desired_soc is None:
            raise ValueError("desired_soc should be defined for soc based strategy!")
        return self

    @model_validator(mode="after")
    def validated_desired_duration(self) -> "ChargingNeedPreference":
        if self.target == "time_based" and self.desired_duration is None:
            raise ValueError("desired_duration should be defined for soc based strategy!")
        return self



class EVModel(BaseModel):
    """EV model for the single electric vehicle unit."""

    id: str
    soc: confloat(ge=0, le=100)
    kwh: PositiveFloat
    max_accepted_kw: PositiveFloat
    mileage_full: NonNegativeFloat
    home_charger: ElectricCharger
    preferred_charge_hour: Optional[conint(ge=0, le=23)] = None
    soc_preference: ChargingSOCPreference
    travel_pref: Callable[[datetime.date], TravelPreference]
    charge_loc_pref: Callable[[datetime.date], ChargingLocation]
    charging_need_pref: Callable[[datetime.date], ChargingNeedPreference]
    station_category_order: List[str]



class EVModelingInput(BaseModel):
    """Input model for simulating EV."""

    number_of_evs: conint(ge=1)
    residential_percentage: confloat(gt=0, le=100)
    annual_growth_percentage: confloat(gt=0, le=100)
    number_of_days: conint(ge=1)
    bike_percentage: confloat(gt=0, le=100)
    cars_percentage: confloat(gt=0, le=100)
    number_of_years: conint(ge=1)
    time_resolution_min: conint(ge=1)


class EVVehicleConstants(BaseModel):
    initial_min_soc: confloat(ge=0, le=100) = 5
    initial_max_soc: confloat(ge=0, le=100) = 50
    arrival_min_hour: conint(ge=0, le=23) = 16
    arrival_max_hour: conint(ge=0, le=23) = 23
    desired_soc_min: confloat(ge=0, le=100) = 50
    desired_soc_max: confloat(ge=0, le=100) = 80
    weekday_min_mile: NonNegativeInt = 20
    weekday_max_mile: NonNegativeInt = 40
    weekend_min_mile: NonNegativeInt = 60
    weekend_max_mile: NonNegativeInt = 80


class ChargingStationConstants(BaseModel):
    min_num_slots: conint(ge=1) = 3
    max_num_slots: conint(ge=1) = 20
    pct_level_first_stations: confloat(ge=0, le=100) = 30
    pct_level_second_stations: confloat(ge=0, le=100) = 50
    pct_dc_stations: confloat(ge=0, le=100) = 20
    min_dc_station_kw: confloat(ge=50, le=350) = 50
    max_dc_station_kw: confloat(ge=50, le=350) = 350
    min_l1_kw: confloat(ge=1.0, le=2.4) = 1.3
    max_l1_kw: confloat(ge=1.0, le=2.4) = 2.4
    min_l2_kw: confloat(ge=6.2, le=19.2) = 6.2
    max_l2_kw: confloat(ge=6.2, le=19.2) = 19.2
