#third-party imports
from cerberus import Validator
import pandas as pd

#local imports
from schemas import (
    IRRADIANCE_DATAFRAME_SCHEMA,
    IRRADIANCE_INPUT_SCHEMA,
    INVERTER_PARAMETER_SCHEME,
    SOLAR_PARAMETERS_INPUT_SCHEMA
)
from exceptions import (
    IrradianceDataException,
    SolarParametersException,
    InverterParametersException
)

def irradiance_dataframe_validation(irradiance_input_dict):
    v=Validator(IRRADIANCE_INPUT_SCHEMA, allow_unknown=False)
    v.validate(irradiance_input_dict)
    if not v.validate(irradiance_input_dict):
        raise IrradianceDataException(v.errors)
    if irradiance_input_dict['irradiance_file_path']!='':
        irradiance_dataframe=pd.read_csv(irradiance_input_dict['irradiance_file_path']).fillna(value=0)
        irradiance_dict=irradiance_dataframe.to_dict(orient='index')
        v=Validator(IRRADIANCE_DATAFRAME_SCHEMA, allow_unknown=False)
        for row in irradiance_dict.values():
            if not v.validate(row):
                raise IrradianceDataException(v.errors)

def solar_parameters_validation(solar_parameters: dict):
    v=Validator(SOLAR_PARAMETERS_INPUT_SCHEMA, allow_unknown=False)
    if not v.validate(solar_parameters):
        raise SolarParametersException(v.errors)

def inverter_parameters_validation(inverter_parameters: dict):
    v=Validator(INVERTER_PARAMETER_SCHEME, allow_unknown=False)
    if not v.validate(inverter_parameters):
        raise InverterParametersException(v.errors)

