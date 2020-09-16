'''
Finding time for battery chharging and discharging using load duration curve (goal: reduce peak)
A parametric analysis approach:
    Step 1: Arrange the load profile in descending order (load duration curve)
    Step 2: Find distribution of top 10% load hours 
    Step 3: Perform a parametric analysis and find out which combination provides greater reduction in peak
Similar approach to find out discharging hours.
'''

from datetime import datetime as dt
from datetime import timedelta
import json
import logging
from itertools import combinations
from battery_use_case.battery import EnergyStorage
import pandas as pd
import matplotlib.pyplot as plt
import os

LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'

class ParametricSensor:
    def __init__(self,
                    load_profile=[],
                    start_time= dt(2018,1,1,0,0,0),
                    time_step_min=30,
                    battery_dict = None,
                    strategy_dict = None,
                    step=5
            ):
    
        self.load_profile = load_profile
        self.start_time = start_time
        self.time_step_min = time_step_min
        self.battery_dict =battery_dict
        self.strategy_dict = strategy_dict
        self.step = step

        self.logger = logging.getLogger()
        logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

        if battery_dict == None:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'battery.json'),'r') as file:
                self.battery_dict = json.load(file)
        else:
            self.battery_dict = battery_dict
        
        self.time_list = [self.start_time + i*timedelta(minutes=self.time_step_min) \
                    for i in range(len(self.load_profile))]

    def plot_result(self):

        max_index = self.sweep_result['peak_reduced'].index(max(self.sweep_result['peak_reduced']))

        plt.plot(range(len(self.load_profile)),self.load_profile, label='original')
        
        for id, array in enumerate(self.sweep_result['modified_profile']):
            label_name = str(self.sweep_result['upper_threshold'][id]) + '_' + \
                        str(self.sweep_result['lower_threshold'][id])
            if id == max_index:
                plt.plot(range(len(self.load_profile)),array,'--o', label=label_name)

        plt.legend()
        plt.show()


    def parametric_sweep(self):

        if self.strategy_dict == None:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),\
                'strategy.json'),'r') as file:
                self.strategy_dict = json.load(file)

            self.strategy_dict

        self.sweep_result = {
            'peak_reduced':[],
            'upper_threshold': [],
            'lower_threshold':[],
            'modified_profile':[]
        }

        step_res_hr = self.time_step_min/60

        upper_begin = 1.0 - self.strategy_dict['Max Discharging Rate (kW)']/(max(self.load_profile)*step_res_hr)
        if upper_begin <0.5: upper_begin = 0.5


        for i in range(self.step):

            upper_threshold = 1 - (i+1)*(1-upper_begin)/self.step
            lower_begin = upper_threshold
            
            for j in range(self.step-1):

                lower_threshold = lower_begin - (j+1)*lower_begin/self.step

                self.logger.info(f'Running for scenario {upper_threshold} - {lower_threshold} ')
                
                self.strategy_dict['method'] = 'sensor'
                self.strategy_dict['Charging load'] = lower_threshold
                self.strategy_dict['Discharging load'] = upper_threshold
                

                # Call battery controller
                df = pd.DataFrame({'Load':self.load_profile,'TimeStamps':self.time_list})
                df = df.set_index('TimeStamps')
                battery_instance = EnergyStorage(df, self.battery_dict, self.strategy_dict, self.time_step_min/60)
                result = battery_instance.get_result()
                peak_reduced = max(self.load_profile) - max(result['modified_profile'])
                self.logger.info(f'Peak reduced is {peak_reduced}')

                self.sweep_result['peak_reduced'].append(peak_reduced)
                self.sweep_result['upper_threshold'].append(upper_threshold)
                self.sweep_result['lower_threshold'].append(lower_threshold)
                self.sweep_result['modified_profile'].append(result['modified_profile'])

    def get_best_thresholds(self):
        
        try:
            max_index = self.sweep_result['peak_reduced'].index(max(self.sweep_result['peak_reduced']))

            return {
                'upper_threshold': self.sweep_result['upper_threshold'][max_index],
                'lower_threshold': self.sweep_result['lower_threshold'][max_index],
                'peak_reduced': self.sweep_result['peak_reduced'][max_index]
            }
        except Exception as e:
            
            return 'Failed'


class ParametricTime:

    def __init__(self, 
                load_profile='',
                start_time= dt(2018,1,1,0,0,0),
                time_step_min=30, 
                top_percen=10, 
                num_of_charging_hours=2,
                num_of_discharging_hours=2,
                battery_dict = None,
                strategy_dict = None,
            ):


        self.load_profile = load_profile
        self.start_time = start_time
        self.time_step_min = time_step_min
        self.top_percen = top_percen
        self.num_of_charging_hours = num_of_charging_hours
        self.num_of_discharging_hours = num_of_discharging_hours
        self.strategy_dict = strategy_dict


        self.logger = logging.getLogger()
        logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

        if battery_dict == None:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'battery.json'),'r') as file:
                self.battery_dict = json.load(file)
        else:
            self.battery_dict = battery_dict

        self.analyze_ldc()
        #self.parametric_sweep()
        #self.plot_result()
        #self.logger.info(f'{self.get_best_hours()}')
    
    def analyze_ldc(self):

        self.time_list = [self.start_time + i*timedelta(minutes=self.time_step_min) \
                    for i in range(len(self.load_profile))]
        
        self.sorted_time_list, self.ldc = zip(*sorted(zip(self.time_list,self.load_profile),\
                                            key=lambda x: x[1], reverse=True))

        self.num_of_top_hours = [0]*24 # initialize all load hours to 0
        for index in range(int(self.top_percen*len(self.load_profile)/100)):
            hour = self.sorted_time_list[index].hour
            self.num_of_top_hours[hour-1] +=1
        
        self.peak_hour = self.sorted_time_list[0].hour
        self.logger.info(f'Peak hour is {self.peak_hour}')

        self.num_of_bottom_hours = [0]*24 # initialize all load hours to 0
        for index in range(int(self.top_percen*len(self.load_profile)/100)):
            hour = self.sorted_time_list[len(self.load_profile)-index-1].hour
            self.num_of_bottom_hours[hour-1] +=1

    def top_percen_sensitivity(self):

        top_percen = [0.01,0.1,0.2,0.4,0.8,1.2,1.6,2,2.4,2.8,3.2]
        peak_redcution = []
        for tpc in top_percen:
            self.logger.info(f'Running algorithm for {tpc}% top and bottom load hours ')
            self.top_percen = tpc
            self.analyze_ldc()
            message = self.parametric_sweep()
            if message == 'Success':
                result = self.get_best_hours()
                peak_redcution.append(result['peak_reduced'])
                self.logger.info(f"Peak reduced {result['peak_reduced']}")
            else:
                peak_redcution.append(None)

        plt.plot(top_percen,peak_redcution,'--or')
        plt.xlabel('Top % load hours')
        plt.ylabel('Peak Reduced (kW)')
        plt.show()


    def parametric_sweep(self):

        if self.strategy_dict == None:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'strategy.json'),'r') as file:
                self.strategy_dict = json.load(file)
        
        self.strategy_dict['method'] = 'time'

        top_hours = [i for i in range(24) if self.num_of_top_hours[i]!=0]
        if self.peak_hour not in top_hours: 
            top_hours.append(self.peak_hour)
        self.logger.info(f'Top Hours: {top_hours}')

        bottom_hours = [i for i in range(24) if self.num_of_bottom_hours[i]!=0]
        self.logger.info(f'Bottom Hours: {bottom_hours}')

        bottom_hours = list(set(bottom_hours) - set(top_hours))
        self.logger.info(f'Bottom modified Hours: {bottom_hours}')

        
        if len(bottom_hours) < self.num_of_charging_hours:
            self.logger.warning('Number of bottom hours less than required ....')
            return 'Failed'
            
        self.sweep_result = {
            'peak_reduced':[],
            'charging_hours': [],
            'discharging_hours':[],
            'modified_profile':[],
            'battery_energy':[]
        }

        for thr in combinations(top_hours,self.num_of_discharging_hours):
            if self.peak_hour in thr:
                for bhr in combinations(bottom_hours,self.num_of_charging_hours):
                    self.logger.info(f'Scenario with discharging hours {thr} and charging hours {bhr}')
                    self.strategy_dict['Charging Hour'] = list(bhr)
                    self.strategy_dict['Discharging Hour'] = list(thr)

                    # Call battery controller
                    df = pd.DataFrame({'Load':self.load_profile,'TimeStamps':self.time_list})
                    df = df.set_index('TimeStamps')
                    battery_instance = EnergyStorage(df, self.battery_dict, self.strategy_dict, self.time_step_min/60)
                    result = battery_instance.get_result()
                    peak_reduced = max(self.load_profile) - max(result['modified_profile'])
                    #self.logger.info(f'Peak reduced is {peak_reduced}')

                    self.sweep_result['peak_reduced'].append(peak_reduced)
                    self.sweep_result['charging_hours'].append(list(bhr))
                    self.sweep_result['discharging_hours'].append(list(thr))
                    self.sweep_result['modified_profile'].append(result['modified_profile'])
                    self.sweep_result['battery_energy'].append(result['battery_kwh'])
        return 'Success'

    def get_best_hours(self):
        
        try:
            self.max_index = self.sweep_result['peak_reduced'].index(max(self.sweep_result['peak_reduced']))

            return {
                'charging_hours': self.sweep_result['charging_hours'][self.max_index],
                'discharging_hours': self.sweep_result['discharging_hours'][self.max_index],
                'peak_reduced': self.sweep_result['peak_reduced'][self.max_index]
            }
        except Exception as err:
            return 'Failed'
    
    def plot_result(self):

        max_index = self.sweep_result['peak_reduced'].index(max(self.sweep_result['peak_reduced']))

        fig,ax = plt.subplots()
        ax.plot(range(len(self.load_profile)),self.load_profile, label='original')
        
        for id, array in enumerate(self.sweep_result['modified_profile']):
            label_name = ''.join(str(x) for x in self.sweep_result['charging_hours'][id]) + '_'\
                            + ''.join(str(x) for x in self.sweep_result['discharging_hours'][id])
            if id == max_index:
                ax.plot(range(len(self.load_profile)),array,'--', label=label_name)

        ax.legend()
        ax.set_ylabel('load (kW)')
        ax1 = ax.twinx()
        ax1.plot(range(len(self.load_profile)),self.sweep_result['battery_energy'][max_index],'--ro', label='battery_energy')
        ax.set_ylabel('Battery energy (kWh)')
        ax1.legend()
        plt.show()

if __name__ == '__main__':

    load_profile = pd.read_csv(r'C:\Users\KDUWADI\Box\BRPL Demand Side Management\Data\brpl_data\brpl_transformerdata.csv')
    one_day_profile = load_profile['PeakLoad'].tolist()[:48*7]

    instance = ParametricTime(load_profile=one_day_profile)
    #instance.top_percen_sensitivity()
    instance.analyze_ldc()
    instance.parametric_sweep()
    instance.get_best_hours()
    print(instance.get_best_hours())
    instance.plot_result()


    

    # instance = ParametricSensor(load_profile=one_day_profile)
    # instance.parametric_sweep()
    # instance.plot_result()
    # print(instance.get_best_thresholds())


