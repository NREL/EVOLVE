from fastapi import APIRouter, HTTPException, status, Depends

from api import models
from api.dependencies.dependency import get_current_user

router = APIRouter(
    prefix="/data/{data_id}/share",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{username}")
async def share_data_with_user(
    data_id: int, username: str, user: models.user_pydantic = Depends(get_current_user)
):
    """Create shared relation for a data"""
    shared_user = await models.Users.get(username=username)
    shared_data = await models.TimeseriesData.get(id=data_id).prefetch_related(
        "user__user"
    )
    print(shared_data.user.username, user.username)

    if shared_data.user.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
        )

    usr_shared = models.UserSharedTimeSeriesData(
        timeseriesdata=await models.TimeseriesData.get(id=shared_data.id),
        user=await models.Users.get(username=shared_user.username),
    )

    await usr_shared.save()
    return await models.user_shared_ts_data_pydantic.from_tortoise_orm(usr_shared)


@router.delete("/{username}")
async def delete_user_sharing(
    data_id: int, username: str, user: models.user_pydantic = Depends(get_current_user)
):
    """Delete user from sharing the data!"""
    ts_data = await models.TimeseriesData.get(id=data_id).prefetch_related("user__user")
    shared_data = await models.UserSharedTimeSeriesData.get(
        timeseriesdata=ts_data, user=await models.Users.get(username=username)
    )
    if ts_data.user.username == user.username or user.username == username:
        await shared_data.delete()
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
    )
