
DEFAULT_CONFIGURATION = {
    "project_path": "",
    "dtpower_file": "SlotWiseEnergy.csv",
    "solar_irradiance_file": "SolarData.csv",
    "customer_energy": '',
    "year_list": [2016,2017,2018,2019,2020],
    "export_folder": ""
}


VALID_SETTINGS = {
    "project_path": {'type':str},
    "dtpower_file": {'type':str},
    "solar_irradiance_file": {'type':str},
    "customer_energy": {'type': str},
    "year_list": {'type':list},
    "export_folder": {'type':str}
}