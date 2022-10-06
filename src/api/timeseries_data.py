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

# internal imports
import models

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')

class TSFormInput(BaseModel):
    timestamp: str
    resolution: float
    category: str
    description: str

def create_ts_image(file_name:str, column_name: str):
    """ Create TS data image. """
    print('I am here!')

async def handle_timeseries_data_upload(
    input_csv_bytes: bytes,
    metadata: TSFormInput,
    user: models.user_pydantic,
):
    """ Function to manage upload of files. """

    df = pd.read_csv(io.BytesIO(input_csv_bytes),
        encoding='utf-8', index_col=metadata.timestamp, parse_dates=True)

    df = df.sort_index()
    all_timestamps = list(df.index)
    diff_timestamps = np.array(all_timestamps[1:])  - np.array(all_timestamps[:-1])

    timeseries_data_path = Path(DATA_PATH) / user.username / 'timeseries_data'
 
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
                username=user.username,
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


