""" Module for handling communication with
Influx db database."""

# Standard imports
from typing import Union, Dict

# Third-party imports
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import pandas as pd 
from pydantic import BaseModel


class InfluxDBConfigModel(BaseModel):
    org: str 
    token: str
    url: str 
    bucket: str


class InfluxDBClient:
    """ Class for managing interactions with InfluxDB TimeSeries Database."""

    def __init__(self, config: InfluxDBConfigModel)-> None:

        self.config = config
        self.client = influxdb_client.InfluxDBClient(
            url=config.url,
            token=config.token,
            org=config.org,
            timeout=90000
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.delete_api = self.client.delete_api()
        self.query_api = self.client.query_api()

    def query_data(self,
            start: str,
            stop: str,
            measurement: str,
            username: str,
            tagname: str,
            fieldname: str,
            resolution: str,
        ):
        """ Query data for given timestamps. 
        
        e.g. resolution: 15m
        """

        query = f'''from(bucket: "{self.config.bucket}")
            |> range(start: {start}, stop: {stop})
            |> filter(fn:(r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) => r["user"] == "{username}")
            |> filter(fn: (r) => r["name"] == "{tagname}")
            |> filter(fn:(r) => r["_field"] == "{fieldname}")
            |> aggregateWindow(every: {resolution}, fn: mean)
            '''

        result = self.query_api.query(org=self.config.org, query=query)

        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_time(),record.get_value()))
        
        return results


    def delete_data(self,
        predicate: str,
        start: str = "1970-01-01T00:00:00Z",
        stop: str = "2100-01-01T00:00:00Z"
    ):
        """ Deletes data using predicate .
        e.g. '_measurement="kw" and "user"="kduwadi"',
        """
        self.delete_api.delete(
            start=start,
            stop=stop,
            predicate=predicate,
            bucket=self.config.bucket,
            org=self.config.org
            )

    def insert_dataframe(self, 
        df: pd.DataFrame, 
        username: str,
        tag_mapping: Union[str, Dict],
        measurement_name: str
    )-> None: 
        """ Take dataframe with single or multiple columns and
        inserts into timeseries database. 
        
        Args:
            df (pd.DataFrame): Timestamp indexed dataframe 
            username (str): Username to which data belongs to
            tag_mapping (str): Column name to tag name mapping. If tag_mapping 
                is a single string than all column values will be included in
                same point measurement. Useful for uploading irradiance data.
            measurement_name (str): Name of the measurement
        Note: 
        """

        data = []

        if isinstance(tag_mapping, dict):
            for column_name, tag_name in tag_mapping.items():
                sub_df = df[column_name].to_dict()
                for time, value in sub_df.items():
                    data.append(
                        influxdb_client.Point(measurement_name) \
                            .tag('user', username) \
                            .tag('name', tag_name) \
                            .field(measurement_name, float(value)) \
                            .time(time)
                    )

        elif isinstance(tag_mapping, str):
            for column_name in df.columns:
                sub_df = df[column_name].to_dict()
                for time, value in sub_df.items():
                    data.append(
                        influxdb_client.Point(measurement_name) \
                            .tag('user', username) \
                            .tag('name', tag_mapping) \
                            .field(column_name, float(value)) \
                            .time(time)
                    )

        if data:
            self.write_api.write(
                bucket=self.config.bucket, 
                org=self.config.org, 
                record=data
            )

    def close_client(self):
        self.client.close()


if __name__ == '__main__':



    # df = pd.read_csv(r'C:\Users\KDUWADI\Desktop\NREL_Projects\TUNISIA\data\sample_uploads\sample.csv',
    #     parse_dates=['timestamp']
    # )
    # df.set_index('timestamp', inplace=True)
    # df.index = pd.to_datetime(df.index, unit='s')

    df = pd.read_csv(r'C:\Users\KDUWADI\Desktop\NREL_Projects\TUNISIA\data\solar_data\solar_irradiance_processed.csv',
        parse_dates=['datetime'])
    df.set_index('datetime', inplace=True)
    df.index = pd.to_datetime(df.index, unit='s')

    db_instance = InfluxDBClient(config=InfluxDBConfigModel(org='NREL',
        token='5356bc92-b4e7-494c-bfcf-07684a090993',
        url='http://localhost:8086',
        bucket='evolve'
    ))

    # db_instance.insert_dataframe(
    #     df,
    #     'kduwadi',
    #     {'AIN EL GOSSE': '5356bc92-b4e7-494c-bfcf-07684a090995',
    #         'CRDA COURANT': '5356bc92-b4e7-494c-bfcf-07684a090996'
    #     },
    #     "kw"
    # )

    # db_instance.insert_dataframe(
    #     df,
    #     'kduwadi',
    #     '1234-abcd',
    #     "irradiance"
    # )

    db_instance.delete_data(
        '_measurement="irradiance" and "user"="kduwadi" and "name"="1234-abcd"'
    )


    import matplotlib.pyplot as plt 

    for resolution in ["5m"]: # "15m", "30m", "60m", "300m"
        results = db_instance.query_data(
            start="2019-01-01T00:00:00Z",
            stop="2019-01-02T00:00:00Z",
            measurement="irradiance",
            username="kduwadi",
            tagname="1234-abcd",
            fieldname="ghi",
            resolution=resolution
        )
        plt.plot([el[0] for el in results], [el[1] for el in results],label=resolution)

    plt.legend()
    plt.show()
    db_instance.close_client()

















