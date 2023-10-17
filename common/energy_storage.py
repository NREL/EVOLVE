""" Pydantic models for energy storage and related strategies."""

# standard imports
from typing import Optional, List, Annotated, TypeAlias, Literal

# third-party imports
# pylint:disable=no-name-in-module
from pydantic import (
    BaseModel,
    confloat,
    model_validator,
    StringConstraints,
    Field,
    PositiveFloat,
    StrictStr,
)

HourString: TypeAlias = Annotated[
    str, StringConstraints(pattern="[0-9] AM|[0-9] PM|1[0-2] AM|1[0-1] PM")
]


class _ESFormData(BaseModel):
    """Interface for energy storage model."""

    id: Annotated[StrictStr, Field(..., description="Unique identifier for energy storage.")]
    name: Annotated[StrictStr, Field(..., description="Friendly name for energy storage.")]
    esEnergyCapacity: Annotated[
        PositiveFloat, Field(..., description="Energy capacity of battery in kwh.")
    ]
    esPowerCapacity: Annotated[
        PositiveFloat, Field(..., description="Maximum power capacity for battery in kW.")
    ]
    esDischargingEff: Annotated[
        Optional[confloat(ge=0.2, le=1.0)],
        Field(0.95, description="Discharging efficiency for the battery."),
    ]
    esChargingEff: Annotated[
        Optional[confloat(ge=0.2, le=1.0)],
        Field(0.95, description="Charging efficiency for the battery."),
    ]
    esInitialSOC: Annotated[
        Optional[confloat(ge=0, le=1.0)],
        Field(1.0, description="Initial state of charge for the battery."),
    ]


class _ChargDischargRates(BaseModel):
    """Interface for storing charge and discharge rates."""

    esDischargingRate: Annotated[
        Optional[confloat(ge=0.01, le=100)],
        Field(0.5, description="Rate at which to discharge the battery."),
    ]
    esChargingRate: Annotated[
        Optional[confloat(ge=0.01, le=100)],
        Field(0.5, description="Rate at which to charge the battery."),
    ]


class TimeBasedESFormData(_ESFormData, _ChargDischargRates):
    """Interface for time based energy storage form data."""

    esStrategy: Annotated[
        Literal["time"], Field(..., description="Time based charging discharging strategy.")
    ]
    chargingHours: Annotated[
        List[HourString], Field(..., description="Hours for charging batteries.")
    ]
    disChargingHours: Annotated[
        List[HourString], Field(..., description="Hours for discharging batteries.")
    ]

    @model_validator(mode="after")
    def validate_charging_hours(self) -> "TimeBasedESFormData":
        """Method to validate charging and discharging hours."""

        if set(self.disChargingHours) & set(self.chargingHours):
            raise ValueError(
                "Charging hours and discharging hours should not have \
                duplicate values."
            )
        return self


class PriceBasedESFormData(_ESFormData, _ChargDischargRates):
    """Interface for price based form data."""

    esStrategy: Annotated[
        Literal["price"], Field(..., description="Price based charging discharging strategy.")
    ]
    chargingPrice: Annotated[
        PositiveFloat, Field(..., description="If price falls below this battery charging starts.")
    ]
    disChargingPrice: Annotated[
        PositiveFloat,
        Field(..., description="If prices goes above this, battery starts discharging."),
    ]
    priceProfile: Annotated[
        int, Field(..., description="Integer ID for price profile data in database. ")
    ]

    @model_validator(mode="after")
    def validate_prices(self) -> "PriceBasedESFormData":
        """Method to validate charging and discharging prices."""
        if self.chargingPrice >= self.disChargingPrice:
            raise ValueError(
                f"Charging price {self.chargingPrice} must be"
                f"less than discharging price {self.disChargingPrice}"
            )
        return self


class PeakShavingESFormData(_ESFormData, _ChargDischargRates):
    """Interface for power based form data."""

    esStrategy: Annotated[
        Literal["peak_shaving"],
        Field(..., description="Peak shaving charging discharging strategy."),
    ]
    chargingPowerThreshold: Annotated[
        confloat(gt=0, le=100),
        Field(
            ...,
            description="Percentage of peak load below which if load falls "
            "the battery starts to charge.",
        ),
    ]
    dischargingPowerThreshold: Annotated[
        confloat(gt=0, le=100),
        Field(
            ...,
            description="Percentage of peak load above which if load reaches, "
            "battery starts to dicharge.",
        ),
    ]

    @model_validator(mode="after")
    def validate_power_thresholds(self) -> "PeakShavingESFormData":
        """Method to validate charging and discharging power threshold."""
        if self.dischargingPowerThreshold >= self.chargingPowerThreshold:
            raise ValueError(
                f"Charging power threshold {self.chargingPowerThreshold} must be"
                f"less than discharging price {self.dischargingPowerThreshold}"
            )
        return self


class SelfConsumptionESFormData(_ESFormData):
    """Interface for self consumption based form data."""

    esStrategy: Annotated[
        Literal["self_consumption"],
        Field(..., description="Self consumption battery charging discharging strategy."),
    ]


ESFormData: TypeAlias = Annotated[
    (
        PriceBasedESFormData
        | TimeBasedESFormData
        | PeakShavingESFormData
        | SelfConsumptionESFormData
    ),
    Field(discriminator="esStrategy"),
]
