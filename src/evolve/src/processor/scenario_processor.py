""" Module for handling RABBIT MQ Queue message."""

# Manage python standard imports
from typing import Dict, List
from pathlib import Path
import os
import datetime
import traceback

# Third-party imports
import psycopg2
from dotenv import load_dotenv
import polars
import numpy as np


# Internal imports
from input_config_model import InputConfigModel, ESFormData
from battery import GenericBattery, GenericBatteryParams
from batery_timed_strategy import TimeBasedCDStrategyInputModel, TimeBasedCDStrategy


load_dotenv()

DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': str(os.getenv("DB_PORT")),
    'database': os.getenv("DB_NAME")
}
DATA_PATH = os.getenv('DATA_PATH')


class PostGresDB:
    """ Class for managing interaction with PostGres DB. """
    
    def __init__(self,
        db_config: Dict
    ):
        """ Constructor for DB.

        e.g. db_config = {
            user: str, 
            password: str, 
            host: str, 
            port: str, 
            database: str
        }
        
        """
        self.connection = psycopg2.connect(**db_config)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.connection.close()
    

def populate_sliced_category(df:polars.DataFrame):

    start_date = df.select(polars.col('timestamp')).min()[0,0]
    end_date = df.select(polars.col('timestamp')).max()[0,0]
    duration_hr = (end_date - start_date).total_seconds()/3600

    # Data is more than one month makes sense to aggregate by months
    if duration_hr >= 960:
        format_code = '%b'
    elif duration_hr < 960 and duration_hr >168:
        format_code = '%W'
    elif duration_hr <=168 and duration_hr >24:
        format_code ='%a'
    elif duration_hr < 24:
        format_code='%I %p'
    else:
        format_code = '%Y'
        
    return df.with_column(polars.col('timestamp').apply(lambda x: x.strftime(format_code)).alias('category'))


def compute_energy_metric(df:polars.DataFrame,  resolution: int, column_name='kW'):
    """ Compute energy for different category """

    df = populate_sliced_category(df)
    
    import_df = df.filter(polars.col(column_name)>0).groupby("category").agg(polars.col(column_name).sum()).with_column(
        (polars.col(column_name)*resolution/60).alias('import_kWh')
    ).select(['import_kWh', 'category'])

    export_df = df.filter(polars.col(column_name)<=0).groupby("category").agg(polars.col(column_name).sum()).with_column(
        (polars.col(column_name)*resolution/60).alias('export_kWh')
    ).select(['export_kWh', 'category'])

    return import_df.join(export_df, on="category", how="left")


def compute_max_power(df:polars.DataFrame, column_name='kW'):
    """ Compute max power """

    df = populate_sliced_category(df)
    
    import_df = df.filter(polars.col(column_name)>0).groupby("category").agg(polars.col(column_name).max()).with_column(
        (polars.col(column_name)).alias('import_peak_kW')
    ).select(['import_peak_kW', 'category'])

    export_df = df.filter(polars.col(column_name)<=0).groupby("category").agg(polars.col(column_name).max()).with_column(
        (polars.col(column_name)).alias('export_peak_kW')
    ).select(['export_peak_kW', 'category'])

    return import_df.join(export_df, on="category", how="left")

def update_report_status(id:int, status:str):
    with PostGresDB(DB_CONFIG) as cursor:
        cursor.execute(
            f"""update reportmetadata 
                set status=%s""", [status]
        )

def compute_base_load_metrics(load_df:polars.DataFrame, resolution:int, base_path:str ):
    
    base_load_energy_df = compute_energy_metric(load_df, resolution)
    base_load_power_df = compute_max_power(load_df)

    load_df.write_csv(base_path / 'base_load.csv')
    base_load_energy_df.write_csv(base_path / 'base_load_energy_metrics.csv')
    base_load_power_df.write_csv(base_path / 'base_load_peak_power_metrics.csv')

def default_discharge_func(time_: float):

    dischargecurve = np.polyfit(
        [0,24, 720],
        [0,5,7],
    2)

    return (dischargecurve[0]**2)*time_ + dischargecurve[1]*time_ \
                            + dischargecurve[2]


def timw2num(time_str: str):
    return int(time_str.split(' ')[0]) + 12 if 'PM' in time_str else 0

def process_time_based_es(
    battery: ESFormData,
    timestamps: List[datetime.datetime]
):
    """ Process a single battery. """

    battery_params = GenericBatteryParams(
            maximum_dod=battery.esPowerCapacity,
            energy_capacity_kwhr=battery.esEnergyCapacity,
            initial_soc=0.5,
            discharge_func=default_discharge_func
    )

    battery_instance = GenericBattery(battery_params)
    timecdmodel = TimeBasedCDStrategyInputModel(
        charging_hours=[timw2num(el) for el in battery.chargingHours],
        discharging_hours=[timw2num(el) for el in battery.disChargingHours],
        c_rate=0.25
    )

    time_based_cd_instance = TimeBasedCDStrategy(
        config=timecdmodel
    )

    time_based_cd_instance.simulate(
        timestamps,
        battery_instance
    )

    return {
        'battery_power': [round(el, 3) for el in battery_instance.battery_power_profile],
        'battery_soc': [round(el,3) for el in battery_instance.battery_soc_profile]
    }
    

def process_energy_storage(
    batteries: List[ESFormData],
    load_df: polars.DataFrame
):
    """ Simulates battery. """

    battery_output = {}

    for battery in batteries:
        if battery.esStrategy == 'time':
            battery_output[battery.name] = process_time_based_es(
                battery, load_df['timestamp'].to_list())

    return battery_output
            


def process_scenario(
    input_config: InputConfigModel,
):
    """ Takes a full scenario json and simulates a scenario. 
    
    Args
        input_config (Dict): Scenario JSON content along with
            report metadata.
    """
    
    # Update the status
    update_report_status(input_config.id, 'RUNNING')

    base_path = Path(DATA_PATH) / input_config.username / 'reports_data' / str(input_config.id)
    if not base_path.exists():
        base_path.mkdir(parents=True)

    try:
        load_df = get_load_df(
            input_config.data.basic.loadProfile,
            input_config.data.basic.startDate,
            input_config.data.basic.endDate,
            input_config.data.basic.resolution,
            input_config.data.basic.dataFillingStrategy
        )
        load_df = load_df.sort(by='timestamp')
        compute_base_load_metrics(load_df, input_config.data.basic.resolution, base_path)
        
        if input_config.data.energy_storage:
            battery_output = process_energy_storage(
                input_config.data.energy_storage, load_df
            )
            battery_power_df = polars.from_dict({bname: bdict['battery_power'] \
                for bname, bdict in battery_output.items()})
            battery_soc_df =  polars.from_dict({bname: bdict['battery_soc'] \
                for bname, bdict in battery_output.items()})

            battery_power_df.write_csv(base_path / 'battery_power_timeseries.csv')
            battery_soc_df.write_csv(base_path / 'battery_soc_timeseries.csv')

        
        update_report_status(input_config.id, 'COMPLETED')


    except Exception as e:
        with (base_path / 'error.txt') as fp:
            fp.writelines(str(e))
        print(e)
        update_report_status(input_config.id, 'ERROR')


def upsample_interpolate_df(df:polars.DataFrame, resolution: int):
    return df.upsample('timestamp', every=f"{resolution}m").interpolate().fill_null("forward")

def upsample_staircase_df(df:polars.DataFrame, resolution: int):
    return df.upsample('timestamp', every=f"{resolution}m").select(polars.all().forward_fill())

def downsample_df(df:polars.DataFrame, resolution: int, column_name: str):
    return df.groupby_dynamic('timestamp', every=f"{resolution}m").agg(
            polars.col(column_name).mean()
        )

def filter_by_date(df:polars.DataFrame, start_date: datetime.date, end_date: datetime.date):
    return df.filter(
        (polars.col('timestamp') > start_date) & \
        (polars.col('timestamp') < end_date)
    )


def get_load_df(
    load_id: int,
    start_date: str, 
    end_date: str,
    resolution: int,
    strategy: str,
):

    """ Returns a polars dataframe."""
    file_owner, filename, data_res = get_file_name_from_id(load_id)
    file_path = Path(DATA_PATH) / file_owner / 'timeseries_data' /(filename + '.csv')

    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist!")

    df = filter_by_date(
            polars.read_csv(file_path, parse_dates=True), start_date, end_date
    )

    if data_res <= resolution:
        return downsample_df(df, resolution, 'kW')
    else:
        return {
            'interpolation': upsample_interpolate_df,
            'staircase': upsample_staircase_df
        }.get(strategy)(df, resolution)



def get_file_name_from_id(id:int):
    """ Get the filename. """

    with PostGresDB(DB_CONFIG) as cursor:
        cursor.execute(
            f"""select users.username, timeseriesdata.filename, timeseriesdata.resolution_min 
                from timeseriesdata 
                inner join users 
                on timeseriesdata.user_id = users.id
                where timeseriesdata.id=%s""", [id]
        )
        record = cursor.fetchone()
    return record


if __name__ == '__main__':
    
    import json
    import pydantic 
    with open(r"C:\Users\KDUWADI\Desktop\NREL_Projects\TUNISIA\data\evolve_data_post\jake\reports\12.json", "r") as fp:
        json_content = json.load(fp)

    input_config = {
        "id": 12,
        "username": "jake",
        "data": json_content
    }

    input_config_pydantic= pydantic.parse_obj_as(InputConfigModel, input_config)
    process_scenario(input_config_pydantic)





