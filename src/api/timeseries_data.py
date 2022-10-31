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

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')

class TSFormInput(BaseModel):
    timestamp: str
    resolution: float
    category: str
    description: str



async def handle_timeseries_data_upload(
    input_csv_bytes: bytes,
    metadata: TSFormInput,
    username: str
):
    """ Function to manage upload of files. """

    try:
        df = pd.read_csv(io.BytesIO(input_csv_bytes),
            encoding='utf-8', index_col=metadata.timestamp, parse_dates=True)
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail=f"Wrong column name and/or unrecognized input!"
    )

    df = df.sort_index()
    all_timestamps = list(df.index)
    diff_timestamps = np.array(all_timestamps[1:])  - np.array(all_timestamps[:-1])
    user = await models.Users.get(username=username)

    timeseries_data_path = Path(DATA_PATH) / username / 'timeseries_data'
    if not timeseries_data_path.exists():
        timeseries_data_path.mkdir(parents=True)
 
    if all(diff_timestamps == np.timedelta64(int(metadata.resolution), 'm')) and timeseries_data_path.exists():

        
        ts_pydantics = []

        # Let's save files
        column_names = list(df.columns)
        for column in column_names:

            # Save each column data into separate csv files
            file_uuid = str(uuid.uuid4())
            column_df = df[column]
            column_df.to_csv(timeseries_data_path / (file_uuid + '.csv'))
            

            data_model = models.TimeseriesData(
                user=user,
                start_date= all_timestamps[0].to_pydatetime(),
                end_date= all_timestamps[-1].to_pydatetime(),
                resolution_min=metadata.resolution,
                name=column,
                description=metadata.description,
                filename=file_uuid,
                image=file_uuid,
                category=metadata.category
            )
            await data_model.save()
            data_pydantic = await models.ts_minimal.from_tortoise_orm(data_model)
            ts_pydantics.append(data_pydantic)
        
        return ts_pydantics

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail=f"Specified time resolution does not match!"
    )


