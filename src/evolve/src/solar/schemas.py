SOLAR_PARAMETERS_INPUT_SCHEMA={
    'pv_location':{
        'required':True,
        'type':['float','list']
        },
    'kva':{
        'required':True,
        'type':'float',
        'min':0.0
        },
    'tracking_type':{
        'required':True,
        'type':'string',
        'allowed':['fixed','single_axis','dual_axis']
        },
    'fixed_axis_surface_tilt':{
        'required': False,
        'type':'float',
        'min':0.0,
        'max':90.0
        },
    'fixed_axis_surface_azimuth':{
        'required': False,
        'type':'float',
        'min':0.0,
        'max':360.0
        },
    'single_axis_axis_tilt':{
        'required': False,
        'type':'float',
        'min':0.0,
        'max':90.0
        },
    'single_axis_axis_azimuth':{
        'required': False,
        'type':'float',
        'min':0.0,
        'max':360.0
        },
    'single_axis_max_tilt':{
        'required': False,
        'type':'float',
        'min':0.0,
        'max':90.0,
        'default':85
        },
    'dual_axis_max_tilt':{
        'required': False,
        'type':'float',
        'min':0.0,
        'max':90.0,
        'default':85
        }
}

INVERTER_PARAMETER_SCHEME={
    'inverter_sizing_ratio':{
        'required':True,
        'min':0,
        'default':1.2
        },
    'inverter_temp_coeff':{
        'required':True,
        'default': 0.003
        },
}

IRRADIANCE_INPUT_SCHEMA={
    'irradiance_file_path':{
        'required': False,
        'type':'string'
        },
    'start':{
        'required':True,
        'type':'string'
        },
    'end':{
        'required':True, 
        'type':'string'
        },
    'resolution_mins':{
        'required':True, 
        'type':'integer'
        }
}

IRRADIANCE_DATAFRAME_SCHEMA={
    'Date':{
        'required':True,
        'type':'string'
        },
    'Time':{
        'required':True,
        'type':'string'
        },
    'ghi':{
        'required':True,
        'type': 'float'
        },
    'dni':{
        'required':True,
        'type': 'float'
        },
    'dhi':{
        'required':True,
        'type': 'float'
        },
    'temp':{
        'required': False,
        'type': 'float'
        }
}


