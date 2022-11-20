""" Module for managing routes associated with scenario metadata. """
import uuid
import os
from pathlib import Path
from typing import List

from fastapi import (APIRouter, HTTPException, status, Depends)
import tortoise

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
        
