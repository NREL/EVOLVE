from typing import List 
from pathlib import Path
import os

from fastapi import (APIRouter, HTTPException, status, Depends,
    File, Form)
from fastapi.responses import FileResponse
from dotenv import load_dotenv

import models
from custom_models import DataCommentResponseModel, DataCommentInput
from dependencies.dependency import get_current_user
import timeseries_data

load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=List[models.ts_pydantic])
async def get_timeseries_data(user: models.user_pydantic = Depends(get_current_user)):
    """ Get a list of data items for a user. """  

    ts_data = await models.TimeseriesData.all().filter(
        user=await models.Users.get(username=user.username)
    )
    if ts_data:
        ts_data_pydantic = [await models.ts_pydantic.from_tortoise_orm(data) for data in ts_data]
        return ts_data_pydantic

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

@router.get('/{data_id}/comments', response_model=List[DataCommentResponseModel])
async def get_comments_for_data(data_id:int, user: models.user_pydantic = Depends(get_current_user)):
    """ Get all the comments for given data id."""

    ts_data = await models.TimeseriesData.get(id=data_id).prefetch_related(
        'user__user'
    )
    if ts_data.user.username != user.username:
        
        # If the user is not owner make sure the data is shared with this user
        shared_user = await models.Users.get(username=user.username)
        try:
            await models.UserSharedTimeSeriesData.get(
                id=data_id, 
                user=shared_user
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized access!')
    
    comments = await models.DataComments.filter(
        timeseriesdata=await models.TimeseriesData.get(id=data_id)
    ).prefetch_related('user__user')

    comment_objs = []
    for comment in comments:
        comment_dict = dict(comment)
        comment_dict.update({'username': comment.user.username})
        comment_objs.append(
            DataCommentResponseModel(**comment_dict)
        )
   
    return comment_objs

@router.get('/{data_id}/users')
async def get_shared_users(
    data_id: int,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Get a list of shared user for a data by id"""
    parent_data = await models.TimeseriesData.get(id=data_id)

    if parent_data.username != user.username:
        shared_user = await models.UserSharedTimeSeriesData.get(
            timeseries_data=await models.TimeseriesData.get(id=shared_data.id), 
            user=await models.Users.get(username=shared_user.username)
        )
    
    shared_data = await models.UserSharedTimeSeriesData.all().filter(
        timeseries_data=await models.TimeseriesData.get(id=data_id)
    )
    if shared_data:
        shared_data_pydantic = [await models.user_shared_ts_data_pydantic.from_tortoise_orm(data) \
             for data in shared_data]
        return [d.username for d in shared_data_pydantic] + [parent_data.username]
    


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

@router.post('/{data_id}/comments', response_model=models.data_comments_pydantic)
async def create_data_comment(
    comment: DataCommentInput,
    data_id: int,
    user: models.user_pydantic = Depends(get_current_user)):

    """ Create a comment for given data id"""
    comment_obj = models.DataComments(
        timeseriesdata = await models.TimeseriesData.get(id=data_id),
        user=await models.Users.get(username=user.username),
        comment=comment.comment,
        edited=False
    )
    await comment_obj.save()
    return await models.data_comments_pydantic.from_tortoise_orm(comment_obj)

@router.post('/{data_id}/share/{username}')
async def share_data_with_user(
    data_id: int,
    username: str,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Create shared relation for a data """
    shared_user = await models.Users.get(username=username)
    shared_data = await models.TimeseriesData.get(id=data_id)

    if shared_data.username != user.username:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")
    
    usr_shared = models.UserSharedTimeSeriesData(
        timeseries_data=await models.TimeseriesData.get(id=shared_data.id),
        user=await models.Users.get(username=shared_user.username),
    )

    await usr_shared.save()
    return await models.user_shared_ts_data_pydantic.from_tortoise_orm(
        usr_shared
    )



@router.put('/{data_id}/comments/{comment_id}', response_model=models.data_comments_pydantic)
async def get_comments_for_data(
    data_id:int, 
    comment_id: int,
    updated_comment: DataCommentInput,
    user: models.user_pydantic = Depends(get_current_user)):
    """ Edit comment by data id and comment id. """
    comment = await models.DataComments.get(
        timeseries_data=await models.TimeseriesData.get(id=data_id), 
        id=comment_id, 
        user=await models.Users.get(username=user.username)
    )
    comment.comment = updated_comment.comment
    comment.edited = True
    await comment.save()
    return await models.data_comments_pydantic.from_tortoise_orm(comment)



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_ts_data(id: int, user: models.user_pydantic = Depends(get_current_user)):
    """ Delete a data object by id for a user. """

    ts_data = await models.TimeseriesData.get(
        id=id, 
        user=await models.Users.get(username=user.username)
    )
    file_name = ts_data.filename + '.csv'
    file_path = Path(DATA_PATH) / user.username / 'timeseries_data' / file_name
    await ts_data.delete()
    file_path.unlink(missing_ok=True)


@router.delete('/{data_id}/comments/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_comments_for_data(
    data_id:int, 
    comment_id: int,
    user: models.user_pydantic = Depends(get_current_user)):

    """ Delete comment by comment id and data id."""
    comment = await models.DataComments.get(
        timeseries_data=await models.TimeseriesData.get(id=data_id), 
        id=comment_id, 
        user=await models.Users.get(username=user.username)
    )
    await comment.delete()

