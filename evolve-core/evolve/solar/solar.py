""" Module for managing solar modeling. """


# standard imports
from abc import ABC, abstractmethod
from typing import TypeAlias, Optional
import datetime

# third-party imports
from pydantic import (
    BaseModel,
    confloat,
    Field,
    model_validator,
    NonNegativeFloat,
    PositiveFloat,
    ConfigDict
)
import pandas as pd
from timezonefinder import TimezoneFinder
import pvlib

AzimuthType: TypeAlias = confloat(ge=0, le=360)
LatitudeType: TypeAlias = confloat(ge=-180, le=180)
TiltType: TypeAlias = confloat(ge=-90, le=90)
LongitudeType: TypeAlias = confloat(ge=-90, le=90)


class IrradianceRecordModel(BaseModel):
    """Interface for irradiance data model."""

    ghi: confloat(le=2000, ge=0) = Field(
        ..., description="Global Horizontal Irradiance watt/m^2."
    )
    dhi: confloat(le=2000, ge=0) = Field(
        ..., description="Diffuse Horizontal Irradiance watt/m^2."
    )
    dni: confloat(le=2000, ge=0) = Field(
        ..., description="Direct Normal Irradiance in watt/m^2."
    )
    temp: Optional[confloat(le=2000, ge=0)] = Field(
        None, description="Ambient temperature in degree celcius."
    )
    timestamp: datetime.datetime = Field(..., description="Timestamp")


class SolarBasicModel(BaseModel):
    """Interface for basic parameters required to model solar."""

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)
    longitude: LongitudeType = Field(
        ..., description="Longitude of location where solar is installed."
    )
    latitude: LatitudeType = Field(
        ..., description="Latitude of location where solar panel is installed."
    )
    kw: NonNegativeFloat = Field(..., description="Solar panel capacity in kW")
    irradiance: pd.DataFrame = Field(
        ..., description="Dataframe containing irradiance data."
    )

    @model_validator(mode="after")
    def validate_dataframe(self) -> "SolarBasicModel":
        """Validate irradiacne dataframe."""
        # pylint:disable=no-member
        records = self.irradiance.to_dict(orient="records")
        _ = [IrradianceRecordModel.model_validate(item) for item in records]
        return self


class AxisModel(BaseModel):
    """Abstract class for Axis model."""


class FixedAxisModel(AxisModel):
    """Interface for Fixed Axis Model"""

    surface_tilt: TiltType = Field(37, description="Surface tilt of solar panel.")
    surface_azimuth: AzimuthType = Field(
        180, description="Surface azimuth of solar panel."
    )


class SingleAxisModel(AxisModel):
    """Interface for Single Axis Model"""

    axis_tilt: TiltType = Field(37, description="Axis tilt in degrees.")
    axis_azimuth: AzimuthType = Field(180, description="Axis azimuth in degrees.")
    axis_max_tilt: TiltType = Field(
        85, description="Maximum axis tilt allowed in degrees."
    )


class DualAxisModel(AxisModel):
    """Interface for Dual Axis Model"""

    axis_max_tilt: TiltType = Field(85, description="Maximum tilt allowed in degrees.")


class InverterModel(BaseModel):
    """Interface Inverter Model"""

    acdcratio: PositiveFloat = Field(1.2, description="AC to DC ratio.")
    temp_coeff: float = Field(0.003, description="Temperature coefficient.")


class SolarModel(ABC):
    """Class for modeling solar panel."""

    def __init__(
        self,
        solar_basic_model: SolarBasicModel,
        inv_model: InverterModel,
    ):
        self.solar_basic_model = solar_basic_model
        self.inv_model = inv_model

    def _get_solar_location(self):
        # gets solar location and adds the apparent zenith and azimuth to irrad data
        solar_position = pvlib.solarposition.get_solarposition(
            self.solar_basic_model.irradiance.index,
            self.solar_basic_model.latitude,
            self.solar_basic_model.longitude,
        )

        self.solar_basic_model.irradiance[
            "apparent_zenith"
        ] = solar_position.apparent_zenith
        self.solar_basic_model.irradiance["azimuth"] = solar_position.azimuth
        self.solar_basic_model.irradiance.fillna(value=0, inplace=True)

    def _add_temperature_data(self):
        if "temp" not in self.solar_basic_model.irradiance.columns:
            self.solar_basic_model.irradiance["temp"] = 25.0

    def _format_times(self):
        tzone = TimezoneFinder().timezone_at(
            lng=self.solar_basic_model.longitude,
            lat=self.solar_basic_model.latitude,
        )

        self.solar_basic_model.irradiance["timestamp"] = pd.DatetimeIndex(
            self.solar_basic_model.irradiance["timestamp"], tz=tzone
        )

    def get_inverter_ac_output(self):
        """Method to compute inverter output."""
        _, poa_irradiance = self.get_poa()
        poa_irradiance = poa_irradiance.merge(
            self.solar_basic_model.irradiance["temp"], on="timestamp"
        ).fillna(value=0)

        dc_output = pd.DataFrame(
            pvlib.pvsystem.pvwatts_dc(
                g_poa_effective=poa_irradiance["poa_direct"],
                temp_cell=poa_irradiance["temp"],
                pdc0=self.solar_basic_model.kw,
                gamma_pdc=self.inv_model.temp_coeff,
                temp_ref=25.0,
            ),
            index=poa_irradiance.index,
        )

        dc_output.columns = ["output"]
        ac_output = pd.DataFrame(
            pvlib.inverter.pvwatts(
                pdc=dc_output,
                pdc0=self.solar_basic_model.kw * self.inv_model.acdcratio,
                eta_inv_nom=0.96,
                eta_inv_ref=0.9637,
            ),
            index=poa_irradiance.index,
            columns=["output"]
        )
        return list(ac_output["output"])

    @abstractmethod
    def get_poa(self):
        """Method to compute plabe of array irradiance."""
        self._format_times()
        self.solar_basic_model.irradiance.set_index(
            "timestamp", drop=True, inplace=True
        )
        self._get_solar_location()
        self._add_temperature_data()
        self.solar_basic_model.irradiance.to_csv("new_csv.csv")


class FixedAxisSolarModel(SolarModel):
    """Class to model fixed axis solar model."""

    def __init__(
        self,
        solar_basic_model: SolarBasicModel,
        axis_model: FixedAxisModel,
        inv_model: InverterModel,
    ):
        super().__init__(solar_basic_model, inv_model)
        self.axis_model = axis_model

    def get_poa(self):
        super().get_poa()

        return [
            self.axis_model.surface_tilt,
            self.axis_model.surface_azimuth,
        ], pd.DataFrame(
            pvlib.irradiance.get_total_irradiance(
                surface_tilt=self.axis_model.surface_tilt,
                surface_azimuth=self.axis_model.surface_azimuth,
                solar_zenith=self.solar_basic_model.irradiance["apparent_zenith"],
                solar_azimuth=self.solar_basic_model.irradiance["azimuth"],
                dni=self.solar_basic_model.irradiance["dni"],
                ghi=self.solar_basic_model.irradiance["ghi"],
                dhi=self.solar_basic_model.irradiance["dhi"],
            ),
            index=self.solar_basic_model.irradiance.index,
        )


class SingleAxisSolarModel(SolarModel):
    """Class to model single axis solar model"""

    def __init__(
        self,
        solar_basic_model: SolarBasicModel,
        axis_model: SingleAxisModel,
        inv_model: InverterModel,
    ):
        super().__init__(solar_basic_model, inv_model)
        self.axis_model = axis_model

    def get_poa(self):
        super().get_poa()

        single_axis_tracking_data = pd.DataFrame(
            pvlib.tracking.singleaxis(
                apparent_zenith=self.solar_basic_model.irradiance["apparent_zenith"],
                apparent_azimuth=self.solar_basic_model.irradiance["azimuth"],
                axis_tilt=self.axis_model.axis_tilt,
                axis_azimuth=self.axis_model.axis_azimuth,
                max_angle=self.axis_model.axis_max_tilt,
                backtrack=False,
            ),
            index=self.solar_basic_model.irradiance.index,
        ).fillna(value=0)

        return single_axis_tracking_data, pd.DataFrame(
            pvlib.irradiance.get_total_irradiance(
                surface_tilt=single_axis_tracking_data["surface_tilt"],
                surface_azimuth=single_axis_tracking_data["surface_azimuth"],
                solar_zenith=self.solar_basic_model.irradiance["apparent_zenith"],
                solar_azimuth=self.solar_basic_model.irradiance["azimuth"],
                dni=self.solar_basic_model.irradiance["dni"],
                ghi=self.solar_basic_model.irradiance["ghi"],
                dhi=self.solar_basic_model.irradiance["dhi"],
                # model="haydavies",
                # dni_extra=0,
            ),
            index=self.solar_basic_model.irradiance.index,
        )


class DualAxisSolarModel(SolarModel):
    """Class to model dual axis solar model."""

    def __init__(
        self,
        solar_basic_model: SolarBasicModel,
        axis_model: DualAxisModel,
        inv_model: InverterModel,
    ):
        super().__init__(solar_basic_model, inv_model)
        self.axis_model = axis_model

    def get_poa(self):
        super().get_poa()
        tracking_dict = {}

        for index, row in self.solar_basic_model.irradiance.iterrows():
            tracking_dict[index] = {}
            if row["apparent_zenith"] <= 90:
                # if sun is above horizon
                tracking_dict[index]["surface_azimuth"] = row["azimuth"]
                if row["apparent_zenith"] <= self.axis_model.axis_max_tilt:
                    tracking_dict[index]["surface_tilt"] = row["apparent_zenith"]

                else:
                    tracking_dict[index]["surface_tilt"] = self.axis_model.axis_max_tilt
            else:
                tracking_dict[index]["surface_azimuth"] = 0
        dual_axis_tracking_data = pd.DataFrame.from_dict(tracking_dict, orient="index")

        return dual_axis_tracking_data, pd.DataFrame(
            pvlib.irradiance.get_total_irradiance(
                surface_tilt=dual_axis_tracking_data["surface_tilt"],
                surface_azimuth=dual_axis_tracking_data["surface_azimuth"],
                solar_zenith=self.solar_basic_model.irradiance["apparent_zenith"],
                solar_azimuth=self.solar_basic_model.irradiance["azimuth"],
                dni=self.solar_basic_model.irradiance["dni"],
                ghi=self.solar_basic_model.irradiance["ghi"],
                dhi=self.solar_basic_model.irradiance["dhi"],
                # model="haydavies",
                # dni_extra=0,
            ),
            index=self.solar_basic_model.irradiance.index,
        )
