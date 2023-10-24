""" Module for managing routes associated with labels. """
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
import tortoise

from dependencies.dependency import get_current_user
from label_form_model import ScenarioLabelFormModel
import models

router = APIRouter(
    prefix="/scenario",
    tags=["scenario_label"],
    responses={404: {"description": "Not found"}},
)


@router.post("/label", response_model=models.scen_label_pydantic)
async def create_scen_label(
    body: ScenarioLabelFormModel, user: models.user_pydantic = Depends(get_current_user)
):
    """Add label to a scenario."""

    # Making sure label exists
    await models.Labels.get(
        labelname=body.labelname, user=await models.Users.get(username=user.username)
    )

    # Making sure scenario exists
    await models.ScenarioMetadata.get(
        id=body.scenarioid, user=await models.Users.get(username=user.username)
    )

    try:
        await models.ScenarioLabels.get(
            label=await models.Labels.get(labelname=body.labelname),
            scenario=await models.ScenarioMetadata.get(id=body.scenarioid),
            user=await models.Users.get(username=user.username),
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Label already exists for a scenario.",
        )

    except tortoise.exceptions.DoesNotExist:
        scen_label_obj = models.ScenarioLabels(
            label=await models.Labels.get(labelname=body.labelname),
            scenario=await models.ScenarioMetadata.get(id=body.scenarioid),
            user=await models.Users.get(username=user.username),
        )

        await scen_label_obj.save()
        return await models.scen_label_pydantic.from_tortoise_orm(scen_label_obj)


@router.delete("/{id}/label/{labelname}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario_label(
    id: int, labelname: str, user: models.user_pydantic = Depends(get_current_user)
):
    """Delete scenario label by name."""

    try:
        scen_label_data = await models.ScenarioLabels.get(
            label=await models.Labels.get(labelname=labelname),
            scenario=await models.ScenarioMetadata.get(id=id),
            user=await models.Users.get(username=user.username),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!"
        ) from e

    await scen_label_data.delete()
