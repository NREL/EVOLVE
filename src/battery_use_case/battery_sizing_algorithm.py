"""
Created on Tue Nov 13 16:43:48 2018
@author: rbryce
"""
# standard libraries
import math
import numpy as np
import pandas as pd


LOADTHRESHOLD_PERCENTAGE = 70
BATTERY_HOURS = 4

class BatterySizing:

    def __init__(self, loadprofile: list, dt_rating, resolution: float = 0.5):

        self.loadprofile = loadprofile
        self.dtrating = dt_rating
        self.resolution = resolution
        self.threshold_load = self.dtrating * LOADTHRESHOLD_PERCENTAGE/100
        self.compute_size()

    def compute_size(self):

        self.durationcounter, self.energycounter, self.peakcounter = [], [], []

        start_counter_flag = False
        if len(self.loadprofile)>0:

            for id, load in enumerate(self.loadprofile):

                if not start_counter_flag and load > self.threshold_load:
                    start_index = id
                    energy = load
                    start_counter_flag = True

                else:

                    if start_counter_flag and load > self.threshold_load:
                        energy += load
                    
                    if start_counter_flag and load < self.threshold_load:

                        start_counter_flag = False
                        energy = energy * self.resolution
                        
                        self.energycounter.append(energy)
                        self.durationcounter.append((id-start_index)*self.resolution)
                        self.peakcounter.append(max(self.loadprofile[start_index:id]))


            
            self.battery_power = [el - self.threshold_load for el in self.peakcounter]
            self.battery_energy = [x[0]- x[1]*self.threshold_load for x in zip(self.energycounter, self.durationcounter)]
            
            try:
                self.battery_capacity = np.percentile(self.battery_power, LOADTHRESHOLD_PERCENTAGE)
                self.battery_energy = np.percentile(self.battery_energy, LOADTHRESHOLD_PERCENTAGE)
            except Exception as err:
                self.battery_capacity = 0
                self.battery_energy = 0
        
        else:
            self.battery_energy = 0
            self.battery_power = 0

    def return_size(self):

        if self.battery_energy == 0 or self.battery_capacity ==0:
            if self.battery_energy/self.battery_capacity> BATTERY_HOURS:
                self.battery_capacity = self.battery_energy/BATTERY_HOURS       
            else:
                self.battery_energy=self.battery_capacity*BATTERY_HOURS

        return {
            'battery_power_kW': self.battery_capacity,
            'battery_energy_kWh': self.battery_energy
        }


if __name__ == '__main__':

    data_path  = 'C:/Users/KDUWADI/Box/BYPL-USAID research/Data/extracted_profile/TG-LGR017A-1-2016_dataframe.csv'
    #data_path = 'C:/Users/KDUWADI/Box/BYPL-USAID research/Data/extracted_profile/TG-LGR017A-1-2016_dataframe_test.csv'
    trans_data = pd.read_csv(data_path)['TransformerPower'].tolist()
    instance = BatterySizing(trans_data, 200)
    print(instance.return_size())