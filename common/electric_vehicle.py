""" Pydantic model for electric vehicle. """

# standard imports
from typing import Tuple, TypeAlias, Annotated, Literal, Optional

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
    PlainSerializer,
    model_validator,
)

# Some constants used to avoid unrealistic large numbers
# small nnumbers

MAX_HOME_CHARGER_KW: float = 20.0
MAX_STATION_SLOT_KW: float = 500.0
MIN_CHARGER_KW: float = 1.0

seralizer = PlainSerializer(
    lambda x: ",".join([str(el) for el in x]), return_type=str, when_used="json"
)

PositiveFloatRangeField: TypeAlias = Annotated[Tuple[PositiveFloat, PositiveFloat], seralizer]
PositiveIntRangeField: TypeAlias = Annotated[Tuple[PositiveInt, PositiveInt], seralizer]
PctRangeField: TypeAlias = Annotated[
    Tuple[confloat(ge=0, le=100), confloat(ge=0, le=100)], seralizer
]
DayHourRangeField: TypeAlias = Annotated[Tuple[conint(ge=0, le=23), conint(ge=0, le=23)], seralizer]


class ElectricVehiclesForm(BaseModel):
    """Interface for electric vehicle form data."""

    evType: Annotated[Literal["vehicle"], Field(..., description="Tag for electric vehcile.")]
    id: Annotated[
        StrictStr,
        Field(..., description="Unique identifier for group of electric vehicles."),
    ]
    numberOfEV: Annotated[
        PositiveInt,
        Field(..., description="Number of electric vehicles to be modeled."),
    ]
    evCategoryName: Annotated[
        StrictStr,
        Field(..., description="Friendly name for group of vehicles to be modeled."),
    ]
    acceptedkW: Annotated[
        PositiveFloatRangeField,
        Field(..., description="Range of accepted kws for electric vehicles."),
    ]
    acceptedkWh: Annotated[
        PositiveFloatRangeField,
        Field(..., description="Range of energy capacities in kwh for electric vehicles."),
    ]
    mileage: Annotated[
        PositiveFloatRangeField,
        Field(..., description="Range of mileage to be used for electric vehicles."),
    ]
    weekdayMiles: Annotated[
        PositiveFloatRangeField,
        Field(..., description="Range of miles travelled on weekday"),
    ]
    weekendMiles: Annotated[
        PositiveFloatRangeField,
        Field(..., description="Range of miles travelled on weekends."),
    ]
    homeCharger: Annotated[
        confloat(ge=MIN_CHARGER_KW, le=MAX_HOME_CHARGER_KW),
        Field(
            ...,
            description="Maximum capaacity of home charger used for this group of vehicles.",
        ),
    ]
    avergeMileage: Annotated[
        PositiveFloat, Field(..., description="Average mile travelled per hour.")
    ]
    weekdayTravelHours: Annotated[
        DayHourRangeField,
        Field(
            ...,
            description="Range of hours indicating travel pattern for weekday e.g. [9,17]",
        ),
    ]
    weekendTravelHours: Annotated[
        DayHourRangeField,
        Field(
            ...,
            description="Range of hours indicating travel pattern for weekend e.g. [12,19]",
        ),
    ]
    intialSocs: Annotated[
        PctRangeField,
        Field(..., description="Range of initial state of charges for vehicles."),
    ]
    preferredHours: Annotated[
        Optional[conint(ge=0, le=23)], Field(..., description="Preferred charge hour.")
    ] = None
    pctVehiclesForPreferredHour: Annotated[
        Optional[confloat(ge=0, le=100)], 
        Field(..., description="Percentage vehicles adopting preferred hours.")
    ] = 100

    @model_validator(mode="before")
    def modify_input_if_str(self):
        """Modify if the input is string."""
        float_params = [
            "acceptedkW",
            "acceptedkWh",
            "mileage",
            "weekdayMiles",
            "weekendMiles",
            "intialSocs",
        ]
        int_params = ["weekdayTravelHours", "weekendTravelHours"]
        for param in self:
            if isinstance(self.get(param, ""), str) and param in float_params:
                self[param] = [float(el) for el in self.get(param).split(",")]
            elif isinstance(self.get(param, ""), str) and param in int_params:
                self[param] = [int(el) for el in self.get(param).split(",")]
        return self


class ChargingStationsForm(BaseModel):
    """Interface for charging station form data."""

    evType: Annotated[
        Literal["charging_station"], Field(..., description="Tag for charging station.")
    ]
    id: Annotated[
        StrictStr,
        Field(..., description="Unique identifier for this group of charging stations."),
    ]
    stationCategoryName: Annotated[
        StrictStr,
        Field(..., description="Friendly name for this group of charging stations."),
    ]
    numberOfStations: Annotated[
        PositiveInt, Field(..., description="Number of stations to be modeled.")
    ]
    numberOfSlots: Annotated[
        PositiveIntRangeField,
        Field(
            ...,
            description="Range of number of slots possible for a given charging station.",
        ),
    ]
    maxSlotkW: Annotated[
        confloat(ge=MIN_CHARGER_KW, le=MAX_STATION_SLOT_KW),
        Field(..., description="Maximum kW capacity for given slot."),
    ]

    @model_validator(mode="before")
    def modify_input_if_str(self):
        """Modify if the input is string."""

        int_params = ["numberOfSlots"]
        for param in self:
            if isinstance(self.get(param, ""), str) and param in int_params:
                self[param] = [int(el) for el in self.get(param).split(",")]
        return self


EVFormData: TypeAlias = Annotated[
    (ElectricVehiclesForm | ChargingStationsForm), Field(discriminator="evType")
]
