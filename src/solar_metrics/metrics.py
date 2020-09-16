# Standard library
import os
import pickle
from datetime import datetime as dt
import math
import json

# Third-party library
import pandas as pd

# Internal library
from note_global.data_handler import DataHandler
from note_global.logger import getLogger
from note_global.validate import validate
from solar_metrics.constants import DEFAULT_CONFIGURATION #VALID_SETTINGS

class Metric:


    def __init__(self, config_path=None):

        if config_path != None:

            if isinstance(config_path,dict):
                self.config_dict = config_path
            else:
                with open(config_path,'r') as json_file:
                    self.config_dict = json.load(json_file)
            self.config_dict = {**DEFAULT_CONFIGURATION,**self.config_dict}

            self.logger = getLogger()
            
            validate(self.config_dict,VALID_SETTINGS)

            self.logger.info('Configuartion input validated..')

            self.data_handler = DataHandler(self.config_dict,self.logger)

            self.dtnames = list(self.data_handler.dt_data.groupby('DT_CODE').groups)
            self.feedernames = list(self.data_handler.dt_data.groupby('FEEDER_NAME').groups)


    def create_skeleton(self,project_path):

        if os.path.exists(project_path):
            with open(os.path.join(project_path,'config.json'),'w') as json_file:
                json.dump(DEFAULT_CONFIGURATION,json_file)
            

    def compute_feeder_metric(self):

        self.col_names = ['Date','FeederName','PVPenetration','Avg2Peak','PeakReduction',\
                'EnergyReduction','MaxRampRate']

        self.data_dict = {key:[] for key in self.col_names}

        # for feeder in self.feedernames:
        #     print(feeder)
        #     print(self.data_handler.get_customernumber_bygroup(feeder, 'feeder'))

        for feeder in self.feedernames:
        #for feeder in [self.feedernames[1]]:
            self.dt_data_by_feeder = self.data_handler.dt_data.groupby('FEEDER_NAME').get_group(feeder)
            
            for year in self.config_dict['year_list']:
                self.logger.info(f"Metric being exported for feeder {feeder} for year {year}")
                for month in range(1,13,1):
                    feeder_data = []
                    
                    for dt_name in list(self.dt_data_by_feeder.groupby('DT_CODE').groups):
                        self.logger.info(f"Operating transformer {dt_name} of feeder {feeder}")
                        
                        net_load, net_load_highres = self.data_handler.analyze_dt(dt_name,year,\
                            'Monthly',dt(year,month,1,0,0,0))
                        
                        if net_load_highres != None:
                            net_load_highres = [el if not math.isnan(el) else 0 for el in net_load_highres]
                       
                        #self.logger.info(f"len of net load high res {len(net_load_highres)} -- {dt_name} of feeder {feeder}")

                        if net_load != None:
                            if feeder_data == []: 
                                feeder_data = net_load_highres
                            else:
                                feeder_data = [sum(x) for x in zip(feeder_data,net_load_highres)]
                    
                    if feeder_data !=[]:
                        
                        net_load_highres = feeder_data
                        
                        solarmultiplier = self.data_handler.return_solar_multiplier\
                                    (dt(year,month,1),'Monthly')
                        pv_gen, pv_gen_highres = self.data_handler.feeder_pv_profile(feeder,\
                                dt(year,month,1,0,0,0), 'Monthly')

                        
                        baseload_highres = net_load_highres
                        if pv_gen != None and pv_gen != []:
                            baseload_highres = [sum(x) for x in zip(net_load_highres,pv_gen_highres)] 
                        
                    
                        baseload_highres_filternan = [el for el in baseload_highres if not math.isnan(el)]
                        if sum(baseload_highres_filternan) == 0:
                            baseload_highres_filternan = []
                        
                        self.logger.info(f"len of base load high res {len(baseload_highres_filternan)} -- of feeder {feeder} -- month {month}")
                        for pv_penetration in range(0,101,10):
                            if baseload_highres_filternan == []:
                                self.data_dict['Avg2Peak'].append(None)
                                self.data_dict['PeakReduction'].append(None)
                                self.data_dict['EnergyReduction'].append(None)
                                self.data_dict['MaxRampRate'].append(None)
                            else:
                               # self.logger.info('I am here!!')
                                load_with_pv = [el-max(baseload_highres)*pv_penetration\
                                    *solarmultiplier[id]/100 for id,el in enumerate(baseload_highres)\
                                    if not math.isnan(el)]

                                load_with_pv_abs = [abs(el) for el in load_with_pv]
                                
                                self.data_dict['Avg2Peak'].append(sum(load_with_pv)\
                                    /(len(load_with_pv_abs)*max(load_with_pv_abs)))

                                self.data_dict['PeakReduction'].append((max(baseload_highres) \
                                    - max(load_with_pv_abs))*100/(max(baseload_highres)))

                                self.data_dict['EnergyReduction'].append((sum(baseload_highres_filternan)-\
                                    sum(load_with_pv))*100/sum(baseload_highres_filternan))

                                ramprate = [load_with_pv[i+1]-load_with_pv[i] \
                                    for i in range(len(load_with_pv)-1)]

                                self.data_dict['MaxRampRate'].append(max(ramprate))

                            self.data_dict['PVPenetration'].append(str(pv_penetration)+'%')
                            self.data_dict['FeederName'].append(feeder)
                            self.data_dict['Date'].append(dt(year,month,1))
                    
                    else:
                        self.logger.info(f"Operating transformer -- empty feeder data -- {dt_name} of feeder {feeder}")
                        
                        for PVpen in range(0,101,10):
                            self.data_dict['LoadFactor'].append(None)
                            self.data_dict['PeakReduction'].append(None)
                            self.data_dict['EnergyReduction'].append(None)
                            self.data_dict['MaxRampRate'].append(None)
                            self.data_dict['PVPenetration'].append(str(pv_penetration)+'%')
                            self.data_dict['FeederName'].append(feeder)
                            self.data_dict['Date'].append(dt(year,month,1))
                            
        df = pd.DataFrame(self.data_dict)
        if self.config_dict['export_folder'] == '':
            df.to_csv(os.path.join(self.config_dict['project_path'],'Feedermetrics.csv'))

        else: 
            df.to_csv(os.path.join(self.config_dict['export_folder'],'Feedermetrics.csv'))

        self.logger.info(f"{os.path.join(self.config_dict['export_folder'],'Feedermetrics.csv')} \
            exported successfully")
    
    
    def compute_dt_metric(self):

        self.col_names = ['Date','DTName','PVPenetration','Avg2Peak','PeakReduction',\
                'EnergyReduction','MaxRampRate']
        self.data_dict = {key:[] for key in self.col_names}
    
        for dt_name in self.dtnames:
            for year in self.config_dict['year_list']:
                self.logger.info(f"Metric being exported for transformer {dt_name} for year {year}")
                for month in range(1,13,1):
                    net_load, net_load_highres = self.data_handler.analyze_dt\
                            (dt_name,year,'Monthly',dt(year,month,1,0,0,0))
                    
                    if net_load != None:
                    
                        solarmultiplier = self.data_handler.return_solar_multiplier\
                            (dt(year,month,1),'Monthly')
                        
                        pv_gen, pv_gen_highres = self.data_handler.dt_pv_profile(dt_name,\
                            dt(year,month,1,0,0,0), 'Monthly')
                        
                        if pv_gen != None:
                            baseload_highres = [sum(x) for x in zip(net_load_highres,pv_gen_highres)] 
                        else:
                            baseload_highres = net_load_highres
                    
                        baseload_highres_filternan = [el for el in baseload_highres if not math.isnan(el)]
                        
                        for pv_penetration in range(0,101,10):
                            if baseload_highres_filternan == []:
                                self.data_dict['Avg2Peak'].append(None)
                                self.data_dict['PeakReduction'].append(None)
                                self.data_dict['EnergyReduction'].append(None)
                                self.data_dict['MaxRampRate'].append(None)
                            else:
                                load_with_pv = [el-max(baseload_highres)*pv_penetration*solarmultiplier[id]/100 \
                                    for id,el in enumerate(baseload_highres) if not math.isnan(el)]
                                load_with_pv_abs = [abs(el) for el in load_with_pv]
                                
                                self.data_dict['Avg2Peak'].append(sum(load_with_pv)/\
                                    (len(load_with_pv_abs)*max(load_with_pv_abs)))

                                self.data_dict['PeakReduction'].append( (max(baseload_highres) \
                                    - max(load_with_pv_abs))*100/max(baseload_highres) )
                                
                                self.data_dict['EnergyReduction'].append((sum(baseload_highres_filternan)\
                                    -sum(load_with_pv))*100/sum(baseload_highres_filternan)
                                    )
                                ramprate = [load_with_pv[i+1]-load_with_pv[i] \
                                    for i in range(len(load_with_pv)-1)]
                                self.data_dict['MaxRampRate'].append(max(ramprate))

                            self.data_dict['PVPenetration'].append(str(pv_penetration)+'%')
                            self.data_dict['DTName'].append(dt_name)
                            self.data_dict['Date'].append(dt(year,month,1))
                    
                    else:
                        for pv_penetration in range(0,101,10):
                            self.data_dict['Avg2Peak'].append(None)
                            self.data_dict['PeakReduction'].append(None)
                            self.data_dict['EnergyReduction'].append(None)
                            self.data_dict['MaxRampRate'].append(None)
                            self.data_dict['PVPenetration'].append(str(pv_penetration)+'%')
                            self.data_dict['DTName'].append(dt_name)
                            self.data_dict['Date'].append(dt(year,month,1))


        df = pd.DataFrame(self.data_dict)
        if self.config_dict['export_folder'] == '':
            df.to_csv(os.path.join(self.config_dict['project_path'],'DTmetrics.csv'))

        else: 
            df.to_csv(os.path.join(self.config_dict['export_folder'],'DTmetrics.csv'))
        
        self.logger.info(f"{os.path.join(self.config_dict['export_folder'],'DTmetrics.csv')} \
            exported successfully")

if __name__ == '__main__':

    a = Metric(r'src//solar_metrics//config.json')
   #a.compute_dt_metric()
    a.compute_feeder_metric()






