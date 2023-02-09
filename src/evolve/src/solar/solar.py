#third_party imports
from cerberus import Validator
import pandas as pd
from timezonefinder import TimezoneFinder
import pvlib
from matplotlib import pyplot as plt

#local imports
from validation import (
    irradiance_dataframe_validation,
    solar_parameters_validation,
    inverter_parameters_validation
)

class SolarPV:

    def __init__(self, solar_parameters: dict, inverter_parameters: dict, irradiance_parameters: dict):
        
        self.results={'solar_output_kw': []}

        self.irradiance_parameters=irradiance_parameters
        self.irradiance_file_path=irradiance_parameters['irradiance_file_path']
        if self.irradiance_file_path != '':
            self.irradiance_dataframe=pd.read_csv(self.irradiance_file_path).fillna(value=0)

        self.start_time=irradiance_parameters['start']
        self.end_time=irradiance_parameters['end']
        self.resolution=str(irradiance_parameters['resolution_mins'])+'min'

        self.solar_parameters=solar_parameters
        self.pv_location=solar_parameters['pv_location'] #(lat,long)
        self.pv_kva_nameplate=solar_parameters['kva'] 
        self.tracking_type=solar_parameters['tracking_type'] #'fixed_axis', 'single_axis', 'dual_axis'
        self.fixed_axis_surface_tilt=solar_parameters['fixed_axis_surface_tilt']
        self.fixed_axis_surface_azimuth=solar_parameters['fixed_axis_surface_azimuth']
        self.single_axis_axis_tilt=solar_parameters['single_axis_axis_tilt']
        self.single_axis_axis_azimuth=solar_parameters['single_axis_axis_azimuth']
        self.single_axis_max_tilt=solar_parameters['single_axis_max_tilt']
        self.dual_axis_max_tilt=solar_parameters['dual_axis_max_tilt']
        
        self.inverter_parameters=inverter_parameters
        self.inverter_sizing_ratio=inverter_parameters['inverter_sizing_ratio']
        self.inverter_temp_coeff=inverter_parameters['inverter_temp_coeff']

        print('Validating Data Inputs...')
        self.validate_data_inputs()
        print('Running Simulation...')
        self.simulate()
    
    def get_results(self):
        self.results['solar_output_kw']=self.ac_output
        return self.results
    
    def plot_results(self,solar_ac_output:bool=False,solar_dc_output:bool=False,irradiance:bool=False):
        if solar_ac_output:
            ac_list=self.ac_output.AC_Output.values.tolist()
            timesteps=self.ac_output.index.values.tolist()
            xticks=timesteps[0::4]
            plt.plot(timesteps,ac_list, label='AC_kW')
            plt.axhline(y=self.pv_kva_nameplate, label=f"Solar System Nameplate: {self.pv_kva_nameplate} kVA", linestyle='--')
            plt.title('Solar Output')
            plt.xticks(xticks,rotation=90)
            plt.ylabel('kW')
            plt.xlabel('timestep')
            
        if solar_dc_output:
            dc_list=self.dc_output.DC_Output.values.tolist()
            timesteps=self.dc_output.index.values.tolist()
            xticks=timesteps[0::4]
            plt.plot(timesteps,dc_list, label='DC_kW')

        plt.legend()
        plt.show()
        
        if irradiance:
            if self.tracking_type == 'fixed':
                poa_list=self.fixed_poa.poa_direct.values.tolist()
            elif self.tracking_type == 'single_axis':
                poa_list=self.single_axis_poa.poa_direct.values.tolist()
            elif self.tracking_type == 'dual_axis':
                poa_list=self.dual_axis_poa.poa_direct.values.tolist()
            dni_list=self.irradiance_dataframe.dni.values.tolist()
            ghi_list=self.irradiance_dataframe.ghi.values.tolist()
            dhi_list=self.irradiance_dataframe.dhi.values.tolist()
            plt.plot(timesteps,poa_list, label="POA")
            plt.plot(timesteps,dni_list, label='dni')
            plt.plot(timesteps,ghi_list, label='ghi')
            plt.plot(timesteps,dhi_list, label='dhi')
            plt.title('Irradiance Values (W/m^2)')
            plt.xticks(xticks,rotation=90)
            plt.legend()
        
        plt.show()
    
    def validate_data_inputs(self):
        irradiance_dataframe_validation(
            irradiance_input_dict=self.irradiance_parameters)
        solar_parameters_validation(self.solar_parameters)
        inverter_parameters_validation(self.inverter_parameters)
    
    def format_times(self):
        #outputs times from irradiance data in pd datetimeIndex and adds on timezone
        tf = TimezoneFinder()
        tzone = tf.timezone_at(lng=self.pv_location[1], lat=self.pv_location[0])
        self.irradiance_dataframe['DateTime']=pd.DatetimeIndex(
            pd.to_datetime(self.irradiance_dataframe['Date']+' '+self.irradiance_dataframe['Time']),
            tz=tzone
            )
        self.irradiance_dataframe.drop(
            ['Date','Time'],
             axis=1
             ,inplace=True)
    
    def get_solar_location(self):
        #gets solar location and adds the apparent zenith and azimuth to irrad data
        solar_position=pvlib.solarposition.get_solarposition(
            self.irradiance_dataframe.index,
            self.pv_location[0],
            self.pv_location[1])
        self.irradiance_dataframe['apparent_zenith']=solar_position.apparent_zenith
        self.irradiance_dataframe['azimuth']=solar_position.azimuth
        self.irradiance_dataframe.fillna(value=0,inplace=True)

    def add_temperature_data(self):
        if 'temp' not in self.irradiance_dataframe.columns:
            print('No temp data provided. Using 25 deg C for inverter environment')
            self.irradiance_dataframe['temp']=25.0

    def get_irradiance_from_csv(self): #create and format irradiance dataframe from a csv file
        self.format_times() #create datetimes and add correct timezone for the solar location
        self.irradiance_dataframe.set_index('DateTime', drop=True,inplace=True) #sets datetime as the dataframe index
        self.get_solar_location() #gets location of pv system and adds solar zenith and azimuth to dataframe
        self.add_temperature_data()
    
    def create_datetimes_for_clearsky(self):
        tf = TimezoneFinder()
        tzone = tf.timezone_at(
            lng=self.pv_location[1],
             lat=self.pv_location[0]
             )
        self.times = pd.date_range(
            self.start_time,
            self.end_time, 
            freq=self.resolution,
            tz=tzone
            )

    def get_clearsky_irradiance(self):#if no irradiance data provided, get clearsky irradiance using pvlib
        loc=pvlib.location.Location(self.pv_location[0],self.pv_location[1])
        self.create_datetimes_for_clearsky()
        self.irradiance_dataframe=loc.get_clearsky(self.times)
        self.get_solar_location()
        self.irradiance_dataframe.index.name='DateTime'
        self.add_temperature_data()

    def get_poa_fixed(self):
        self.fixed_poa=pd.DataFrame(pvlib.irradiance.get_total_irradiance(
            surface_tilt=self.fixed_axis_surface_tilt,
            surface_azimuth=self.fixed_axis_surface_azimuth,
            solar_zenith=self.irradiance_dataframe['apparent_zenith'],
            solar_azimuth=self.irradiance_dataframe['azimuth'],
            dni=self.irradiance_dataframe['dni'],
            ghi=self.irradiance_dataframe['ghi'],
            dhi=self.irradiance_dataframe['dhi']
            ),index=self.irradiance_dataframe.index).merge(
                self.irradiance_dataframe['temp'],on='DateTime')

    def get_poa_single_axis(self):
        self.single_axis_tracking_data=pd.DataFrame(pvlib.tracking.singleaxis(
            apparent_zenith=self.irradiance_dataframe['apparent_zenith'],
            apparent_azimuth=self.irradiance_dataframe['azimuth'], 
            axis_tilt=self.single_axis_axis_tilt,
            axis_azimuth=self.single_axis_axis_azimuth,
            max_angle=self.single_axis_max_tilt,
            backtrack=False
            ),index=self.irradiance_dataframe.index).fillna(value=0)

        self.single_axis_poa=pd.DataFrame(pvlib.irradiance.get_total_irradiance(
            surface_tilt=self.single_axis_tracking_data['surface_tilt'],
            surface_azimuth=self.single_axis_tracking_data['surface_azimuth'],
            solar_zenith=self.irradiance_dataframe['apparent_zenith'],
            solar_azimuth=self.irradiance_dataframe['azimuth'],
            dni=self.irradiance_dataframe['dni'],
            ghi=self.irradiance_dataframe['ghi'],
            dhi=self.irradiance_dataframe['dhi'], model='haydavies',dni_extra=0
            ), index=self.irradiance_dataframe.index).merge(
                self.irradiance_dataframe['temp'],on='DateTime').fillna(value=0)

    def get_poa_dual_axis(self):
        tracking_dict={}
        for index, row in self.irradiance_dataframe.iterrows():
            tracking_dict[index]={}
            if row['apparent_zenith']<=90:
                #if sun is above horizon
                tracking_dict[index]['surface_azimuth']=row['azimuth']
                if row['apparent_zenith'] <=self.dual_axis_max_tilt:
                    tracking_dict[index]['surface_tilt']=row['apparent_zenith']
                    
                else:
                    tracking_dict[index]['surface_tilt']=self.dual_axis_max_tilt
            else:
                tracking_dict[index]['surface_azimuth']=0
        self.dual_axis_tracking_data=pd.DataFrame.from_dict(tracking_dict,orient='index')

        self.dual_axis_poa=pd.DataFrame(pvlib.irradiance.get_total_irradiance(
            surface_tilt=self.dual_axis_tracking_data['surface_tilt'],
            surface_azimuth=self.dual_axis_tracking_data['surface_azimuth'],
            solar_zenith=self.irradiance_dataframe['apparent_zenith'],
            solar_azimuth=self.irradiance_dataframe['azimuth'],
            dni=self.irradiance_dataframe['dni'],
            ghi=self.irradiance_dataframe['ghi'],
            dhi=self.irradiance_dataframe['dhi'], model='haydavies',dni_extra=0
            ), index=self.irradiance_dataframe.index).merge(
                self.irradiance_dataframe['temp'],on='DateTime').fillna(value=0)

    def get_inverter_output(self, poa_irradiance):

        self.dc_output=pd.DataFrame(pvlib.pvsystem.pvwatts_dc(
            g_poa_effective=poa_irradiance['poa_direct'],
            temp_cell=poa_irradiance['temp'],
            pdc0=self.pv_kva_nameplate,
            gamma_pdc=self.inverter_temp_coeff,
            temp_ref=25.0
            ),index=poa_irradiance.index)
        self.dc_output.columns=['DC_Output']

        self.ac_output=pd.DataFrame(pvlib.inverter.pvwatts(
            pdc=self.dc_output,
            pdc0=self.pv_kva_nameplate*self.inverter_sizing_ratio,
            eta_inv_nom=0.96,
            eta_inv_ref=0.9637
            ),index=poa_irradiance.index)
        self.ac_output.columns=['AC_Output']

    def simulate(self):

        #get or create irradiance data
        if self.irradiance_file_path != '':
            print('\nUsing supplied irradiance data to model solar...')
            self.get_irradiance_from_csv()

        else:
            print('\nNo irradiance data supplied. Getting clearsky irradiance...')
            self.create_datetimes_for_clearsky()
            self.get_clearsky_irradiance()
        
        if self.tracking_type == 'fixed':
            self.get_poa_fixed()
            self.get_inverter_output(self.fixed_poa)
        elif self.tracking_type == 'single_axis':
            self.get_poa_single_axis()
            self.get_inverter_output(self.single_axis_poa)
        elif self.tracking_type == 'dual_axis':
            self.get_poa_dual_axis()
            self.get_inverter_output(self.dual_axis_poa)
                     
