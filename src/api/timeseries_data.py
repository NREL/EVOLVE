""" Module for managing time series data for EVOLVE api."""

# Standard imports
import uuid
import os
import datetime
from pathlib import Path

# third-party imports
import polars
import pandas as pd
from pydantic import BaseModel
import numpy as np
from dotenv import load_dotenv
from fastapi import HTTPException, status

# internal imports
import models

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')

class TSFormInput(BaseModel):
    timestamp: str
    resolution: float
    category: str
    description: str


async def post_notification(username: str, message: str):

    not_obj = models.Notifications(
        user= await models.Users.get(username=username),
        message = message,
        archived = False,
        visited  = False
    )
    await not_obj.save()

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
        # df  =pd.read_csv(file.file, parse_dates=[metadata.timestamp])
        df = polars.read_csv(file.file, parse_dates=True)

    except Exception as e:
        await post_notification(username, 
        f"Wrong column name and/or unrecognized input! : `{file.filename}`")

        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail=f"Unrecognized input!"
    )

    # Do some validation on dataframe 
    # If not valid throw exception

    try:
        diff_timestamps = df.select(polars.col(metadata.timestamp).diff(null_behavior='drop'))
    except Exception as e:
        await post_notification(username, 
        f"Wrong column name passed : `{file.filename}` column passed is `{metadata.timestamp}`")

        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail=f"Unrecognized input!")

    if len(diff_timestamps.filter(polars.col(metadata.timestamp)==datetime.timedelta(minutes=metadata.resolution))) \
        != len(diff_timestamps):

        await post_notification(username, 
        f"Specified time resolution does not match! `{file.filename}`")

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=f"Specified time resolution does not match!"
        )
    

    # Now that the data is valid let's upload data to databases
    user = await models.Users.get(username=username)
    ts_pydantics = []


    # Let's save files
    column_names = list(df.columns)
    timeseries_data_path = Path(DATA_PATH) / username / 'timeseries_data'
    if not timeseries_data_path.exists():
        timeseries_data_path.mkdir(parents=True)

    tagging_dict = {}
    if metadata.category != 'irradiance':
        for column in column_names:
            # Save each column data into separate csv files
            if column != metadata.timestamp:
                data_uuid = str(uuid.uuid4())
                tagging_dict[column] = data_uuid
                df.select([polars.col(column), polars.col(metadata.timestamp)]).rename(
                    {column: metadata.category, metadata.timestamp: 'timestamp'}
                ).write_csv(
                    timeseries_data_path / (data_uuid + '.csv')
                )

    else:
        data_uuid = str(uuid.uuid4()) 
        tagging_dict = {file.filename.split('.')[0]: data_uuid} 
        df.write_csv(
            timeseries_data_path / (data_uuid + '.csv')
        )

    for name, uuid_ in tagging_dict.items():
        data_model = models.TimeseriesData(
            user=user,
            start_date= df.select(polars.col(metadata.timestamp)).min()[0,0],
            end_date=df.select(polars.col(metadata.timestamp)).max()[0,0],
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
    
    await post_notification(username, 
        f"Uploaded successfully `{file.filename}`")
    return ts_pydantics

    


