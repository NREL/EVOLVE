
# standard libraries
import numpy as np
from scipy.optimize import linprog
import pandas as pd
import matplotlib.pyplot as plt
import math

ENERGY_PRICE = 2.00
ENERGY2POWERRATIO = 4

class BTMsizing:

    def __init__(self, load_data: list, pv_data: list, resolution, iterations: int):

        self.load_data = load_data
        self.pv_data = pv_data
        self.resolution = resolution
        self.iterations = iterations
        self.timesteps = len(self.load_data)
        self.compute_size()
        
        
                
    def compute_size(self):
        
        self.battery_profile, self.netloadprofile = [], []
        
        for n in range(self.iterations):

            battery_energy_capacity = n**2
            initial_battery_energy = battery_energy_capacity/2
            final_battery_energy = battery_energy_capacity/2
            
            basis_load = np.array(self.load_data) - np.array(self.pv_data)
            basis_load = basis_load.reshape(len(self.load_data), 1)

            """ Defining objective function """
            
            obj_coefficient_array=np.append(ENERGY_PRICE*np.ones((1,self.timesteps),float),\
                -1*ENERGY_PRICE*np.ones((1,self.timesteps),float),axis=1)

            """ Building inequality constraints """
            

            A_ub, b_ub = [], []
            #build charging subset of inequality matrix
            charging_Aub_subset=np.zeros((self.timesteps,2*self.timesteps),float)
            for j in range(self.timesteps):
                for i in range(self.timesteps):
                    if i >= j:
                        charging_Aub_subset[i,j]=1
                   
            for j in range(self.timesteps):
                for i in range(self.timesteps):
                    if i > j:
                        charging_Aub_subset[i,j+self.timesteps]=-1
            
            charging_bub_subset=(battery_energy_capacity-initial_battery_energy)*np.ones((self.timesteps,1),float)

            #build dischargin subset of inequality matrix
            discharging_Aub_subset=np.zeros((self.timesteps,2*self.timesteps),float)
            for j in range(self.timesteps):
                for i in range(self.timesteps):
                    if i >= j:
                        discharging_Aub_subset[i,j+self.timesteps]=1
            for j in range(self.timesteps):
                for i in range(self.timesteps):
                    if i > j:
                        discharging_Aub_subset[i,j]=-1
            discharging_bub_subset=(initial_battery_energy)*np.ones((self.timesteps,1),float)

            #Build Load Relation subet of inequality matrix
            relation_Aub_subset=np.zeros((self.timesteps,2*self.timesteps),float)
            for j in range(self.timesteps):
                for i in range(self.timesteps):
                    if i==j:
                        relation_Aub_subset[i,j]=-1
                        relation_Aub_subset[i,j+self.timesteps]=1
            relation_bub_subset=basis_load


            A_ub=np.append(np.append(charging_Aub_subset,discharging_Aub_subset,axis=0),relation_Aub_subset,axis=0)
            b_ub=np.append(np.append(charging_bub_subset,discharging_bub_subset,axis=0),relation_bub_subset,axis=0)

            # Build cyclic equality constraints
            A_eq=np.ones((1,self.timesteps*2),float)
            for i in range(self.timesteps):
                A_eq[0,i+self.timesteps]=-1
            
            b_eq=(final_battery_energy-initial_battery_energy)*np.ones((1,1),float)

            bound_seq_storage= [(0,battery_energy_capacity/ENERGY2POWERRATIO*self.resolution) for i in range(self.timesteps*2)]

            try:    
                res=linprog(obj_coefficient_array, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bound_seq_storage, method='interior-point')
        
                battery_energy=np.zeros((self.timesteps,1),float)
                for i in range(self.timesteps):
                    if i ==0:
                        battery_energy[i,0]=initial_battery_energy+res.x[i]*self.resolution-res.x[i+self.timesteps]*self.resolution
                    else:
                        battery_energy[i,0]=battery_energy[i-1,0]+res.x[i]*self.resolution-res.x[i+self.timesteps]*self.resolution
                
                battery_power=np.zeros((self.timesteps,1),float)
                for i in range(self.timesteps):
                    battery_power[i,0]=res.x[i+self.timesteps]-res.x[i]
                
                self.battery_profile.append([res.x[i+self.timesteps]-res.x[i] for i in range(self.timesteps)])
                
                # net_load_energy_initial=np.sum(basis_load)*self.resolution
                net_load_energy_result=np.sum(basis_load[48:-48, :]-battery_power[48:-48, :])*self.resolution

                net_load = (basis_load-battery_power).tolist()
                self.netloadprofile.append([el for val in net_load for el in val])
                
            
                if n==0:
                    result_matrix=np.zeros((self.iterations,3),float)
                result_matrix[n,0]=float(n)
                result_matrix[n,1]= battery_energy_capacity
                result_matrix[n,2]= net_load_energy_result    
            
            except Exception as err:
                if n==0:
                    result_matrix=np.zeros((self.iterations,3),float)
                result_matrix[n,0]=float(n)
                result_matrix[n,1]=0
                result_matrix[n,2]=0  

        self.results_dataframe =pd.DataFrame(result_matrix)
        self.results_dataframe.columns=['Iteration','Energy_Capacity','Total_Net_Load']

        print(self.results_dataframe)
        relative_change=pd.DataFrame((self.results_dataframe['Total_Net_Load'].values[1:]\
            - self.results_dataframe['Total_Net_Load'].values[:-1])/self.results_dataframe['Total_Net_Load'].values[:-1])
        self.results_dataframe['Relative_Change'] = pd.DataFrame(np.zeros((1,1),float)).append(relative_change, ignore_index=True)
        
        try:
            self.max_relative_change_index = self.results_dataframe['Relative_Change'].idxmin()
            print(self.max_relative_change_index, len(self.battery_profile))
            self.optimal_size=(self.results_dataframe['Energy_Capacity'].loc[self.results_dataframe['Relative_Change'].idxmin()]/ENERGY2POWERRATIO,\
                self.results_dataframe['Energy_Capacity'].loc[self.results_dataframe['Relative_Change'].idxmin()])
        except:
            self.optimal_size=(0,0)
        
        return self.optimal_size

    def get_result(self):

        return self.results_dataframe

    def get_battery_profile(self):

        return self.battery_profile[self.max_relative_change_index]


    def get_netloadprofile(self):

        return self.netloadprofile[self.max_relative_change_index]

    
    def get_battery_energy_profile(self):

        b_energy = []
        initial_energy = self.optimal_size[1]/2
        battery_profile = self.get_battery_profile()
        for bp in battery_profile:
            initial_energy -= bp
            b_energy.append(initial_energy)

        
        return b_energy


if __name__ == '__main__':

    data_path  = 'C:/Users/KDUWADI/Box/BYPL-USAID research/Data/extracted_profile/TG-LGR017A-1-2019_dataframe.csv'
    trans_data = pd.read_csv(data_path)['TransformerPower'].tolist()
    trans_data = [el if not math.isnan(el) else 0 for el in trans_data]
    solar_path = r'C:\Users\KDUWADI\Box\BYPL-USAID research\Data\extractedbypldata\solar_data.csv'
    solar_data = pd.read_csv(solar_path)['Irradiane'].tolist()
    solar_data = [el*70 for el in solar_data]
    

    instance = BTMsizing(trans_data[:48*7], solar_data[:48*7], 0.5, 20)
    print(instance.optimal_size)
    result_dataframe = instance.get_result()
    print(result_dataframe['Total_Net_Load'])

    battery_profile = instance.get_battery_profile()
    netloadprofile = instance.get_netloadprofile()
    batteryenergy = instance.get_battery_energy_profile()

    # print(battery_profile)
    # print(netloadprofile)
    # print(batteryenergy)

    plt.plot(range(48*7), trans_data[:48*7],label='trans profile')
    plt.plot(range(48*7), solar_data[:48*7],label='solar profile')
    plt.plot(range(len(battery_profile)), battery_profile, label='battery profile')
    plt.plot(range(len(netloadprofile)), netloadprofile, label='net load profile')
    plt.plot(range(len(batteryenergy)), batteryenergy,label='battery energy')
    plt.legend()
    plt.show()
    

