""" Module for managing routes associated with scenario metadata. """
import uuid
import os
from pathlib import Path
from typing import List

from fastapi import (APIRouter, HTTPException, status, Depends)
import tortoise
import pydantic

import models
from dependencies.dependency import get_current_user
from scenario_form_model import ScenarioData

DATA_PATH = os.getenv('DATA_PATH')

router = APIRouter(
    prefix="/scenario",
    tags=["scenario"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=List[models.scenmeta_pydantic])
async def get_all_scenarios(
    user: models.user_pydantic = Depends(get_current_user)):

    scen_data = await models.ScenarioMetadata.all().filter(
        user=await models.Users.get(username=user.username)
    )

    return [await models.scenmeta_pydantic.from_tortoise_orm(scen) 
        for scen in scen_data]

@router.get('/{id}', response_model=ScenarioData)
async def get_scenario_metadata(
    id: int,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Get JSON scenario metadata by ID."""
    scen_data = await models.ScenarioMetadata.get(
            id=id,
            user=await models.Users.get(username=user.username)
        )

    file_path = Path(DATA_PATH) / user.username / 'scenarios' / scen_data.filename
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail='Item not found!')

    return pydantic.parse_file_as(ScenarioData, file_path)

@router.post('/', response_model=models.scenmeta_pydantic)
async def create_scenario_metadta(
    body: ScenarioData,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Create scenario metadata. """
    try:
        await models.ScenarioMetadata.get(
            name=body.basic.scenarioName,
            user=await models.Users.get(username=user.username)
        )
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail='Scenario with same name already exists!')
    
    except tortoise.exceptions.DoesNotExist as e: 
        
        filename = str(uuid.uuid4()) + '.json'

        folder_path = Path(DATA_PATH) / user.username / 'scenarios'
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
     
        with open(folder_path / filename, 'w') as fout:
            fout.write(body.json())

        scenario_obj = models.ScenarioMetadata(
            user= await models.Users.get(username=user.username),
            name=body.basic.scenarioName,
            description='Description not yet passed from UI.',
            solar = 'solar' in body.basic.technologies,
            ev = 'ev' in body.basic.technologies,
            storage = 'energy_storage' in body.basic.technologies,
            filename = filename
        )

        await scenario_obj.save()
        return await models.scenmeta_pydantic.from_tortoise_orm(scenario_obj)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario_data(id: int, user: models.user_pydantic = Depends(get_current_user)):
    """ Delete scenario data by id. """

    try:
        scen_data = await models.ScenarioMetadata.get(
            id=id, 
            user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")

    file_name = scen_data.filename
    file_path = Path(DATA_PATH) / user.username / 'scenarios' / file_name
    await scen_data.delete()
    file_path.unlink(missing_ok=True)