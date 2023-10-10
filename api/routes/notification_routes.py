""" Module for managing routes associated with labels. """
from typing import List 
import datetime

from fastapi import (APIRouter, HTTPException, status, Depends)

from dependencies.dependency import get_current_user
import models

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={404: {"description": "Not found"}},
)



@router.get('/', response_model=List[models.notification_pydantic])
async def get_all_notifications(
    visited: bool,
    since_last: datetime.datetime,
    user: models.user_pydantic = Depends(get_current_user)):

    notification_data = await models.Notifications.all().filter(
        user=await models.Users.get(username=user.username),
        visited=visited,
        created_at__gte=since_last,
        archived=False
    ).order_by('-created_at')

    return [await models.notification_pydantic.from_tortoise_orm(notification) 
        for notification in notification_data]

# @router.post('/', response_model=models.notification_pydantic)
# async def create_notification(
#     body: NotificationCreateFormModel,
#     user: models.user_pydantic = Depends(get_current_user)
# ):
#     """ Create notifications. """

#     not_obj = models.Notifications(
#         user= await models.Users.get(username=user.username),
#         message = body.message,
#         archived = False,
#         visited  = False
#     )

#     await not_obj.save()
#     return await models.notification_pydantic.from_tortoise_orm(not_obj)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(id: int, user: models.user_pydantic = Depends(get_current_user)):
    """ Delete notification data by id. """

    try:
        not_data = await models.Notifications.get(
            id=id, 
            user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")

    await not_data.delete()

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_notification(user: models.user_pydantic = Depends(get_current_user)):
    """ Delete all notification. """

    try:
        not_data = await models.Notifications.all().filter(
            user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")
    
    _ = [await notification.delete() for notification in not_data]

