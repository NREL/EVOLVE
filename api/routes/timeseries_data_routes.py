from typing import List
from pathlib import Path
import os

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    File,
    Form,
    BackgroundTasks,
    UploadFile,
)
from fastapi.responses import FileResponse
from dotenv import load_dotenv

import models
from dependencies.dependency import get_current_user
import timeseries_data
from custom_models import TimeSeriesDataResponseModel, SharedUserInfoModel

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


async def convert_ts_data_to_pydantic(ts_data: List):
    """Internal function to convert timeseries data to pydantic."""
    ts_data_updated = []

    for data in ts_data:
        data_to_dict = dict(data)
        shared_ts_data = list(data.usr_shared_data)

        shared_users = []
        for shtd in shared_ts_data:
            await shtd.fetch_related("user__user")
            shared_users.append(
                SharedUserInfoModel(
                    username=shtd.user.username, shared_date=shtd.shared_date
                )
            )

        shared_users.append(
            SharedUserInfoModel(
                username=data.user.username, shared_date=data.created_at
            )
        )

        ts_data_updated.append(
            TimeSeriesDataResponseModel(
                **data_to_dict, owner=data.user.username, shared_users=shared_users
            )
        )

    return ts_data_updated


async def convert_shared_ts_to_pydantic(ts_shared_data: List):
    """Internal function to convert shared timeseries data to pydantic."""
    ts_data_updated = []

    for data in ts_shared_data:
        data_to_dict = dict(data.timeseriesdata)
        await data.timeseriesdata.fetch_related("usr_shared_data", "user__user")
        shared_ts_data = list(data.timeseriesdata.usr_shared_data)

        shared_users = []
        for shtd in shared_ts_data:
            await shtd.fetch_related("user__user")
            shared_users.append(
                SharedUserInfoModel(
                    username=shtd.user.username, shared_date=shtd.shared_date
                )
            )

        shared_users.append(
            SharedUserInfoModel(
                username=data.timeseriesdata.user.username,
                shared_date=data.timeseriesdata.created_at,
            )
        )

        ts_data_updated.append(
            TimeSeriesDataResponseModel(
                **data_to_dict,
                owner=data.timeseriesdata.user.username,
                shared_users=shared_users
            )
        )

    return ts_data_updated


# @router.get('/{searchtext}/limit/{limit}', response_model=List[models.ts_pydantic])
# async def get_data_from_search_string(
#     searchtext: str,
#     limit: int,
#     user: models.user_pydantic = Depends(get_current_user)
# ):
#     ts_data = await models.TimeseriesData.filter(category='kW').filter(name__icontains=searchtext).limit(limit)
#     return [await models.ts_pydantic.from_tortoise_orm(data) for data in ts_data]


@router.get("/", response_model=List[TimeSeriesDataResponseModel])
async def get_timeseries_data(user: models.user_pydantic = Depends(get_current_user)):
    """Get a list of data items for a user."""

    ts_data = (
        await models.TimeseriesData.all()
        .filter(user=await models.Users.get(username=user.username))
        .prefetch_related("usr_shared_data", "user__user")
    )

    ts_data_pydantic = []
    if ts_data:
        ts_data_pydantic += await convert_ts_data_to_pydantic(ts_data)

    ts_data_shared = (
        await models.UserSharedTimeSeriesData.all()
        .filter(user=await models.Users.get(username=user.username))
        .prefetch_related("timeseriesdata__usr_shared_data")
    )

    if ts_data_shared:
        ts_data_pydantic += await convert_shared_ts_to_pydantic(ts_data_shared)

    if ts_data_pydantic:
        return ts_data_pydantic

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Items not found!"
    )


@router.get("/{data_id}", response_model=TimeSeriesDataResponseModel)
async def get_timeseries_data_item(
    data_id: int, user: models.user_pydantic = Depends(get_current_user)
):
    """Get a list of data items for a user."""

    ts_data = await models.TimeseriesData.get(id=data_id).prefetch_related(
        "usr_shared_data", "user__user"
    )

    if ts_data.user.username != user.username:
        try:
            await models.UserSharedTimeSeriesData.get(
                user=await models.Users.get(username=user.username),
                timeseriesdata=await models.TimeseriesData.get(id=data_id),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
            ) from e

    response_data = await convert_ts_data_to_pydantic([ts_data])
    return response_data[0]


@router.get("/{id}/file")
async def get_data_for_download(
    id: int, user: models.user_pydantic = Depends(get_current_user)
):
    """Get a file to download by id"""

    ts_data = await models.TimeseriesData.get(id=id).prefetch_related("user__user")

    if ts_data.user.username != user.username:
        try:
            await models.UserSharedTimeSeriesData.get(
                user=await models.Users.get(username=user.username),
                timeseriesdata=ts_data,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
            ) from e

    file_name = ts_data.filename + ".csv"
    file_path = Path(DATA_PATH) / ts_data.user.username / "timeseries_data" / file_name
    return FileResponse(file_path)


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_timeseries_data(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    metadata: str = Form(),
    user: models.user_pydantic = Depends(get_current_user),
):
    """Create a data item for a user."""

    metadata_pydantic = timeseries_data.TSFormInput.parse_raw(metadata)
    background_tasks.add_task(
        timeseries_data.handle_timeseries_data_upload,
        file,
        metadata_pydantic,
        user.username,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ts_data(
    id: int, user: models.user_pydantic = Depends(get_current_user)
):
    """Delete a data object by id for a user."""

    try:
        ts_data = await models.TimeseriesData.get(
            id=id, user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
        ) from e

    file_name = ts_data.filename + ".csv"
    file_path = Path(DATA_PATH) / user.username / "timeseries_data" / file_name
    await ts_data.delete()
    file_path.unlink(missing_ok=True)
