# standard libraries
from datetime import datetime as dt
import logging
from datetime import timedelta
import json
import math

# External libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# internal libraries
#from generate_profile.constants import LOG_FORMAT

LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'

class EnergyStorage:

    def __init__(self, profile, battery_parameters:dict, strategy:dict, resolution:float):

        self.logger = logging.getLogger()
        logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

        self.resolution = resolution

        # if profile != []:
        self.profile = profile
        
        #self.profile['Load']=self.profile['Load'].interpolate(method='polynomial', order=2,limit_direction='both')
        # else:
        #     raise ValueError('Input can not be empty list !!!')

        self.battery_parameters = battery_parameters
        self.charge_discharge_strategy = strategy
        
        # define few variables
        self.results = {
            "battery_kwh" :[],
            "battery_soc" : [],
            "battery_dischargekw" : [],
            "battery_chargekw" : [],
            "battery_selfdischarge":[],
            "modified_profile":[]
        }

        self.current_soc = self.battery_parameters['Initial SOC']
        self.current_kwh = self.battery_parameters['Energy Capacity (KWh)']*self.current_soc
        self.discharge = 0
        self.charge = 0

        time,discharge = [x[0] for x in self.battery_parameters['Self Discharge']],\
            [x[1] for x in self.battery_parameters['Self Discharge']]
        
        if self.battery_parameters['Interpolation'] == 'quadratic':
            self.selfdischargecurve = np.polyfit(time,discharge,2)

        self.time = 0
        self.selfdischarge = 0

        self.simulate()


    def get_result(self):

        return self.results
    
    def get_selfdischarge(self,time):

        if time >= 0:
            return (self.selfdischargecurve[0]**2)*time + self.selfdischargecurve[1]*time \
                            + self.selfdischargecurve[2]
        else:
            return 0
    
    def simulate(self):

        for date in self.profile.index:

            self.load = self.profile['Load'][date]
            if math.isnan(self.load) or self.load==None: 
                self.load = 0
            self.dischargekw = 0
            self.chargekw = 0
            self.date = date

            self.selfdischarge = self.get_selfdischarge(self.time) - \
                                        self.get_selfdischarge(self.time-self.resolution)

            if self.charge_discharge_strategy['method'] == 'sensor':

                self.peak_shaving_sensor_approach()
            
            elif self.charge_discharge_strategy['method'] == 'time':

                self.peak_shaving_time_approach()

            
            self.update_result()
            self.time +=self.resolution

    
    def peak_shaving_sensor_approach(self):

        if self.load > self.charge_discharge_strategy['Discharging load']*max(self.profile['Load'].tolist()):
                
            # discharge kW required 
            if not self.charge_discharge_strategy['Reverse flow']:
                discharge_kw = self.load - self.charge_discharge_strategy['Discharging load'] \
                                            *max(self.profile['Load'].tolist()) 
                if discharge_kw <0: discharge_kw = 0
            else:
                discharge_kw = self.charge_discharge_strategy['Max Discharging Rate (kW)']

            # check if max discharging rate is above required discharging rate
            if discharge_kw > self.charge_discharge_strategy['Max Discharging Rate (kW)']:
                discharge_kw = self.charge_discharge_strategy['Max Discharging Rate (kW)']

            self.discharge_battery(discharge_kw)

        elif self.load <= self.charge_discharge_strategy['Charging load']*max(self.profile['Load'].tolist()):

            charging_kw = self.charge_discharge_strategy['Charging Rate (kW)']

            self.charge_battery(charging_kw)

        else: 
            self.battery_idling()

    
    def peak_shaving_time_approach(self):

        if self.date.hour in self.charge_discharge_strategy['Discharging Hour']:
                
            # discharge kW required 
            if not self.charge_discharge_strategy['Reverse flow']:
                discharge_kw = self.load if self.load >=0 else 0
            else:
                discharge_kw = self.charge_discharge_strategy['Max Discharging Rate (kW)']

            # check if max discharging rate is above required discharging rate
            if discharge_kw > self.charge_discharge_strategy['Max Discharging Rate (kW)']:
                discharge_kw = self.charge_discharge_strategy['Max Discharging Rate (kW)']

            self.discharge_battery(discharge_kw)

        elif self.date.hour in self.charge_discharge_strategy['Charging Hour']:

            charging_kw = self.charge_discharge_strategy['Charging Rate (kW)']

            self.charge_battery(charging_kw)

        else: 
            self.battery_idling()

                
    def discharge_battery(self,discharge_kw):

        # check if the energy is available in the battery or not
        self.usable_kwh = (self.current_kwh - self.battery_parameters['Energy Capacity (KWh)']* \
            self.battery_parameters['MinSOC'])*self.battery_parameters['Discharging Efficiency']
        
        if self.usable_kwh/self.resolution < discharge_kw and self.usable_kwh>0:
            discharge_kw = self.usable_kwh/self.resolution
        elif self.usable_kwh <=0:
            discharge_kw = 0

        self.current_kwh = self.current_kwh - discharge_kw*self.resolution \
                                /self.battery_parameters['Discharging Efficiency'] - \
                                    self.selfdischarge*self.current_kwh/100

        self.current_soc = self.current_kwh/self.battery_parameters['Energy Capacity (KWh)']
        self.load = self.load - discharge_kw
        self.dischargekw = discharge_kw
        
        if discharge_kw >0:
            self.discharge +=1

    def charge_battery(self,charging_kw):

        max_energy = self.battery_parameters['MaxSOC']*self.battery_parameters['Energy Capacity (KWh)']
                
        if (max_energy - self.current_kwh)/self.resolution < charging_kw:
            charging_kw = (max_energy - self.current_kwh)/self.resolution

        if charging_kw <0: charging_kw = 0

        self.current_kwh = self.current_kwh + charging_kw*self.resolution \
            *self.battery_parameters['Charging Efficiency']

        self.current_soc = self.current_kwh/self.battery_parameters['Energy Capacity (KWh)']
        self.load = self.load + charging_kw
        self.chargekw = charging_kw

        if charging_kw>0:
            self.charge += 1
            self.time = 0

        if charging_kw == 0:
            self.current_kwh = self.current_kwh - self.selfdischarge*self.current_kwh/100
            self.current_soc = self.current_kwh/self.battery_parameters['Energy Capacity (KWh)']

    def battery_idling(self):

        self.current_kwh = self.current_kwh - self.selfdischarge*self.current_kwh/100
        self.current_soc = self.current_kwh/self.battery_parameters['Energy Capacity (KWh)']

    def update_result(self):

        self.results['battery_kwh'].append(self.current_kwh)
        self.results['battery_soc'].append(self.current_kwh)
        self.results['battery_dischargekw'].append(self.dischargekw)
        self.results['battery_chargekw'].append(self.chargekw)
        self.results['modified_profile'].append(self.load)
        self.results['battery_selfdischarge'].append(self.selfdischarge*self.current_kwh)


if __name__ == '__main__':

    
    df = pd.read_csv('BYPL-NREL-Effort//src//battery_use_case//test.csv',parse_dates=['TimeStamps'])
    df = df.set_index('TimeStamps')
    with open('BYPL-NREL-Effort//src//battery_use_case//battery.json','r') as json_file:
        battery_dict = json.load(json_file)

    with open('BYPL-NREL-Effort//src//battery_use_case//strategy.json','r') as json_file:
        strategy_dict = json.load(json_file)
    
    a = EnergyStorage(df,battery_dict,strategy_dict,0.5)
    dfresult = pd.DataFrame(a.get_result())
    
    print(df)
    fig,ax = plt.subplots()
    ax.plot(range(len(dfresult)),df['Load'],'-o',label='ProfileWithoutBattery')
    ax.plot(range(len(dfresult)),dfresult['modified_profile'],'-o',label='ProfileWithBattery')

    # ax.plot(range(len(dfresult)),[max(df['Load'])*0.7]*len(dfresult),'--g')
    # ax.plot(range(len(dfresult)),[max(df['Load'])*0.3]*len(dfresult),'--k')

    ax.legend(loc=9)
    ax.set_ylabel('Load (kW)')
    ax1 = ax.twinx()
    ax1.plot(range(len(dfresult)),dfresult['battery_kwh'],'--r',label='BatterykWh')
    ax1.legend(loc=1)
    ax1.set_ylabel('Energy (kWh)')
    plt.show()
    del a

