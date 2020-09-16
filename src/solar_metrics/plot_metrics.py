
"""
Used this script to generate plot of metrics for NREL-BYPL report
"""
# standard library imports
import os

# third-party imports
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt

datapath = r'C:\Users\KDUWADI\Desktop\NREL_Projects\BYPL-USAID\DashboardProject'
feeder_metric = 'Feedermetrics.csv'

# dt_data = pd.read_csv(r'C:\Users\KDUWADI\Desktop\NREL_Projects\BYPL-USAID\DashboardProject\SlotWiseEnergy.csv')    
# dt_data.columns = ['GRID','PANEL_NO','FEEDER_ID','GRID_NAME','FEEDER_NAME','SDO',
#                     'ZONE','FL_CODE','SSTN_NAME','DT_CODE','DT_KVA','METERNO','WH_ABS','DATE','MONTH',
#                     'MF','ENERGY(kwh)']
# dt_data_groupby =dt_data.groupby('DT_CODE')
# dt_data_ = dt_data_groupby.get_group('TG-PNR104A-1')
# plt.plot(range(len(dt_data_)), dt_data_['ENERGY(kwh)'].tolist())
# plt.show()


feeder_data = pd.read_csv(os.path.join(datapath, feeder_metric), parse_dates=['Date'])
mask = (feeder_data['Date'] >= dt(2016,5,1,0,0,0)) & (feeder_data['Date'] <= dt(2020,3,1,0,0,0))
feeder_data = feeder_data.loc[mask]

fig, axes = plt.subplots(3,1)

feeder_group = feeder_data.groupby('FeederName')
feeder_specific_data = feeder_group.get_group('HARGOVIND ENCLAVE')
sns.lineplot(data=feeder_specific_data, x = 'Date', y= 'Avg2Peak' , hue = 'PVPenetration', ax=axes[0] )
axes[0].set_ylabel('Monthly Average Power \n to Peak Power Ratio')
axes[0].set_xlabel('')
axes[0].set_title('Feeder 1')
#axes[0].set_xlim(dt(2016,5,1,0,0,0),dt(2020,3,1,0,0,0))
axes[0].get_xaxis().set_major_locator(mdates.MonthLocator(interval=6))
axes[0].get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(axes[0].get_xticklabels(), rotation=0, ha="right")
axes[0].legend(ncol=2)

feeder_specific_data = feeder_group.get_group('O/G -3  SOHAN SINGH GALI NO. 4')
g = sns.lineplot(data=feeder_specific_data, x = 'Date', y= 'Avg2Peak' , hue = 'PVPenetration', ax = axes[1] )
axes[1].set_ylabel('Monthly Average Power \n to Peak Power Ratio')
axes[1].set_xlabel('')
axes[1].set_title('Feeder 2')
axes[1].get_xaxis().set_major_locator(mdates.MonthLocator(interval=6))
axes[1].get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(axes[1].get_xticklabels(), rotation=0, ha="right")
axes[1].legend(ncol=2)


feeder_specific_data = feeder_group.get_group('VISHKARMA PARK')
g = sns.lineplot(data=feeder_specific_data, x = 'Date', y= 'Avg2Peak' , hue = 'PVPenetration', ax = axes[2] )
axes[2].set_ylabel('Monthly Average Power \n to Peak Power Ratio')
axes[2].set_xlabel('')
axes[2].set_title('Feeder 3')
axes[2].get_xaxis().set_major_locator(mdates.MonthLocator(interval=6))
axes[2].get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(axes[2].get_xticklabels(), rotation=0, ha="right")
axes[2].legend(ncol=2)

plt.show()




