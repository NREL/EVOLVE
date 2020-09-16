# Standard libraries
import logging
import os
import json
import datetime 
import math
import copy

# External libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.diagnostic import het_white
import matplotlib.pyplot as plt

# Internal libraries
from generate_profile.constants import LOG_FORMAT, DATE_FORMAT

class LinearModel:

    """ A class to develop a linear regression model to predict 
    transformer power profile bases on exogenous parameters mainly 
    weatherdata.
    """

    def __init__(self,config_json_path="BYPL-NREL-Effort\\generate_profile\\config.json"):

        """ Constructor """

        # setup logger
        self.logger = logging.getLogger()
        logging.basicConfig(format=LOG_FORMAT,level='DEBUG')

        # read settings 
        if isinstance(config_json_path,str):
            with open(config_json_path,'r') as json_file:
                self.config = json.load(json_file)
        
        elif isinstance(config_json_path,dict):
            self.config = config_json_path

        else:
            raise TypeError(f"Invalid type for 'config_json_path' can be only {dict,str}")
        
        # TODO: validate settings

        self.logger.info('Reading data .......')

        # Read all data
        self.data = {
            'weatherdata': pd.read_csv(self.config["weatherdatapath"],parse_dates=True,index_col='TimeStamps'),
            'dtprofile':pd.read_csv(self.config["dtprofilepath"],parse_dates=True,index_col='TimeStamps'),
            'datedata':pd.read_csv(self.config["datedatapath"],parse_dates=True,index_col='TimeStamps'),
            'consumerenergydata':pd.read_csv(self.config["consumerdatapath"])
        }

        self.start_date = datetime.datetime.strptime(self.config["start_date"],DATE_FORMAT)
        self.end_date = datetime.datetime.strptime(self.config["end_date"],DATE_FORMAT)

        self.timelist = [date for date in self.data['dtprofile'].index \
                            if date>=self.start_date and date <=self.end_date]

        self.logger.info('Imported data successfully.')

    def create_dataframe(self, dt_name = '',start_date='', end_date=''):
        
        if start_date != '' and end_date != '':
            self.timelist = [date for date in self.data['dtprofile'].index \
                            if date>=start_date and date <= end_date]
        
        self.energy_proportion = self.generate_energy_proportion_dataframe()
                
        self.dataformodel = pd.concat([
                self.data['weatherdata'].loc[self.timelist],
                self.data['datedata'].loc[self.timelist],
                self.energy_proportion
            ],axis=1,sort=False)
        
        if dt_name =='': dt_name = self.config['dt_name']

        self.dataformodel['TransformerPower'] = self.data['dtprofile'][dt_name] \
                                                    .loc[self.timelist]
        
        dataset_name = self.config['file_name'].split('.')[0] + '_dataframe.csv'
        #self.dataformodel.to_csv(os.path.join(self.config['export_folder'],dataset_name))
        #self.normalizedtprofile()
        self.dataformodel['TransformerPower'] = [el if el>0 else 0.01 \
                                                for el in self.dataformodel['TransformerPower']]

        self.logger.info('Created dataframe successfully')
    
    def normalizedtprofile(self):

        trans_power = self.dataformodel['TransformerPower'].tolist()
        self.dataformodel['TransformerPower'] = [x/max(trans_power) for x in trans_power]
        self.logger.info('Transformer power is normalized')
    
    
    def get_dataformodel(self):
        """ returns data for model """
        return self.dataformodel

    def summary_totext(self):
        """ returns a text file of model summary"""

        textfile = open('texts.txt','w')
        textfile.write(self.result.summary().as_text())
        textfile.close()


    def lm_model(self,group_name, model):

        # Normalize transformer power profile
        
        self.group_name = group_name

        # develop a statistical model
        self.dataformodel = self.dataformodel.fillna(0)
        self.model = smf.ols(model,data=self.dataformodel)

        self.logger.info(f'Model developed --> "{model}"')

        # fit and predict model
        self.result = self.model.fit()
        #self.check_heteroskedasticity()
        #self.generate_qqplot()

        self.summary_totext()

        self.trans_prediction = self.result.predict(self.dataformodel)
        self.trans_prediction = [np.exp(el) for el in self.trans_prediction]

        # predict for group 
        self.copydata = copy.deepcopy(self.dataformodel)

        temp_dict = {'Domestic':0,'NonDomestic':0,'Industrial':0}
        temp_dict[self.group_name] = 1

        for key,value in temp_dict.items():
            self.copydata[key] = [value]*len(self.copydata)

        self.prediction = self.result.predict(self.copydata)
        self.prediction = [np.exp(x) for x in self.prediction]

        monthly_total_energy_dict = {}
        for tpower, date in zip(self.trans_prediction,self.dataformodel.index):
            key_name = f'{date.year}-{date.month}'
            if key_name not in monthly_total_energy_dict:
                monthly_total_energy_dict[key_name] = 0
            if not math.isnan(tpower):
                monthly_total_energy_dict[key_name] += tpower

        monthly_energy_group_dict = {}
        for date, power in zip(self.dataformodel.index, self.prediction):
            key_name = f'{date.year}-{date.month}'
            if key_name not in monthly_energy_group_dict:
                monthly_energy_group_dict[key_name] = 0
            if not math.isnan(power):
                monthly_energy_group_dict[key_name] += power

        contribution_coefficient_dict = {}
        for date in self.dataformodel.index:
            key_name = f'{date.year}-{date.month}'
            contribution_coefficient_dict[key_name] = self.dataformodel[self.group_name][date]

        for key, value in monthly_energy_group_dict.items():
            monthly_energy_group_dict[key] = monthly_total_energy_dict[key] \
                                            *contribution_coefficient_dict[key]/value
        
        self.prediction_mod = []
        for power, date in zip(self.prediction,self.dataformodel.index):
            key_name = f'{date.year}-{date.month}'
            self.prediction_mod.append(power*monthly_energy_group_dict[key_name])

        self.logger.info(f'Model used for predictiong "{group_name}" group')
         
    def get_group_prediction(self):
        
        return self.prediction_mod

    def get_transformer_prediction(self):

        return self.trans_prediction

    # "np.log(TransformerPower) ~ C(Hhindex)*Domestic*C(Month)\
    #                             + Temperature*Domestic + Humidity*Domestic \
    #                             + C(Month) + C(Hhindex)*Hday*Domestic"

    def get_dommodel(self):

        return "np.log(TransformerPower) ~ C(Hhindex)*Domestic*C(Month)\
                                + Temperature*Domestic*C(Month) + Humidity*Domestic*C(Month) \
                                + C(Hhindex)*C(Hday)*C(Month)"
    def get_ndommodel(self):

        return "np.log(TransformerPower) ~ C(Hhindex)*NonDomestic*C(Month)\
                                + Temperature*NonDomestic*C(Month) + Humidity*NonDomestic*C(Month) \
                                + C(Hhindex)*C(Hday)*C(Month)"

    def get_indmodel(self):

        return "np.log(TransformerPower) ~ C(Hhindex)*Industrial*C(Month)\
                                + Temperature*Industrial*C(Month) + Humidity*Industrial*C(Month) \
                                + C(Month)*C(Hhindex)*C(Hday)"
    
    def generate_qqplot(self):

        sm.qqplot(self.result.resid,line="45")
        plt.show()
    
    def check_heteroskedasticity(self):

        white_test = het_white(self.result.resid,  [self.dataformodel['Temperature']])

        #bp_test = het_breuschpagan(self.result.resid, self.result.model.exog)

        labels = ['LM Statistic', 'LM-Test p-value', 'F-Statistic’', 'F-Test p-value']
        #self.logger.info(dict(zip(labels, bp_test)))
        self.logger.info(dict(zip(labels, white_test)))
    
    def execute_all_lm(self):

        model_dict = {
            'Domestic': self.get_dommodel(),
            'NonDomestic':self.get_ndommodel(),
            'Industrial': self.get_indmodel()
        }

        self.prediction_result = {}

        for group in self.class_keys:
            self.lm_model(group,model_dict[group])
            self.prediction_result[group] = self.get_group_prediction()
            self.prediction_result['TransformerPrediction'] = self.get_transformer_prediction()
        

    def export_all(self):

        df = pd.DataFrame({'TransformerOriginal':self.dataformodel['TransformerPower']})
        for group, result in self.prediction_result.items():
            df[group] = result
        df.index = self.dataformodel.index
        df.to_csv(os.path.join(self.config['export_folder'],self.config['file_name']))

        self.logger.info(f'exported all prediction for transformer {self.config["dt_name"]}')


    def generate_energy_proportion_dataframe(self):

        """ For a specified dt, generates a time-series dataframe with proportion of energy
        consumption for three classes : domestic, non-domestic and industrial
        """

        # Extract dataframe for a dt
        dt_name = self.config['dt_name']
        energy_data_grouped = self.data['consumerenergydata'].groupby('DT_CODE')
        energydata = energy_data_grouped.get_group(dt_name)

        # Extract dataframe 
        group_byclass = energydata.groupby('BILLING_CLASS')
        class_dict = {group: [] for group in group_byclass.groups}


        for key in class_dict.keys():

            energydata_byclass = group_byclass.get_group(key)

            for date in self.timelist:
                col_name = str(date.month) + '/1/' + str(date.year)
                
                if col_name in energydata_byclass:
                    class_dict[key].append(sum(energydata_byclass[col_name].tolist()))
                else:
                    class_dict[key].append(1)

        mapper = {'DOM':'Domestic','NDOM':'NonDomestic','SIP':'Industrial'}

        df = pd.DataFrame()
        for id, key in enumerate(class_dict):
            temp_arr = []
            for x in zip(*[v for k,v in class_dict.items()]):
                x_mod = [xs if xs>0 else 0 for xs in x]
                contribution_pu = x_mod[id]/sum(x_mod) if sum(x_mod) !=0 else 0 
                temp_arr.append(contribution_pu)
            temp_arr = [el if el !=0 else 0.01 for el in temp_arr]
            df[mapper[key]] = temp_arr

        
        df.index = self.timelist

        # fill with zeros if a class is not present
        for keys, values in mapper.items():
            if values not in df.columns:
                df[values] = [0]*len(df)

        self.class_keys = [mapper[key] for key in class_dict.keys()]

        self.logger.info(f"Developed energy proportion dataframe for transformer {dt_name}")
    
        return df


if __name__ == '__main__':

    # model_instance = LinearModel(config_json_path="BYPL-NREL-Effort\\generate_profile\\config.json")
    # model_instance.create_dataframe()
    # model_instance.execute_all_lm()
    # model_instance.export_all()

    with open("src\\generate_profile\\config.json",'r') as json_file:
        config_dict = json.load(json_file)

    trans_list = ['TG-LGR017A-1', 'TG-LGR017A-2', 'TG-LGR046A-1', 'TG-LGR046A-2', 'TG-LGR054A-1', 
                'TG-LGR054A-2', 'TG-LGR080A-1', 'TG-PNR104A-1', 'TG-PNR104A-2', 'TG-PNR105A-1', 
                'TG-PNR120A-1', 'TG-PNR120A-2', 'TG-PNR120A-3', 'TG-PNR121A-1', 'TG-PNR128A-1', 
                'TG-PNR161A-1', 'TG-PNR189A-1', 'TG-VNG046A-1', 'TG-VNG046A-2', 'TG-VNG058A-1', 
                'TG-VNG071A-1', 'TG-VNG071A-2', 'TG-VNG071A-3', 'TG-VNG072A-1', 'TG-VNG072A-2', 
                'TG-VNG075A-1', 'TG-VNG075A-2', 'TG-VNG103A-1', 'TG-VNG103A-2', 'TG-VNG103A-3', 
                'TG-VNG107A-1', 'TG-VNG107A-2']
    
    year_start_list = ['2016-6-1 0:0:0','2017-1-1 0:0:0','2018-1-1 0:0:0','2019-1-1 0:0:0','2020-1-1 0:0:0']
    year_end_list = ['2016-12-31 23:30:0','2017-12-31 23:30:0','2018-12-31 23:30:0','2019-12-31 23:30:0','2020-3-1 0:0:0']
    year = ['2016','2017','2018','2019','2020']

    # for trans in trans_list:
    #     for start_date, end_date, yr in zip(year_start_list,year_end_list,year):
    #         config_dict["start_date"] = start_date
    #         config_dict["end_date"] = end_date
    #         config_dict['dt_name'] = trans
    #         config_dict["export_folder"] = "C:\\Users\\KDUWADI\\Box\\BYPL-USAID research\\Data\\extracted_profile"
    #         config_dict["file_name"] = trans + '-' + yr + '.csv'

    #         model_instance = LinearModel(config_dict)
    #         model_instance.create_dataframe()
    #         model_instance.execute_all_lm()
    #         model_instance.export_all()
    #         del model_instance



    trans = 'TG-LGR017A-1'
    config_dict["start_date"] = '2019-1-1 0:0:0'
    config_dict["end_date"] = '2019-12-31 23:30:0'
    config_dict['dt_name'] = trans
    config_dict["export_folder"] = "C:\\Users\\KDUWADI\\Desktop"
    config_dict["file_name"] = trans + '-' + str(2019) + '.csv'
    
    model_instance = LinearModel(config_dict)
    model_instance.create_dataframe()
    model_instance.execute_all_lm()
    model_instance.export_all()
    model_instance.dataformodel.to_csv(os.path.join(config_dict['export_folder'],trans+'.csv'))
    del model_instance
    
