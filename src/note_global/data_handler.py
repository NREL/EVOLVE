# Standard imports
import os
from datetime import datetime as dt
import numpy as np
from calendar import monthrange
import calendar
import logging

# Third-party imports
import pandas as pd

# Internal imports

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

        if 'dtpower_file' in self.config_dict:
            self.dt_data = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                                self.config_dict['dtpower_file']))
    
            self.dt_data.columns = ['GRID','PANEL_NO','FEEDER_ID','GRID_NAME','FEEDER_NAME','SDO',
                    'ZONE','FL_CODE','SSTN_NAME','DT_CODE','DT_KVA','METERNO','WH_ABS','DATE','MONTH',
                    'MF','ENERGY(kwh)']
            self.feeders = list(self.dt_data.groupby('FEEDER_NAME').groups)
        
        if 'solar_irradiance_file' in self.config_dict:
            self.solar_data = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                            self.config_dict['solar_irradiance_file']),parse_dates=['Date'],index_col='Date')
        
        if 'dt_metrics_file' in self.config_dict:
            self.dt_metrics = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                                self.config_dict['dt_metrics_file']),parse_dates=['Date'])

        if 'feeder_metrics' in self.config_dict:
            self.feeder_metrics = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                    self.config_dict['feeder_metrics']),parse_dates=['Date'])

        if 'customer_energy' in self.config_dict:
            self.customers_energy = pd.read_csv(os.path.join(self.config_dict['project_path'],\
                    self.config_dict['customer_energy']))

        self.logger.info('All files successfully read')


    def get_trans_capacity(self):

        self.trans_capacity = {}
        group_by_dt = self.dt_data.groupby('DT_CODE')
        for trans_name in list(group_by_dt.groups):
            capacity = group_by_dt.get_group(trans_name)['DT_KVA'].tolist()
            self.trans_capacity[trans_name] = capacity[0]

    def get_customernumber_bygroup(self, name, dtorfeeder):

        col_name = 'DT_CODE' if dtorfeeder == 'DT' else 'FEEDER NAME'
        dt_customer_energy = self.customers_energy.groupby(col_name).get_group(name)
        customer_number_by_group = {'DOM':0,'NDOM':0,'SIP':0}
        grouped_by_custtype = dt_customer_energy.groupby('BILLING_CLASS')
        for cust_group in list(grouped_by_custtype.groups):
            customer_number_by_group[cust_group] = len(grouped_by_custtype.get_group(cust_group))

        return list(customer_number_by_group.values())


    def get_loaddataframe(self,dt_name,year):

        result_path = self.config_dict['linear_model_results_path']
        filename = dt_name+'-'+str(year)+'.csv'
        dt_result_dataframe = pd.read_csv(os.path.join(result_path,filename),parse_dates=[0])
    
        return dt_result_dataframe
                

    def return_solar_multiplier(self,startdate,mode):

        num_of_days= 366 if calendar.isleap(startdate.year) else 365

        data = self.solar_data['Irradiane']
        
        if mode=='Daily':
            date_range = pd.date_range(startdate,periods=48,freq='30min')

        if mode == 'Weekly':
            date_range = pd.date_range(startdate,periods=48*7,freq='30min')
                    
        if mode == 'Monthly':
            date_range = pd.date_range(dt(startdate.year,startdate.month,1,0,0,0),\
                periods=48*monthrange(startdate.year, startdate.month)[1],freq='30min')

        if mode == 'Yearly':
            date_range = pd.date_range(dt(startdate.year,1,1,0,0,0),\
                periods=48*num_of_days,freq='30min')


        return [data[date] for date in date_range]


    def feeder_pv_profile(self, feeder_name, date,mode):

        feeder_df = self.dt_data.groupby('FEEDER_NAME').get_group(feeder_name)

        data_list, data_list_high_res = [],[]
        for dt in list(feeder_df.groupby('DT_CODE').groups):

            data, data_high_res = self.dt_pv_profile(dt, date,mode)
            if data != None:
                if data_list == []: 
                    data_list = data_list
                    data_list_high_res = data_high_res
                else:
                    data_list = [sum(x) for x in zip(data_list,data)]
                    data_list_high_res = [sum(x) for x in zip(data_list_high_res,data_high_res)]

        return data_list, data_list_high_res


    def dt_pv_profile(self,dist,startdate, mode):

        pv_dict = {'TG-VNG071A-3': {'Date': ['8/19/2016'], 'PVcapacity': [5]}, 
                'TG-VNG071A-1': {'Date': ['7/4/2018', '10/12/2018'], 'PVcapacity': [20, 50]}, 
                'TG-VNG107A-2': {'Date': ['5/1/2018', '5/1/2018'], 'PVcapacity': [10, 10]}, 
                'TG-VNG046A-2': {'Date': ['5/14/2018'], 'PVcapacity': [5]}, 
                'TG-VNG072A-2': {'Date': ['8/20/2018', '8/20/2018'], 'PVcapacity': [10, 10]}, 
                'TG-LGR046A-2': {'Date':['9/8/2018'], 'PVcapacity': [9]}, 
                'TG-VNG058A-1': {'Date': ['10/5/2018', '6/10/2019', '6/12/2019'], 'PVcapacity': [10, 3, 3]}, 
                'TG-VNG107A-1': {'Date': ['5/22/2019'], 'PVcapacity': [6]}}

        
        irr_data = self.solar_data['Irradiane']


        for dt_name, data_dict in pv_dict.items():

            num_of_days= 366 if calendar.isleap(startdate.year) else 365

            if dist == dt_name:
                date_list = [dt.strptime(date,'%m/%d/%Y') for date in data_dict['Date']]
                
                sortedtuplelist = sorted(zip(date_list,data_dict['PVcapacity']),key=lambda x:x[0])
                pv_capacity = sum([x[1] for x in sortedtuplelist if x[0]<=startdate])

                if mode=='Daily':
                    date_range = pd.date_range(startdate,periods=48,freq='30min')

                if mode=='Weekly':
                    date_range = pd.date_range(startdate,periods=48*7,freq='30min')
                    
                if mode == 'Monthly':
                    date_range = pd.date_range(dt(startdate.year,startdate.month,1,0,0,0),\
                        periods=48*monthrange(startdate.year, startdate.month)[1],freq='30min')

                if mode == 'Yearly':
                    date_range = pd.date_range(dt(startdate.year,1,1,0,0,0),\
                        periods=48*num_of_days,freq='30min')
                
                pv_range = []
                solarmultipler = [irr_data[date] for date in date_range]
                which_dates = [x[0] for x in sortedtuplelist if x[0] in date_range and x[0] != startdate]
                
                if which_dates !=[]:
                    for pv_conn_date in which_dates:
                            pv_range = pv_range + [pv_capacity]*len([date for date in date_range \
                                if date <pv_conn_date])

                            pv_capacity = sum([x[1] for x in sortedtuplelist if x[0]<=pv_conn_date])

                    if len(pv_range) < len(date_range):
                            pv_range += [pv_capacity]*(len(date_range)-len(pv_range))
                else:
                    pv_range = [pv_capacity]*len(date_range)

                pv_range = [x[0]*x[1]*0.5 for x in zip(pv_range,solarmultipler)]
                
                if mode =='Daily': 
                    return pv_range, pv_range
                
                if mode == 'Weekly':
                    return [sum(x)*24 for x in np.array_split(pv_range,7)], pv_range

                if mode == 'Monthly':
                    return [sum(x)*24 for x in np.array_split(pv_range,\
                        monthrange(startdate.year, startdate.month)[1])], pv_range
                
                if mode == 'Yearly':
                    return [sum(x)*24 for x in np.array_split(pv_range,num_of_days)], pv_range

        return None,None

    
    
    def analyze_feeder(self,feeder_name, year, mode, userdate, startdate=[], enddate=[]):

        feeder_df = self.dt_data.groupby('FEEDER_NAME').get_group(feeder_name)
        dt_names = list(feeder_df.groupby('DT_CODE').groups)
        feeder_energy, feeder_energy_high_res = [], []
        for dist in dt_names:
            print(dist)
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

        self.grouped_dt_data = self.dt_data.groupby('DT_CODE')

        if startdate ==[]: startdate=dt(year,1,1,0,0,0)
        if enddate ==[]: enddate = dt(year,12,31,23,59,0)

        self.dist = self.grouped_dt_data.get_group(dt_name).reset_index()
        
        self.dt_df = pd.DataFrame({
            'DATE': self.dist['DATE'].tolist(),
            'Energy(kwh)': self.dist['ENERGY(kwh)'].tolist()
        })
       
        # Introducing year column to slice it by year
        self.dt_df['Year'] = [str(dt.strptime(date, '%m/%d/%Y %H:%M:%S').year) \
                    for date in self.dt_df['DATE'].tolist()]

        # Get data for input year
        self.dt_df_grouped_year = self.dt_df.groupby('Year')
        
        if str(year) in list(self.dt_df_grouped_year.groups):
            self.dt_df_year = self.dt_df_grouped_year.get_group(str(year))
    

            # Let's find out missing time stamps
            all_date_list = list(pd.date_range(startdate,enddate,freq='30min'))
            available_date_list = [dt.strptime(date, '%m/%d/%Y %H:%M:%S') \
                    for date in self.dt_df_year['DATE'].tolist()]
    
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
                weekly_date_list = pd.date_range(weekbegin,periods=48*7,freq='30min')

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


