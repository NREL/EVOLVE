# Standard imports
from datetime import datetime as dt
from datetime import timedelta
import json
import math
import numpy as np
import calendar
import logging

# Thirs-party imports
import pandas as pd

# Internal Imports
from battery_use_case.battery import EnergyStorage
from battery_use_case.parametric_threshold import ParametricTime, ParametricSensor
from battery_use_case.battery_sizing_algorithm import BatterySizing
from battery_use_case.optimized_battery_sizing import BTMsizing
from ev_scenarios.analyze_ev import ev_profile
from constants import TIME_RESOLUTION, FACTOR

logger = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

class APIData:
    """ Class for managing API data """

    def __init__(self, config_dict, data_handler):

        self.config_dict = config_dict
        print(self.config_dict)
        self.data_handler = data_handler

        self.dashboard_data = {
            'date': {
                    'format': 'month',
                    'data':['2018-1-1 1:15:0','2018-1-1 5:15:0','2018-3-1 1:15:0','2018-4-1 1:15:0','2018-12-1 1:15:0']
                },
            'xarray': {
                'data': [1,2,3,4,5]
            },
            'sweepmessage':'',
            'autocapacitymessage': '',
            'optimizedbatterymessage': '',
            'number_by_group' : [20,20,20],
            'dt_metric' : {'peakpower':0,'energy':0,'ramp':0,'avg2peak':0},
            'dt_metric_new': {'peak_r':'50%','energy_r': '50%','ramp': '50%','avg2peak': '0.2'},
            'dt_metric_new_isneg': {'peak_r': True,'energy_r': True,'ramp': True,'avg2peak': True},
            'dt_profile': [
                # {'key':'Net load', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Base load', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'New load', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'}
            ],
            'dt_ldc': [
                # {'key':'Net LDC', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Base LDC', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'New LDC', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'}
            ],
            'solar_metric': {'energy': 0, 'power_at_peak':0, 'peak_power': 0},
            'ev_metric': {'energy': 0, 'power_at_peak':0, 'peak_power': 0},
            'battery_metric': {'c_energy': 0, 'd_energy':0, 'cd_cycle': 0},
            'solar_output': [{'key':'solar_output', 'data': [0,0,0,0,0],'color': '#dc3545'}],
            'battery_output': [
                {'key':'storage_energy', 'data': [0,0,0,0,0],'color': '#007bff'},
                {'key':'charging_power', 'data': [0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'discharging_power', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'}
            ],
            'ev_output': [{'key':'ev_output', 'data': [0,0,0,0,0],'color': '#17a2b8'}]
        }


        if self.config_dict['dtorfeeder'] == 'DT':
            self.dashboard_data['number_by_group'] = self.data_handler.get_customernumber_bygroup(
            self.config_dict['transformer'],'DT')
        else:
            self.dashboard_data['number_by_group'] = self.data_handler.get_customernumber_bygroup(
            self.config_dict['feeder'],'Feeder')
            

        # Update date
        self.change_date() 
        self.get_transformer_loading()
        self.get_battery_profile()
        self.update_rest()
    
    def update_rest(self):

        peak_reduced = 100 - int(max(self.latest_profile)*100/max(self.trans_base_load))

        energy_reduced = 100 - int(np.nansum(self.latest_profile)*100/np.nansum(self.trans_base_load))

        base_ramp_rate = max([abs(self.trans_base_load[i+1]-self.trans_base_load[i]) for i \
                in range(len(self.trans_base_load)-1)])

        new_ramp_rate = max([abs(self.latest_profile[i+1]-self.latest_profile[i]) for i \
                in range(len(self.latest_profile)-1)])
        ramp_reduced = 100 - int(new_ramp_rate*100/base_ramp_rate)

        base_avg2peak = np.nansum(self.trans_base_load)/(len(self.trans_base_load)\
                *max(self.trans_base_load))
        
        new_avg2peak = np.nansum(self.latest_profile)/(len(self.latest_profile)\
                *max(self.latest_profile))
        
        avg2peakreduced = 100 -  int(new_avg2peak*100/base_avg2peak)

        self.dashboard_data['dt_metric_new'] = {
            'peak_r': str(peak_reduced)+'%',
            'energy_r':  str(energy_reduced)+'%',
            'ramp': str(ramp_reduced)+'%',
            'avg2peak': str(avg2peakreduced)+'%'
        }

        self.dashboard_data['dt_metric_new_isneg'] = {
            'peak_r': False if peak_reduced <0 else True,
            'energy_r':  False if energy_reduced <0 else True,
            'ramp': False if ramp_reduced <0 else True,
            'avg2peak': False if avg2peakreduced <0 else True
        }



    def get_battery_profile(self):

        # Create a dataframe
        df = pd.DataFrame({
            'TimeStamps': self.timestamps,
            'Load': [el if not math.isnan(el) else 0 for el in self.trans_new_load]
        })
        df = df.set_index('TimeStamps')
        
        battery_dict = {
            "Rated Capacity (kW)": float(self.config_dict['batterypower']),
            "Energy Capacity (KWh)": float(self.config_dict['batteryenergy']),
            "Initial SOC": 1,
            "Charging Efficiency": 0.95,
            "Discharging Efficiency": 0.95,
            "Self Discharge": [[0,0],[24,5],[720,7]],
            "Interpolation": "quadratic",
            "Cycle Life": 500,
            "MinSOC": 0.1,
            "MaxSOC": 0.95
        }

        strategy_dict = {
            "Charging Hour" : [10,11,12],
            "Discharging Hour" : [3,4,5],
            "Charging load" : 0.3,
            "Discharging load" : 0.7,
            "Charging Rate (kW)" : 20,
            "Max Discharging Rate (kW)" : 30,
            "Reverse flow": False,
            "method":"time"
        }

        if self.config_dict['batterystrategy'] == 'Time Based':
            strategy_dict['method'] = 'time'
            strategy_dict['Charging Hour'] = [int(el) for el in self.config_dict['chargethreshold'].split(',')]
            strategy_dict['Discharging Hour'] = [int(el) for el in self.config_dict['dischargethreshold'].split(',')]
        
        if self.config_dict['batterystrategy'] == 'Power Based':
            
            strategy_dict['method'] = 'sensor'
            strategy_dict["Charging load"] = float(self.config_dict['chargethreshold'])
            strategy_dict["Discharging load"] = float(self.config_dict['dischargethreshold'])


        # change battery capacity if auto is selected
        if self.config_dict['autocapacity'] and not self.config_dict['optimizecapacity']:
        
            sizing_instance = BatterySizing(df['Load'].tolist(), self.data_handler.trans_capacity[self.config_dict['transformer']], resolution=1/FACTOR)
            #print(f"Capacity: {self.data_handler.trans_capacity[self.config_dict['transformer']]}, peak load: {max(self.trans_base_load)}")
            size_dict = sizing_instance.return_size()
            battery_dict['Rated Capacity (kW)'] = size_dict['battery_power_kW']
            battery_dict['Energy Capacity (KWh)'] = size_dict['battery_energy_kWh']
            self.dashboard_data['autocapacitymessage'] = f"Battery power: {round(size_dict['battery_power_kW'],2)}, Battery Energy: {round(size_dict['battery_energy_kWh'],2)}, DT capacity : {self.data_handler.trans_capacity[self.config_dict['transformer']]}"


        if self.config_dict['batterystrategy'] != 'Price Based' and battery_dict["Rated Capacity (kW)"] >0 \
                        and battery_dict["Energy Capacity (KWh)"] > 0 and not self.config_dict['optimizecapacity']:

            strategy_dict['Charging Rate (kW)'] = float(self.config_dict['kwchargerate'])*float(battery_dict['Rated Capacity (kW)'])
            strategy_dict['Max Discharging Rate (kW)'] = float(self.config_dict['kwdischargerate'])*float(battery_dict['Rated Capacity (kW)'])

            if strategy_dict['Charging Rate (kW)']>float(battery_dict['Rated Capacity (kW)']):
                strategy_dict['Charging Rate (kW)'] = float(battery_dict['Rated Capacity (kW)'])
            if strategy_dict['Max Discharging Rate (kW)']>float(battery_dict['Rated Capacity (kW)']):
                strategy_dict['Max Discharging Rate (kW)']=float(battery_dict['Rated Capacity (kW)'])
            

            if self.config_dict['batterystrategy'] == 'Time Based' and self.config_dict['sweep']:

                battery_hours = int(battery_dict['Energy Capacity (KWh)']/battery_dict['Rated Capacity (kW)'])
                if battery_hours==0: battery_hours = 1 
                charging_hours = int(battery_dict['Rated Capacity (kW)']/strategy_dict['Charging Rate (kW)'])*battery_hours
                discharging_hours = int(battery_dict['Rated Capacity (kW)']/strategy_dict['Max Discharging Rate (kW)'])*battery_hours
                

                for top_percen in [30,35,40]:

                    param_instance = ParametricTime(
                        load_profile=df['Load'].tolist(),
                        start_time = self.start_date,
                        time_step_min = TIME_RESOLUTION,
                        top_percen=top_percen,
                        num_of_charging_hours=charging_hours,
                        num_of_discharging_hours=discharging_hours,
                        battery_dict=battery_dict,
                        strategy_dict=strategy_dict
                        )

                    messgae = param_instance.parametric_sweep()
                    if messgae == 'Success':
                        result = param_instance.get_best_hours()
                        if result != 'Failed':
                            strategy_dict['Charging Hour'] = result['charging_hours']
                            strategy_dict['Discharging Hour'] = result['discharging_hours']
                            self.dashboard_data['sweepmessage']= 'Charging hours: ' + \
                                ','.join(str(x) for x in result['charging_hours']) + ' Discharging hours: ' +\
                                ','.join(str(x) for x in result['discharging_hours'])
                        break

            if self.config_dict['batterystrategy'] == 'Power Based' and self.config_dict['sweep']:

                param_instance = ParametricSensor(
                    load_profile=df['Load'].tolist(),
                    start_time = self.start_date,
                    time_step_min = TIME_RESOLUTION,
                    battery_dict=battery_dict,
                    strategy_dict=strategy_dict
                    )

                param_instance.parametric_sweep()
                result = param_instance.get_best_thresholds()
                
                if result != 'Failed':
                    strategy_dict['Charging load'] = result['lower_threshold']
                    strategy_dict['DisCharging load'] = result['upper_threshold']
                    self.dashboard_data['sweepmessage']= 'Charging threshold: ' + \
                        str(round(result['lower_threshold'],2)) + ', Discharging threshold: ' \
                            + str(round(result['upper_threshold'],2))


            storage_instance = EnergyStorage(df, battery_dict, strategy_dict, 1/FACTOR)
            battery_result = storage_instance.get_result()

            self.latest_profile = battery_result['modified_profile']

            self.dashboard_data['battery_output'][0]['data'] = battery_result['battery_kwh']
            self.dashboard_data['battery_output'][1]['data'] = battery_result['battery_chargekw']
            self.dashboard_data['battery_output'][2]['data'] = battery_result['battery_dischargekw']

            

            self.dashboard_data['battery_metric'] = {
                'c_energy': int(np.nansum(battery_result['battery_chargekw'])*FACTOR/1000) if \
                            int(np.nansum(battery_result['battery_chargekw'])*FACTOR/1000) !=0 else \
                                round(np.nansum(battery_result['battery_chargekw'])*FACTOR/1000,3),
                'd_energy': int(np.nansum(battery_result['battery_dischargekw'])*FACTOR/1000) if \
                            int(np.nansum(battery_result['battery_dischargekw'])*FACTOR/1000) !=0 else \
                                round(np.nansum(battery_result['battery_dischargekw'])*FACTOR/1000,3),
                'cd_cycle': self.count_cycle(battery_result['battery_chargekw'])
            }

        else:
            self.latest_profile = self.trans_new_load

        if self.config_dict['optimizecapacity']:

            self.pv_generation = [el if not math.isnan(el) else 0 for el in self.pv_generation]
            instance = BTMsizing(df['Load'].tolist(),self.pv_generation,1/FACTOR, 20)
            battery_profile = instance.get_battery_profile()
            netloadprofile = instance.get_netloadprofile()
            battery_energy_profile = instance.get_battery_energy_profile()
            charging_profile = [-el if el <0 else 0 for el in battery_profile]
            discharging_profile = [el if el >0 else 0 for el in battery_profile]

            self.dashboard_data['battery_output'][0]['data'] = battery_energy_profile
            self.dashboard_data['battery_output'][1]['data'] = charging_profile
            self.dashboard_data['battery_output'][2]['data'] = discharging_profile
            b_power, b_energy = instance.optimal_size

            self.dashboard_data['optimizedbatterymessage'] = f"Battery power: {round(b_power,2)}, Battery Energy: {round(b_energy,2)}"

            self.latest_profile = netloadprofile

            self.dashboard_data['battery_metric'] = {
                'c_energy': int(sum(charging_profile)*FACTOR/1000) if int(sum(charging_profile)*FACTOR/1000) !=0 else \
                                round(sum(charging_profile)*FACTOR/1000,3),
                'd_energy': int(sum(discharging_profile)*FACTOR/1000) if int(sum(discharging_profile)*FACTOR/1000) !=0 else \
                                round(sum(discharging_profile)*FACTOR/1000,3),
                'cd_cycle': self.count_cycle(charging_profile)
            }
        
        
        self.dashboard_data['dt_profile'][1]['data'] = [el if not math.isnan(el) else None for el in self.latest_profile]
        self.dashboard_data['dt_ldc'][1]['data'] = sorted(self.dashboard_data['dt_profile'][1]['data'],reverse=True)
        max_index = self.latest_profile.index(max(self.latest_profile))
        self.dashboard_data['solar_metric']['power_at_peak'] = int(self.pv_generation[max_index])
        if int(self.config_dict['evnumber']) >=0:
            self.dashboard_data['ev_metric']['power_at_peak'] = int(self.ev_profile[max_index])
        
    def count_cycle(self,battery_array):
        cycle_count,flag = 0,0
        for el in battery_array:
            if el!=0:
                if flag == 0:
                    cycle_count +=1
                flag=1
            else:
                flag = 0

        return cycle_count
        
    def get_transformer_loading(self):

        
        net_load, net_load_highres = self.data_handler.analyze_dt(
                                            self.config_dict['transformer'],
                                            self.today.year,
                                            self.config_dict['mode'],
                                            self.today) if self.config_dict['dtorfeeder'] == 'DT' else \
                                    self.data_handler.analyze_feeder(
                                            self.config_dict['feeder'],
                                            self.today.year,
                                            self.config_dict['mode'],
                                            self.today)

        baseload_highres =  net_load_highres
        
        
        #self.trans_net_load = [el*2 for el in net_load_highres]
        self.trans_base_load = [el for el in baseload_highres]

        self.pvmultiplers = self.data_handler.return_solar_multiplier(
                                            self.today,
                                            self.config_dict['mode'])
        
        if float(self.config_dict['pvcapacity']) <0:
            self.config_dict['pvcapacity'] = 0
        
        self.pv_generation = [el*float(self.config_dict['pvcapacity']) for el in self.pvmultiplers]
        # ev profile 
        if self.config_dict['mode'] == 'Daily':
            num_days = 1
        elif self.config_dict['mode'] == 'Weekly':
            num_days = 7
        elif self.config_dict['mode'] == 'Yearly':
            num_days = 365

        if int(self.config_dict['evnumber']) <=0:
            self.ev_profile = [0]*len(self.pv_generation)
        else:
            if int(self.config_dict['evnumber']) == 1:  self.config_dict['evnumber'] = 2
            try:
                self.ev_profile = ev_profile(number_of_evs=int(self.config_dict['evnumber']),
                             adoption_percentage=0, res_percentage = self.config_dict['respercentage'],number_of_days=num_days)
            except Exception as e:
                logger.error('Error', str(e))
                self.ev_profile = [0]*len(self.pv_generation)
                
                
        self.trans_new_load = [x[0]-x[1]+x[2] for x in zip(self.trans_base_load, self.pv_generation, self.ev_profile)]

        # Update data
        self.dashboard_data['ev_output'][0]['data'] = [el if not math.isnan(el) else 0 for el in self.ev_profile]
        #self.dashboard_data['dt_profile'][0]['data'] = [el if not math.isnan(el) else 0 for el in self.trans_net_load]
        self.dashboard_data['dt_profile'][0]['data'] = [el if not math.isnan(el) else 0 for el in self.trans_base_load]

        #self.dashboard_data['dt_ldc'][0]['data'] = sorted(self.dashboard_data['dt_profile'][0]['data'],reverse=True)
        self.dashboard_data['dt_ldc'][0]['data'] = sorted(self.dashboard_data['dt_profile'][0]['data'],reverse=True)
        len_of_data = len(self.dashboard_data['dt_ldc'][0]['data'])
        self.dashboard_data['xarray']['data'] =  list(range(len_of_data))

        self.dashboard_data['dt_metric'] = {
            'peakpower': round(max(self.trans_base_load),1),
            'energy': round(np.nansum(self.trans_base_load)/1000,1),
            'ramp': round(max([abs(self.trans_base_load[i+1]-self.trans_base_load[i]) for i \
                in range(len(self.trans_base_load)-1)]),1),
            'avg2peak': round(np.nansum(self.trans_base_load)/(len(self.trans_base_load)\
                *max(self.trans_base_load)),1)
        }

        self.dashboard_data['solar_output'][0]['data'] = self.pv_generation
        self.dashboard_data['solar_metric']['energy'] = int(np.nansum(self.pv_generation)*FACTOR/1000) if \
               int(np.nansum(self.pv_generation)*FACTOR/1000) !=0 else round(np.nansum(self.pv_generation)*FACTOR/1000,3)
        self.dashboard_data['solar_metric']['peak_power'] = int(max(self.pv_generation))
        
        if not int(self.config_dict['evnumber']) <=0:
            logger.info(self.ev_profile)
            self.dashboard_data['ev_metric']['energy'] = round(sum(self.ev_profile)/1000,2)
            self.dashboard_data['ev_metric']['peak_power'] = int(max(self.ev_profile))

    def change_date(self):
        
        self.today = dt.strptime(self.config_dict['day'],'%Y-%m-%d')
        if self.config_dict['mode'] == 'Daily':
            self.start_date = dt(self.today.year, self.today.month, self.today.day, 0,0,0)
            self.dashboard_data['date']['format'] = 'hour'
            self.timestamps = [dt(self.today.year, self.today.month, self.today.day, 0,0,0) \
                        + timedelta(minutes=TIME_RESOLUTION)*i for i in range(FACTOR*24)]
            
        elif self.config_dict['mode'] == 'Yearly':
            self.start_date = dt(self.today.year, 1, 1, 0,0,0)
            self.dashboard_data['date']['format'] = 'month'
            num_of_days = 366 if calendar.isleap(self.today.year) else 365
            self.timestamps = [dt(self.today.year, 1,1, 0,0,0) \
                        + timedelta(minutes=TIME_RESOLUTION)*i for i in range(FACTOR*24*num_of_days)]

        elif self.config_dict['mode'] == 'Weekly':
            self.start_date = dt(self.today.year, self.today.month, self.today.day, 0,0,0)
            self.dashboard_data['date']['format'] = 'day'
            self.timestamps = [dt(self.today.year, self.today.month, self.today.day, 0,0,0) \
                        + timedelta(minutes=TIME_RESOLUTION)*i for i in range(FACTOR*24*7)]
        
        self.dashboard_data['date']['data'] = [date.strftime('%Y-%m-%d %H:%M:%S') \
           for date in self.timestamps]
             

    def get_data(self):

        return self.dashboard_data
