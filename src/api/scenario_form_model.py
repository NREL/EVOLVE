import datetime
from typing import List, Optional

from pydantic import BaseModel, validator, conint, confloat

VALID_DATA_FILLING_STRATEGIES = ['interpolation', 'staircase']
VALID_TECHNOLOGIES = ['solar', 'ev', 'energy_storage']
VALID_SOLAR_INSTALLATION_TYPE = ['fixed', 'single_axis', 'dual_axis']
VALID_HOURS = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM',
    '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM',
    '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM',
    '8 PM', '9 PM', '10 PM', '11 PM']
VALID_ENERGY_STORAGE_CD_STRATEGY = ['time', 'price', 'self_consumption', 'peak_shaving']

class BasicFormData(BaseModel):
    dataFillingStrategy: Optional[str]
    endDate: datetime.date
    startDate: datetime.date 
    loadProfile: int 
    resolution: conint(ge=0)
    scenarioName: str 
    technologies: List[str]

    @validator('dataFillingStrategy')
    def must_be_valid_strategy(cls, v):
        if v is not None:
            if v not in VALID_DATA_FILLING_STRATEGIES:
                raise ValueError(f'Data filling strategy must be one \
                of {VALID_DATA_FILLING_STRATEGIES} but given {v}')
        return v

    @validator('technologies')
    def must_be_valid_technology(cls, v):
        for tech in v:
            if tech not in VALID_TECHNOLOGIES:
                raise ValueError(f'Technology must be one \
                of {VALID_TECHNOLOGIES} but given {v}')
        return v

    @validator('startDate')
    def start_date_must_be_smaller(cls,v, values, **kwargs):
        if v > values['endDate']:
            raise ValueError(f"Start date {v} can not be greater than \
                end date {values['endDate']}")

        return v

class SolarFormData(BaseModel):
    dcacRatio: confloat(ge=0.2, le=2.0)
    id: str
    irradianceData: Optional[int]
    name: str 
    panelAzimuth: confloat(ge=0, le=360)
    panelTilt: confloat(ge=-90, le=90)
    solarCapacity: confloat(gt=0) 
    solarInstallationStrategy: str 

    @validator('solarInstallationStrategy')
    def must_be_valid_strategy(cls, v):
        if v not in VALID_SOLAR_INSTALLATION_TYPE:
            raise ValueError(f'Solar installation type must be one \
            of {VALID_SOLAR_INSTALLATION_TYPE} but given {v}')
        return v

class EVFormData(BaseModel):
    numberOfEV: conint(gt=0)
    pctResEV: confloat(gt=0)
    id: str
    name: str 

class ESFormData(BaseModel):
    esStrategy: str 
    chargingHours: Optional[List[str]]
    disChargingHours: Optional[List[str]]
    chargingPowerThreshold: Optional[confloat(gt=0, le=100)] 
    dischargingPowerThreshold: Optional[confloat(gt=0, le=100)] 
    chargingPrice: Optional[float] 
    disChargingPrice: Optional[float]
    esEnergyCapacity: confloat(gt=0) 
    esPowerCapacity: confloat(gt=0) 
    id: str 
    name: str
    priceProfile: Optional[int]

    @validator('esStrategy')
    def must_be_valid_strategy(cls, v):
        if v not in VALID_ENERGY_STORAGE_CD_STRATEGY:
            raise ValueError(f'Energy storage charging discharging strategy must be one \
            of {VALID_ENERGY_STORAGE_CD_STRATEGY} but given {v}')
        return v

    @validator('disChargingHours')
    def must_be_different_than_charging_hours(cls,v, values, **kwargs):
        if values['esStrategy'] == 'time':
            if v is None or values['chargingHours'] is None:
                raise ValueError('Both charging and discharging hours must be specified\
                if charging discharging strategy is time based.')

            for hours in [v, values['chargingHours']]:
                for item in hours:
                    if item not in VALID_HOURS:
                        raise ValueError(f'Hour must be one of \
                        of {VALID_HOURS} but given {v}')

            if set(v) - set(values['chargingHours']) != set(v):
                raise ValueError('Charging hours and discharging hours should not have \
                duplicate values.')
        return v

    @validator('dischargingPowerThreshold')
    def charging_discharging_power_must_be_specified(cls, v, values, **kwargs):
        if values['esStrategy'] == 'peak_shaving':
            if v is None or values['chargingPowerThreshold'] is None:
                raise ValueError('Both charging power threshold and discharging power \
                    must be specified if strategy is peak shaving')
        
        return v

    @validator('disChargingPrice')
    def charging_discharging_price_must_be_specified(cls, v, values, **kwargs):
        if values['esStrategy'] == 'price':
            if v is None or values['chargingPrice'] is None:
                raise ValueError('Both charging price threshold and discharging price \
                    theshold must be specified if strategy is price.')
        
        return v

class ScenarioData(BaseModel):
    basic: BasicFormData
    solar: List[SolarFormData]
    ev: List[EVFormData]
    energy_storage: List[ESFormData]

class CloneScenarioInputModel(BaseModel):
    name: str


