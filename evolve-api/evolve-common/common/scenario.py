""" This module contains pydantic model for DER Scenario. """
# standard imports
import datetime
from typing import Optional
from enum import Enum
from typing_extensions import Annotated

# third-party imports
from pydantic import BaseModel, Field, NonNegativeInt, model_validator

# internal imports
from common.solar import SolarFormData
from common.energy_storage import ESFormData
from common.electric_vehicle import EVFormData


class DataFillingStrategy(Enum):
    """Data filing strategies."""

    interpolation = "interpolation"
    staircase = "staircase"


class DERTechnologies(Enum):
    """Interface for valid DER technologies."""

    solar = "solar"
    ev = "ev"
    energy_storage = "energy_storage"


class BasicFormData(BaseModel):
    """Interface for basic form data."""

    dataFillingStrategy: Annotated[
        Optional[DataFillingStrategy],
        Field(None, description="Specify how you want to fill missing data."),
    ]
    endDate: Annotated[datetime.date, Field(..., description="End date for simulation.")]
    startDate: Annotated[datetime.date, Field(..., description="Start date for simulaion.")]
    loadProfile: Annotated[
        int, Field(..., description="Unique id to access load profile from database.")
    ]
    resolution: Annotated[
        NonNegativeInt,
        Field(..., description="Time resolution in minute for simulation."),
    ]
    scenarioName: Annotated[str, Field(..., description="Friendly name for a scenario.")]
    scenarioDescription: Annotated[
        str, Field(..., description="Friendly name for a scenario.")
    ] = "Deafult description."
    technologies: Annotated[
        list[DERTechnologies],
        Field(..., description="List of DER technologies to simulate."),
    ]

    @model_validator(mode="after")
    def start_date_must_be_smaller(self) -> "BasicFormData":
        """Method to check start date is less than end date."""
        if self.startDate >= self.endDate:
            raise ValueError(
                f"Start date {self.startDate} can not be greater than \
                end date {self.endDate}"
            )

        return self


class ScenarioData(BaseModel):
    """Interface for scenario form data."""

    basic: BasicFormData
    solar: list[SolarFormData]
    ev: list[EVFormData]
    energy_storage: list[ESFormData]
