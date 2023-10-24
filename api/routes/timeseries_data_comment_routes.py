""" Module for managing routes associated with """
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

import models
from custom_models import DataCommentResponseModel, DataCommentInput
from dependencies.dependency import get_current_user


router = APIRouter(
    prefix="/data/{data_id}/comments",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


async def authenticate_access(username: str, data_id: id):
    """Check if the user can access the comments."""

    ts_data = await models.TimeseriesData.get(id=data_id).prefetch_related("user__user")
    if ts_data.user.username != username:
        # If the user is not owner make sure the data is shared with this user
        shared_user = await models.Users.get(username=username)
        try:
            await models.UserSharedTimeSeriesData.get(id=data_id, user=shared_user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access!"
            ) from e

    return True


@router.get("/", response_model=List[DataCommentResponseModel])
async def get_comments_for_data(
    data_id: int, user: models.user_pydantic = Depends(get_current_user)
):
    """Get all the comments for given data id."""

    await authenticate_access(user.username, data_id)

    comments = await models.DataComments.filter(
        timeseriesdata=await models.TimeseriesData.get(id=data_id)
    ).prefetch_related("user__user")

    comment_objs = []
    for comment in comments:
        comment_dict = dict(comment)
        comment_dict.update({"username": comment.user.username})
        comment_objs.append(DataCommentResponseModel(**comment_dict))

    return comment_objs


@router.post("/", response_model=models.data_comments_pydantic)
async def create_data_comment(
    comment: DataCommentInput,
    data_id: int,
    user: models.user_pydantic = Depends(get_current_user),
):
    """Create a comment for given data id"""
    await authenticate_access(user.username, data_id)

    comment_obj = models.DataComments(
        timeseriesdata=await models.TimeseriesData.get(id=data_id),
        user=await models.Users.get(username=user.username),
        comment=comment.comment,
        edited=False,
    )
    await comment_obj.save()
    return await models.data_comments_pydantic.from_tortoise_orm(comment_obj)


@router.put("/{comment_id}", response_model=models.data_comments_pydantic)
async def update_comments_for_data(
    data_id: int,
    comment_id: int,
    updated_comment: DataCommentInput,
    user: models.user_pydantic = Depends(get_current_user),
):
    """Edit comment by data id and comment id."""

    try:
        comment = await models.DataComments.get(
            timeseriesdata=await models.TimeseriesData.get(id=data_id),
            id=comment_id,
            user=await models.Users.get(username=user.username),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access!"
        ) from e

    comment.comment = updated_comment.comment
    comment.edited = True
    await comment.save()
    return await models.data_comments_pydantic.from_tortoise_orm(comment)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comments_for_data(
    data_id: int,
    comment_id: int,
    user: models.user_pydantic = Depends(get_current_user),
):
    """Delete comment by comment id and data id."""
    try:
        comment = await models.DataComments.get(
            timeseriesdata=await models.TimeseriesData.get(id=data_id),
            id=comment_id,
            user=await models.Users.get(username=user.username),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access!"
        ) from e
    await comment.delete()
