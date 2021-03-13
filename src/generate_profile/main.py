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

    def __init__(self, 
            dt_dataframe, 
            customer_dataframe, 
            weather_dataframe,
            date_dataframe,
            ):

        """ Constructor """

        # setup logger
        self.logger = logging.getLogger()
        logging.basicConfig(format=LOG_FORMAT,level='DEBUG')


        self.logger.info('Reading data .......')

        # generate date_dataframe

        self.data = {
            'weatherdata': weather_dataframe,
            'dtprofile': dt_dataframe,
            'consumerenergydata' : customer_dataframe,
            'datedata': date_dataframe
        }

        self.logger.info('Imported data successfully.')

    def create_dataframe(self,dt_name, start_date, end_date):

        self.dt_name = dt_name

        self.logger.info(f"start_date: {start_date}, end date: {end_date}")
        
        if start_date != '' and end_date != '':
            self.timelist = [date for date in self.data['dtprofile'].index \
                            if date>=start_date and date <= end_date]
        
        self.energy_proportion = self.generate_energy_proportion_dataframe(self.dt_name)
                
        self.dataformodel = pd.concat([
                self.data['weatherdata'].loc[self.timelist],
                self.data['datedata'].loc[self.timelist],
                self.energy_proportion
            ],axis=1,sort=False)
        

        self.dataformodel['TransformerPower'] = self.data['dtprofile'][self.dt_name] \
                                                    .loc[self.timelist]
        
        #dataset_name = self.config['file_name'].split('.')[0] + '_dataframe.csv'
        #self.dataformodel.to_csv(os.path.join(self.config['export_folder'],dataset_name))
        #self.normalizedtprofile()

        self.dataformodel['TransformerPower'] = [el if el>0 else 0.01 \
                                                for el in self.dataformodel['TransformerPower']]

        self.logger.info(f'Created dataframe successfully : {self.dt_name}')
    
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

        temp_dict = {'Domestic':0,'Commercial':0,'Industrial':0}
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

        return "np.log(TransformerPower) ~ C(Hhindex)*Commercial*C(Month)\
                                + Temperature*Commercial*C(Month) + Humidity*Commercial*C(Month) \
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
            'Commercial':self.get_ndommodel(),
            'Industrial': self.get_indmodel()
        }

        self.prediction_result = {}

        for group in self.class_keys:
            self.lm_model(group,model_dict[group])
            self.prediction_result[group] = self.get_group_prediction()
            self.prediction_result['TransformerPrediction'] = self.get_transformer_prediction()
        
        self.logger.info('finished executing lms')

    def export_all(self):

        df = pd.DataFrame({'TransformerOriginal':self.dataformodel['TransformerPower']})
        for group, result in self.prediction_result.items():
            df[group] = result
        df.index = self.dataformodel.index
        #df.to_csv(os.path.join(self.config['export_folder'],self.config['file_name']))

        #self.logger.info(f'exported all prediction for transformer {self.config["dt_name"]}')


    def generate_energy_proportion_dataframe(self, dt_name):

        """ For a specified dt, generates a time-series dataframe with proportion of energy
        consumption for three classes : domestic, non-domestic and industrial
        """

        # Extract dataframe for a dt
        energy_data_grouped = self.data['consumerenergydata'].groupby('Transformer Name')
        energydata = energy_data_grouped.get_group(dt_name)

        # Extract dataframe 
        group_byclass = energydata.groupby('Customer Type')
        class_dict = {group: [] for group in group_byclass.groups}


        for key in class_dict.keys():

            energydata_byclass = group_byclass.get_group(key)

            for date in self.timelist:
                col_name = str(date.month) + '/1/' + str(date.year)
                
                if col_name in energydata_byclass:
                    class_dict[key].append(sum(energydata_byclass[col_name].tolist()))
                else:
                    class_dict[key].append(1)

        mapper = {'domestic':'Domestic','commercial':'Commercial','industrial':'Industrial'}

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

   pass
    
