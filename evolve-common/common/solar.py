""" Pydantic model for solar module. """

# standard imports
from typing import TypeAlias, Annotated, Literal

# third-party imports
# pylint:disable=no-name-in-module
from pydantic import BaseModel, confloat, Field, PositiveFloat


AzimuthType: TypeAlias = confloat(ge=0, le=360)
LatitudeType: TypeAlias = confloat(ge=-180, le=180)
TiltType: TypeAlias = confloat(ge=-90, le=90)
LongitudeType: TypeAlias = confloat(ge=-90, le=90)


class _SolarFormData(BaseModel):
    """Interface for solar form data."""

    id: Annotated[
        str, Field(..., description="Unique identifier for solar installation.")
    ]
    name: Annotated[
        str, Field(..., description="Friendly name for solar installation type.")
    ]
    dcacRatio: Annotated[
        confloat(ge=0.2, le=2.0),
        Field(..., description="DC to AC ratio for modeling inverter. "),
    ]
    irradianceData: Annotated[
        int,
        Field(
            ..., description="Integer ID for irradiance profile stored in database. "
        ),
    ]
    longitude: Annotated[
        LongitudeType,
        Field(9.5, description="Longitude where solar panel is installed."),
    ]
    latitude: Annotated[
        LatitudeType, Field(33.88, description="Latitude where solar panel is installed.")
    ]
    solarCapacity: Annotated[
        PositiveFloat, Field(..., description="Capacity of solar panel in kW.")
    ]


class FixedAxisSolarFormData(_SolarFormData):
    """Interface for fixed axis solar form data."""

    solarInstallationStrategy: Annotated[
        Literal["fixed"], Field(..., description="Fixed axis solar installation.")
    ]
    panelAzimuth: Annotated[
        AzimuthType, Field(..., description="Surface azimuth of the panel in degrees.")
    ]
    panelTilt: Annotated[
        TiltType, Field(..., description="Surface tilt of the panel in degrees.")
    ]


class SingleAxisSolarFormData(_SolarFormData):
    """Interface for single axis solar form data."""

    solarInstallationStrategy: Annotated[
        Literal["single_axis"],
        Field(..., description="Single axis tracking installation."),
    ]
    panelAzimuth: Annotated[
        AzimuthType, Field(..., description="Axis azimuth of the panel in degrees.")
    ]
    panelTilt: Annotated[
        TiltType, Field(..., description="Axis tilt of the panel in degrees.")
    ]


class DualAxisSolarFormData(_SolarFormData):
    """Interface for dual axis solar form data."""

    solarInstallationStrategy: Annotated[
        Literal["dual_axis"], Field(..., description="Dual axis tracking installation.")
    ]


SolarFormData: TypeAlias = Annotated[
    (FixedAxisSolarFormData | SingleAxisSolarFormData | DualAxisSolarFormData),
    Field(discriminator="solarInstallationStrategy"),
]
