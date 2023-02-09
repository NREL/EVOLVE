#third party imports
import json
from pathlib import Path

#local imports
from solar import SolarPV

basepath=Path(__file__).parents[0]

with open(basepath/'SolarPV_input.json') as json_file:
    test_solar_data = json.load(json_file)

irradiance_parameters=test_solar_data['irradiance_parameters']
solar_parameters=test_solar_data['solar_parameters']
inverter_parameters=test_solar_data['inverter_parameters']

test_solar_system=SolarPV(
    solar_parameters,
    inverter_parameters, 
    irradiance_parameters
    )

test_solar_system.plot_results(
    solar_ac_output=True,
    solar_dc_output=True,
    irradiance=True)
