""" Module for managing time series data for EVOLVE api."""

# Standard imports
import io
from pathlib import Path
import uuid
import os

# third-party imports
import pandas as pd
from pydantic import BaseModel
import numpy as np
from dotenv import load_dotenv
from fastapi import HTTPException, status

# internal imports
import models
from influxdb.influx_client import InfluxDBClient, InfluxDBConfigModel

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')

class TSFormInput(BaseModel):
    timestamp: str
    resolution: float
    category: str
    description: str


async def handle_timeseries_data_upload(
    file,
    metadata: TSFormInput,
    username: str
):
    """ Function to manage upload of files. """

    # Checking to see if I can read the file
    # Otherwise throw exceptipn

    try:
        # io.BytesIO(input_csv_bytes)
        df = pd.read_csv(file.file,
            encoding='utf-8', index_col=metadata.timestamp, parse_dates=True)
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail=f"Wrong column name and/or unrecognized input!"
    )


    # Do some validation on dataframe 
    # If not valid throw exception
    df = df.sort_index()
    all_timestamps = list(df.index)
    diff_timestamps = np.array(all_timestamps[1:])  - np.array(all_timestamps[:-1])
    if not all(diff_timestamps == np.timedelta64(int(metadata.resolution), 'm')):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=f"Specified time resolution does not match!"
        )
    

    # Now that the data is valid let's upload data to databases
    user = await models.Users.get(username=username)
    ts_pydantics = []


    # First upload data to TimeSeries Database
    db_instance = InfluxDBClient(config=InfluxDBConfigModel(
        org=os.getenv('INFLUXDB_ORG'),
        token=os.getenv('INFLUXDB_TOKEN'),
        url=os.getenv('INFLUXDB_URL'),
        bucket=os.getenv('INFLUXDB_BUCKET')
    ))

    # Let's save files
    column_names = list(df.columns)
    df.index = pd.to_datetime(df.index, unit='s')

    if metadata.category != 'irradiance':

        tagging_dict = {}
        for column in column_names:

            # Save each column data into separate csv files
            data_uuid = str(uuid.uuid4())
            tagging_dict[column] = data_uuid

    else: 
        tagging_dict = str(uuid.uuid4())

    db_instance.insert_dataframe(
        df,
        username,
        tagging_dict,
        metadata.category
    )


    # Now insert metadata in SQL database
    if isinstance(tagging_dict, str):
        tagging_dict  = {file.filename.split('.')[0]: tagging_dict}   

    for name, uuid_ in tagging_dict.items():
        data_model = models.TimeseriesData(
            user=user,
            start_date= all_timestamps[0].to_pydatetime(),
            end_date= all_timestamps[-1].to_pydatetime(),
            resolution_min=metadata.resolution,
            name=name,
            description=metadata.description,
            filename=uuid_,
            image=uuid_,
            category=metadata.category
        )

        
        await data_model.save()
        data_pydantic = await models.ts_minimal.from_tortoise_orm(data_model)
        ts_pydantics.append(data_pydantic)
    
    db_instance.close_client()
    
    return ts_pydantics

    


