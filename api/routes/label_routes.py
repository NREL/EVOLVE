""" Module for managing routes associated with labels. """
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
import tortoise

from dependencies.dependency import get_current_user
from label_form_model import LabelCreateFormModel
import models

router = APIRouter(
    prefix="/label",
    tags=["label"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[models.label_pydantic])
async def get_all_labels(user: models.user_pydantic = Depends(get_current_user)):
    """Function to return all labels."""

    label_data = await models.Labels.all().filter(
        user=await models.Users.get(username=user.username)
    )

    return [
        await models.label_pydantic.from_tortoise_orm(label) for label in label_data
    ]


@router.post("/", response_model=models.label_pydantic)
async def create_label(
    body: LabelCreateFormModel, user: models.user_pydantic = Depends(get_current_user)
):
    """Create new label."""
    try:
        await models.Labels.get(
            labelname=body.name, user=await models.Users.get(username=user.username)
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Label with same name already exists!",
        )

    except tortoise.exceptions.DoesNotExist:
        label_obj = models.Labels(
            user=await models.Users.get(username=user.username),
            labelname=body.name,
            description=body.description,
        )

        await label_obj.save()
        return await models.label_pydantic.from_tortoise_orm(label_obj)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(id: int, user: models.user_pydantic = Depends(get_current_user)):
    """Delete label data by id."""

    try:
        label_data = await models.Labels.get(
            id=id, user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
        ) from e

    await label_data.delete()


@router.patch("/{id}", response_model=models.label_pydantic)
async def create_scenario_metadta(
    id: int,
    body: LabelCreateFormModel,
    user: models.user_pydantic = Depends(get_current_user),
):
    """Update label by id."""
    try:
        label_obj = await models.Labels.get(
            id=id, user=await models.Users.get(username=user.username)
        )

        label_obj.update_from_dict(
            {"labelname": body.name, "description": body.description}
        )

        await label_obj.save()

        return await models.label_pydantic.from_tortoise_orm(label_obj)

    except tortoise.exceptions.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario with id {id} does not exist!",
        ) from e
