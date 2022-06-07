# Standard imports
import os
from datetime import datetime as dt
import numpy as np
from calendar import monthrange
import calendar
import logging

# Third-party imports
import pandas as pd
from pandas.tseries.offsets import DateOffset
from constants import TIME_RESOLUTION, FACTOR

# Internal imports
from generate_profile.main import LinearModel

LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'

class DataHandler:

    def __init__(self,config_dict,logger=None):

        self.config_dict = config_dict
        
        
        if logger != None:
            self.logger = logger
        else:
            self.logger = logging.getLogger()
            logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

        self.read_files()
        self.get_trans_capacity()
        self.logger.info('DataHandler initiallized ..')
        

    def read_files(self):

        self.dt_data = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                                self.config_dict['dtpower_file']), parse_dates=['Date'])
        
        self.dt_metadata = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                                self.config_dict['dt_metadata_file']))
    
        self.feeders = set(self.dt_metadata['Feeder Name'].tolist())
        
        self.solar_data = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                            self.config_dict['solar_irradiance_file']),parse_dates=['Date'],index_col='Date')
        
        self.dt_to_feeder_map = dict(zip(self.dt_metadata['Transformer Name'], self.dt_metadata['Feeder Name']))


        if 'optional_data' in self.config_dict:
            self.customer_energy = pd.read_csv(os.path.join(self.config_dict['project_path'], \
                self.config_dict['optional_data']['folder_name'], self.config_dict['optional_data']['customer_energy_file']))

            self.weather_data = pd.read_csv(os.path.join(self.config_dict['project_path'], \
                self.config_dict['optional_data']['folder_name'], self.config_dict['optional_data']['weather_file']),
                parse_dates=['Date'])

            self.weather_data = self.weather_data.set_index('Date')
            self.date_data = pd.read_csv(os.path.join(self.config_dict['project_path'], \
                self.config_dict['optional_data']['folder_name'], self.config_dict['optional_data']['date_data_file']),
                parse_dates=['Date'])
            self.date_data = self.date_data.set_index('Date')
            
            # Here create linear model instace
            dt_data_indexed = self.dt_data.set_index('Date')
            
            self.profile_instance = LinearModel(dt_data_indexed, 
                    self.customer_energy, 
                    self.weather_data,
                    self.date_data)

        self.logger.info('All files successfully read')


    def get_trans_capacity(self):

        self.trans_capacity = dict(zip(self.dt_metadata['Transformer Name'],self.dt_metadata['KVA Capacity']))

    def get_customernumber_bygroup(self, name, dtorfeeder):

        if hasattr(self, 'customer_energy'):

            customer_energy_group = self.customer_energy.groupby('Transformer Name')

            if dtorfeeder == 'DT':
                customer_number_by_group = {'domestic':0,'commercial':0,'industrial':0}
                dt_group = customer_energy_group.get_group(name)
                grouped_by_custtype = dt_group.groupby('Customer Type')
                for cust_group in list(grouped_by_custtype.groups):
                    customer_number_by_group[cust_group] = len(grouped_by_custtype.get_group(cust_group))

                return list(customer_number_by_group.values())
            else:

                customer_number_by_group = {'domestic':0,'commercial':0,'industrial':0}
                for dist in self.dt_to_feeder_map:
                    if self.dt_to_feeder_map[dist] == name:
                        dt_group = customer_energy_group.get_group(dist)
                        grouped_by_custtype = dt_group.groupby('Customer Type')
                        for cust_group in list(grouped_by_custtype.groups):
                            customer_number_by_group[cust_group] += len(grouped_by_custtype.get_group(cust_group))

                return list(customer_number_by_group.values())

        return [1,1,1]

        

    # def get_loaddataframe(self,dt_name,year):

    #     result_path = self.config_dict['linear_model_results_path']
    #     filename = dt_name+'-'+str(year)+'.csv'
    #     dt_result_dataframe = pd.read_csv(os.path.join(result_path,filename),parse_dates=[0])
    
    #     return dt_result_dataframe
                

    def return_solar_multiplier(self,startdate,mode):

        num_of_days= 366 if calendar.isleap(startdate.year) else 365

        data = self.solar_data['Irradiance']
        
        if mode=='Daily':
            date_range = pd.date_range(startdate,periods=FACTOR*24,freq=DateOffset(minutes=TIME_RESOLUTION))

        if mode == 'Weekly':
            date_range = pd.date_range(startdate,periods=FACTOR*24*7,freq=DateOffset(minutes=TIME_RESOLUTION))
                    
        if mode == 'Monthly':
            date_range = pd.date_range(dt(startdate.year,startdate.month,1,0,0,0),\
                periods=FACTOR*24*monthrange(startdate.year, startdate.month)[1],freq=DateOffset(minutes=TIME_RESOLUTION))

        if mode == 'Yearly':
            date_range = pd.date_range(dt(startdate.year,1,1,0,0,0),\
                periods=FACTOR*24*num_of_days,freq=DateOffset(minutes=TIME_RESOLUTION))


        return [data[date] for date in date_range]


    
    def analyze_feeder(self,feeder_name, year, mode, userdate, startdate=[], enddate=[]):

     
        feeder_energy, feeder_energy_high_res = [], []

        for dist in self.dt_to_feeder_map:

            if self.dt_to_feeder_map[dist] == feeder_name:
          
                dt_data, dt_data_high_res = self.analyze_dt(dist,year,mode,userdate,startdate,enddate)
                t_data,p_data = zip(*dt_data)
                
                if feeder_energy == []:
                    feeder_energy = p_data
                    feeder_energy_high_res = dt_data_high_res
                
                else:
                    feeder_energy=[sum(filter(None,x)) for x in zip(p_data,feeder_energy)]
                    feeder_energy_high_res = [sum(filter(None,x)) for x in \
                        zip(dt_data_high_res,feeder_energy_high_res)]
        return zip(t_data,feeder_energy), feeder_energy_high_res

    
    def analyze_dt(self, dt_name, year, mode, userdate, startdate=[], enddate=[]):


        if startdate ==[]: startdate=dt(year,1,1,0,0,0)
        if enddate ==[]: enddate = dt(year,12,31,23,59,0)

        
        self.dt_df = pd.DataFrame({
            'DATE': self.dt_data['Date'].tolist(),
            'Energy(kwh)': self.dt_data[dt_name].tolist()
        })
       
        # Introducing year column to slice it by year
        self.dt_df['Year'] = [str(date.year) \
                    for date in self.dt_df['DATE'].tolist()]

        # Get data for input year
        self.dt_df_grouped_year = self.dt_df.groupby('Year')
        
        if str(year) in list(self.dt_df_grouped_year.groups):
            self.dt_df_year = self.dt_df_grouped_year.get_group(str(year))
    

            # Let's find out missing time stamps
            all_date_list = list(pd.date_range(startdate,enddate,freq=DateOffset(minutes=TIME_RESOLUTION)))
            available_date_list =  self.dt_df_year['DATE'].tolist()
    
            # Replace missing time-stamps with zero or None value
            temp_dict = dict(zip(available_date_list, self.dt_df_year['Energy(kwh)'].tolist()))
            new_dict = {date: None for date in all_date_list}
        
            new_dict = {**new_dict,**temp_dict}
        
            self.dt_data_by_year = pd.DataFrame({'DATE': [keys for keys in new_dict.keys()],
                                                'Average Power (kW)': list(new_dict.values())})

            self.dt_data_by_year = self.dt_data_by_year.set_index('DATE')
            self.dt_power_by_year = self.dt_data_by_year['Average Power (kW)']

            if mode == 'Daily':
                daily_dt_data = [[date,self.dt_power_by_year[date]] for date in self.dt_power_by_year.index \
                    if date.year==userdate.year and date.month==userdate.month and date.day==userdate.day]
                return daily_dt_data, [x[1] for x in daily_dt_data]

            if mode == 'Weekly':
                
                weekbegin = dt(userdate.year, userdate.month, userdate.day, 0,0,0)
                weekly_date_list = pd.date_range(weekbegin,periods=FACTOR*24*7,freq=DateOffset(minutes=TIME_RESOLUTION))

                weekly_dt_list = [self.dt_power_by_year[date] for date in weekly_date_list]

                weekly_dt_list_splitted = np.array_split(np.array(weekly_dt_list),7)
                weekly_date_list_splitted = np.array_split(np.array(weekly_date_list),7)

                return [[x[1][int(len(x[1])/2)],sum(filter(None, x[0]))] \
                    for x in zip(weekly_dt_list_splitted, weekly_date_list_splitted)], weekly_dt_list

            if mode == 'Monthly':
                monthly_dt_list = [self.dt_power_by_year[date] for date in self.dt_power_by_year.index \
                    if date.year==userdate.year and date.month==userdate.month]
                
                monthly_date_list = [date for date in self.dt_power_by_year.index \
                    if date.year==userdate.year and date.month==userdate.month]

                monthly_dt_list_splitted = np.array_split(np.array(monthly_dt_list),\
                        monthrange(userdate.year,userdate.month)[1])
                monthly_date_list_splitted = np.array_split(np.array(monthly_date_list), \
                        monthrange(userdate.year,userdate.month)[1])

                return [[x[1][int(len(x[1])/2)],sum(filter(None, x[0]))] \
                    for x in zip(monthly_dt_list_splitted, monthly_date_list_splitted)], monthly_dt_list

            if mode == 'Yearly':
                
                yearly_dt_list = [self.dt_power_by_year[date] for date in self.dt_power_by_year.index \
                    if date.year==userdate.year]
                yearly_date_list = [date for date in self.dt_power_by_year.index if date.year==userdate.year]
                
                num_of_days = 366 if calendar.isleap(userdate.year) else 365
                
                yearly_dt_list_splitted = np.array_split(np.array(yearly_dt_list), num_of_days)
                yearly_date_list_splitted = np.array_split(np.array(yearly_date_list), num_of_days)

                return [[x[1][int(len(x[1])/2)],sum(filter(None, x[0]))] \
                    for x in zip(yearly_dt_list_splitted, yearly_date_list_splitted)], yearly_dt_list

        else:
            return None, None


