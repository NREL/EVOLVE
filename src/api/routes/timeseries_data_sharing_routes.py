
from fastapi import (APIRouter, HTTPException, status, Depends)

import models
from dependencies.dependency import get_current_user

router = APIRouter(
    prefix="/data/{data_id}/share",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


# @router.get('/')
# async def get_shared_users(
#     data_id: int,
#     user: models.user_pydantic = Depends(get_current_user)
# ):
#     """ Get a list of shared user for a data by id"""
#     parent_data = await models.TimeseriesData.get(id=data_id)

#     if parent_data.username != user.username:
#         shared_user = await models.UserSharedTimeSeriesData.get(
#             timeseries_data=await models.TimeseriesData.get(id=shared_data.id), 
#             user=await models.Users.get(username=shared_user.username)
#         )
    
#     shared_data = await models.UserSharedTimeSeriesData.all().filter(
#         timeseries_data=await models.TimeseriesData.get(id=data_id)
#     )
#     if shared_data:
#         shared_data_pydantic = [await models.user_shared_ts_data_pydantic.from_tortoise_orm(data) \
#              for data in shared_data]
#         return [d.username for d in shared_data_pydantic] + [parent_data.username]
    


@router.post('/{username}')
async def share_data_with_user(
    data_id: int,
    username: str,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Create shared relation for a data """
    shared_user = await models.Users.get(username=username)
    shared_data = await models.TimeseriesData.get(id=data_id).prefetch_related(
        "user__user"
    )

    if shared_data.user.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")
    
    usr_shared = models.UserSharedTimeSeriesData(
        timeseriesdata=await models.TimeseriesData.get(id=shared_data.id),
        user=await models.Users.get(username=shared_user.username),
    )

    await usr_shared.save()
    return await models.user_shared_ts_data_pydantic.from_tortoise_orm(
        usr_shared
    )






