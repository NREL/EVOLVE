from typing import List 
from pathlib import Path
import os

from fastapi import (APIRouter, HTTPException, status, Depends,
    File, Form)
from fastapi.responses import FileResponse
from dotenv import load_dotenv

import models
from dependencies.dependency import get_current_user
import timeseries_data
from custom_models import TimeSeriesDataResponseModel, SharedUserInfoModel

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=List[TimeSeriesDataResponseModel])
async def get_timeseries_data(user: models.user_pydantic = Depends(get_current_user)):
    """ Get a list of data items for a user. """  

    ts_data = await models.TimeseriesData.all().filter(
        user= await models.Users.get(username=user.username)
    ).prefetch_related('usr_shared_data')

    if ts_data:
        ts_data_updated = []
        
        for data in ts_data:
            data_to_dict = dict(data)
            shared_ts_data = list(data.usr_shared_data)

            shared_users = []
            for shtd in shared_ts_data:
                await shtd.fetch_related('user__user')
                shared_users.append(SharedUserInfoModel(
                    username=shtd.user.username,
                    shared_date=shtd.shared_date
                ))
            
            ts_data_updated.append(
                TimeSeriesDataResponseModel(**data_to_dict, shared_users=shared_users)
            )
        return ts_data_updated
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Items not found!'
    )

@router.get('/{id}/file')
async def get_data_for_download(id:int, user: models.user_pydantic = Depends(get_current_user)):
    """ Get a file to download by id"""

    ts_data = await models.TimeseriesData.get(
        id=id, 
        user=await models.Users.get(username=user.username)
    )
    file_name = ts_data.filename + '.csv'
    file_path = Path(DATA_PATH) / user.username / 'timeseries_data' / file_name
    return FileResponse(file_path)


@router.post('/upload', response_model=List[models.ts_minimal])
async def upload_timeseries_data(
    file: bytes = File(),
    metadata: str = Form(),
    user: models.user_pydantic = Depends(get_current_user),
):
    """ Create a data item for a user. """
    metadata_pydantic = timeseries_data.TSFormInput.parse_raw(metadata)
    response = await timeseries_data.handle_timeseries_data_upload(
        file, metadata_pydantic, user.username
    )
    return response



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_ts_data(id: int, user: models.user_pydantic = Depends(get_current_user)):
    """ Delete a data object by id for a user. """

    try:
        ts_data = await models.TimeseriesData.get(
            id=id, 
            user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")

    file_name = ts_data.filename + '.csv'
    file_path = Path(DATA_PATH) / user.username / 'timeseries_data' / file_name
    await ts_data.delete()
    file_path.unlink(missing_ok=True)



