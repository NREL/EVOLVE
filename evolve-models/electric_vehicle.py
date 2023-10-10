""" Pydantic model for electric vehicle. """

# standard imports
from typing import Tuple, TypeAlias, Annotated, Literal

# third-party imports
# pylint:disable=no-name-in-module
from pydantic import (
    BaseModel,
    confloat,
    conint,
    PositiveInt,
    PositiveFloat,
    Field,
    StrictStr,
)

# Some constants used to avoid unrealistic large numbers
# small nnumbers

MAX_HOME_CHARGER_KW: float = 20.0
MAX_STATION_SLOT_KW: float = 500.0
MIN_CHARGER_KW: float = 1.0


PositiveFloatRangeField: TypeAlias = Tuple[PositiveFloat, PositiveFloat]
PositiveIntRangeField: TypeAlias = Tuple[PositiveInt, PositiveInt]
PctRangeField: TypeAlias = Tuple[confloat(ge=0, le=100), confloat(ge=0, le=100)]
DayHourRangeField: TypeAlias = Tuple[conint(ge=0, le=23), conint(ge=0, le=23)]


class ElectricVehiclesForm(BaseModel):
    """Interface for electric vehicle form data."""
    evType: Literal['vehicle'] = Field(..., description="Tag for electric vehcile.")
    id: StrictStr = Field(
        ..., description="Unique identifier for group of electric vehicles."
    )
    numberOfEV: PositiveInt = Field(
        ..., description="Number of electric vehicles to be modeled."
    )
    evCategoryName: StrictStr = Field(
        ..., description="Friendly name for group of vehicles to be modeled."
    )
    acceptedkW: PositiveFloatRangeField = Field(
        ..., description="Range of accepted kws for electric vehicles."
    )
    acceptedkWh: PositiveFloatRangeField = Field(
        ..., description="Range of energy capacities in kwh for electric vehicles."
    )
    mileage: PositiveFloatRangeField = Field(
        ..., description="Range of mileage to be used for electric vehicles."
    )
    weekdayMiles: PositiveFloatRangeField = Field(
        ..., description="Range of miles travelled on weekday"
    )
    weekendMiles: PositiveFloatRangeField = Field(
        ..., description="Range of miles travelled on weekends."
    )
    homeCharger: confloat(ge=MIN_CHARGER_KW, le=MAX_HOME_CHARGER_KW) = Field(
        ...,
        description="Maximum capaacity of home charger used for this group of vehicles.",
    )
    avergeMileage: PositiveFloat = Field(
        ..., description="Average mile travelled per hour."
    )
    weekdayTravelHours: DayHourRangeField = Field(
        ...,
        description="Range of hours indicating travel pattern for weekday e.g. [9,17]",
    )
    weekendTravelHours: DayHourRangeField = Field(
        ...,
        description="Range of hours indicating travel pattern for weekend e.g. [12,19]",
    )
    intialSocs: PctRangeField = Field(
        ..., description="Range of initial state of charges for vehicles."
    )


class ChargingStationsForm(BaseModel):
    """Interface for charging station form data."""
    evType: Literal['charging_station'] = Field(..., description="Tag for charging station.")
    id: StrictStr = Field(
        ..., description="Unique identifier for this group of charging stations."
    )
    stationCategoryName: StrictStr = Field(
        ..., description="Friendly name for this group of charging stations."
    )
    numberOfStations: PositiveInt = Field(
        ..., description="Number of stations to be modeled."
    )
    numberOfSlots: PositiveIntRangeField = Field(
        ...,
        description="Range of number of slots possible for a given charging station.",
    )
    maxSlotkW: confloat(ge=MIN_CHARGER_KW, le=MAX_STATION_SLOT_KW) = Field(
        ..., description="Maximum kW capacity for given slot."
    )


EVFormData: TypeAlias = Annotated[
    (ElectricVehiclesForm | ChargingStationsForm), Field(discriminator="evType")
]
