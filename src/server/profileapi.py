# Standard modules
from datetime import datetime as dt
from datetime import timedelta
import calendar
import pandas as pd
import math
import logging

LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'
logger = logging.getLogger()
logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

class ProfileAPI:

    def __init__(self, config_dict, profile_handler):

        self.config_dict = config_dict
        self.profile_handler = profile_handler

        self.dashboard_data = {

            'date': {
                'format': 'month',
                'data':['2018-1-1 1:15:0','2018-1-1 5:15:0','2018-3-1 1:15:0','2018-4-1 1:15:0','2018-12-1 1:15:0']
            },
            'weather_data' : [
                {'key':'Temperature', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Humidity', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
            ],
            'date_data' : [
                {'key':'Month', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Day', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'Hhindex', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'},
                {'key':'Hday', 'data':[0,0,0,0,0],'color': 'rgba(255,255,0,1)'},
                {'key':'Domestic', 'data': [0,0,0,0,0],'color': 'rgba(255,0,255,1)'},
                {'key':'NonDomestic', 'data':[0,0,0,0,0],'color': 'rgba(0,255,255,1)'},
                {'key':'Industrial', 'data': [0,0,0,0,0],'color': 'rgba(255,125,125,1)'},
            ],
            'load_data' : [
                {'key':'DT_original', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'DT_prediction', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'Domestic_prediction', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'},
                {'key':'Nondomestic_prediction', 'data':[0,0,0,0,0],'color': 'rgba(255,255,0,1)'},
                {'key':'Industrial_prediction', 'data':[0,0,0,0,0],'color': 'rgba(0,255,255,1)'},
            ]
        }

       
        year = {
            2016: ['2016-6-1 0:0:0','2016-12-31 23:30:0'],
            2017: ['2017-1-1 0:0:0','2017-12-31 23:30:0'],
            2018: ['2018-1-1 0:0:0','2018-12-31 23:30:0'],
            2019: ['2019-1-1 0:0:0','2019-12-31 23:30:0'],
            2020: ['2020-1-1 0:0:0','2020-3-1 23:30:0']
        }

        self.change_date()

        print(self.config_dict)

        self.profile_handler.create_dataframe(dt_name=self.config_dict['transformer'],
                        start_date=dt.strptime(year[self.today.year][0], '%Y-%m-%d %H:%M:%S'), 
                        end_date=dt.strptime(year[self.today.year][1], '%Y-%m-%d %H:%M:%S'))
        
        self.profile_handler.execute_all_lm()

        logger.info('Finished statistical modelling')
        for id, col_name in enumerate(['Temperature', 'Humidity']):
            self.dashboard_data['weather_data'][id]['data'] = self.profile_handler.dataformodel[col_name][self.timestamps].to_list()
        logger.info('Finished accessing temperature and humidity')
        
        for id, col_name in enumerate(['Month', 'Day', 'Hhindex','Hday','Domestic','NonDomestic','Industrial']):
            self.dashboard_data['date_data'][id]['data'] = self.profile_handler.dataformodel[col_name][self.timestamps].to_list()

        df = pd.DataFrame({'TransformerOriginal':self.profile_handler.dataformodel['TransformerPower']})
        for group, result in self.profile_handler.prediction_result.items():
            df[group] = result
        df.index = self.profile_handler.dataformodel.index

        for id, col_name in enumerate(['TransformerOriginal','TransformerPrediction','Domestic','NonDomestic','Industrial']):
            
            if col_name not in list(df.columns):
                self.dashboard_data['load_data'][id]['data'] = [0]*len(self.dashboard_data['load_data'][0]['data'])
            else:
                self.dashboard_data['load_data'][id]['data'] = df[col_name][self.timestamps].to_list()


        for col_name in ['weather_data','date_data','load_data']:
            for id in range(len(self.dashboard_data[col_name])):
                self.dashboard_data[col_name][id]['data'] = [ \
                    el if not math.isnan(el) else 0 for el in self.dashboard_data[col_name][id]['data']]

    def get_data(self):


        return self.dashboard_data


    def change_date(self):
        
        self.today = dt.strptime(self.config_dict['day'],'%Y-%m-%d')
        if self.config_dict['mode'] == 'Daily':
            self.dashboard_data['date']['format'] = 'hour'
            self.timestamps = [dt(self.today.year, self.today.month, self.today.day, 0,0,0) \
                        + timedelta(minutes=30)*i for i in range(48)]
            
        elif self.config_dict['mode'] == 'Yearly':
            self.dashboard_data['date']['format'] = 'month'
            num_of_days = 366 if calendar.isleap(self.today.year) else 365
            self.timestamps = [dt(self.today.year, 1,1, 0,0,0) \
                        + timedelta(minutes=30)*i for i in range(48*num_of_days)]

        elif self.config_dict['mode'] == 'Weekly':
            self.dashboard_data['date']['format'] = 'day'
            self.timestamps = [dt(self.today.year, self.today.month, self.today.day, 0,0,0) \
                        + timedelta(minutes=30)*i for i in range(48*7)]
        
        self.dashboard_data['date']['data'] = [date.strftime('%Y-%m-%d %H:%M:%S') \
           for date in self.timestamps]