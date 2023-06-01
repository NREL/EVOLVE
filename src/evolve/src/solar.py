""" Module for managing solar modeling. 

Examples:

from model import (
    FixedAxisSolarModel,
    SolarBasicModel,
    InverterModel,
    FixedAxisModel,
)
import pandas as pd

base_path = r"f89fccd6-c618-46c7-b7c9-0a65d46f8d2c.csv"
df = pd.read_csv(base_path, parse_dates=["timestamp"])

fixed = FixedAxisSolarModel(
    solar_basic_model=SolarBasicModel(
        longitude=36, latitude=9, kw=40, irradiance=df
    ),
    axis_model=FixedAxisModel(),
    inv_model=InverterModel(),
)
df = fixed.get_inverter_output()
"""


# standard imports
from abc import ABC, abstractmethod
from typing import List
import datetime

# third-party imports
import pydantic
from pydantic import BaseModel, confloat, validator
import pandas as pd
from timezonefinder import TimezoneFinder
import pvlib


class IrradianceRecordModel(BaseModel):
    ghi: confloat(le=2000, ge=0)
    dhi: confloat(le=2000, ge=0)
    dni: confloat(le=2000, ge=0)
    timestamp: datetime.datetime


class SolarBasicModel(BaseModel):
    longitude: float
    latitude: float
    kw: float
    irradiance: pd.DataFrame

    @validator("irradiance")
    def validate_dataframe(cls, v):
        records = v.to_dict(orient="records")
        pydantic.parse_obj_as(List[IrradianceRecordModel], records)
        return v

    class Config:
        arbitrary_types_allowed = True


class AxisModel(BaseModel):
    pass


class FixedAxisModel(AxisModel):
    surface_tilt: confloat(ge=-90, le=90) = 37
    surface_azimuth: confloat(ge=0, le=360) = 180


class SingleAxisModel(AxisModel):
    axis_tilt: confloat(ge=-90, le=90) = 37
    axis_azimuth: confloat(ge=0, le=360) = 180
    axis_max_tilt: confloat(ge=-90, le=90) = 85


class DualAxisModel(AxisModel):
    axis_max_tilt: confloat(ge=-90, le=90) = 85


class InverterModel(BaseModel):
    acdcratio: float = 1.2
    temp_coeff: float = 0.003


class SolarModel(ABC):
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

    def get_inverter_output(self):

        poa_irradiance = self.get_poa()
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

        dc_output.columns = ["DC_Output"]

        ac_output = pd.DataFrame(
            pvlib.inverter.pvwatts(
                pdc=dc_output,
                pdc0=self.solar_basic_model.kw * self.inv_model.acdcratio,
                eta_inv_nom=0.96,
                eta_inv_ref=0.9637,
            ),
            index=poa_irradiance.index,
        )

        ac_output.columns = ["AC_Output"]
        return ac_output

    @abstractmethod
    def get_poa(self):
        self._format_times()
        self.solar_basic_model.irradiance.set_index(
            "timestamp", drop=True, inplace=True
        )
        self._get_solar_location()
        self._add_temperature_data()


class FixedAxisSolarModel(SolarModel):
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

        return pd.DataFrame(
            pvlib.irradiance.get_total_irradiance(
                surface_tilt=self.axis_model.surface_tilt,
                surface_azimuth=self.axis_model.surface_azimuth,
                solar_zenith=self.solar_basic_model.irradiance[
                    "apparent_zenith"
                ],
                solar_azimuth=self.solar_basic_model.irradiance["azimuth"],
                dni=self.solar_basic_model.irradiance["dni"],
                ghi=self.solar_basic_model.irradiance["ghi"],
                dhi=self.solar_basic_model.irradiance["dhi"],
            ),
            index=self.solar_basic_model.irradiance.index,
        )


class SingleAxisSolarModel(SolarModel):
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
                apparent_zenith=self.solar_basic_model.irradiance[
                    "apparent_zenith"
                ],
                apparent_azimuth=self.solar_basic_model.irradiance["azimuth"],
                axis_tilt=self.axis_model.axis_tilt,
                axis_azimuth=self.axis_model.axis_azimuth,
                max_angle=self.axis_model.axis_max_tilt,
                backtrack=False,
            ),
            index=self.solar_basic_model.irradiance.index,
        ).fillna(value=0)

        return pd.DataFrame(
            pvlib.irradiance.get_total_irradiance(
                surface_tilt=single_axis_tracking_data["surface_tilt"],
                surface_azimuth=single_axis_tracking_data["surface_azimuth"],
                solar_zenith=self.solar_basic_model.irradiance[
                    "apparent_zenith"
                ],
                solar_azimuth=self.solar_basic_model.irradiance["azimuth"],
                dni=self.solar_basic_model.irradiance["dni"],
                ghi=self.solar_basic_model.irradiance["ghi"],
                dhi=self.solar_basic_model.irradiance["dhi"],
                model="haydavies",
                dni_extra=0,
            ),
            index=self.solar_basic_model.irradiance.index,
        )


class DualAxisSolarModel(SolarModel):
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
                    tracking_dict[index]["surface_tilt"] = row[
                        "apparent_zenith"
                    ]

                else:
                    tracking_dict[index][
                        "surface_tilt"
                    ] = self.axis_model.axis_max_tilt
            else:
                tracking_dict[index]["surface_azimuth"] = 0
        dual_axis_tracking_data = pd.DataFrame.from_dict(
            tracking_dict, orient="index"
        )

        return pd.DataFrame(
            pvlib.irradiance.get_total_irradiance(
                surface_tilt=dual_axis_tracking_data["surface_tilt"],
                surface_azimuth=dual_axis_tracking_data["surface_azimuth"],
                solar_zenith=self.solar_basic_model.irradiance[
                    "apparent_zenith"
                ],
                solar_azimuth=self.solar_basic_model.irradiance["azimuth"],
                dni=self.solar_basic_model.irradiance["dni"],
                ghi=self.solar_basic_model.irradiance["ghi"],
                dhi=self.solar_basic_model.irradiance["dhi"],
                model="haydavies",
                dni_extra=0,
            ),
            index=self.solar_basic_model.irradiance.index,
        )
