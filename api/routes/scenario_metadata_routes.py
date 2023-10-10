""" Module for managing routes associated with scenario metadata. """
import uuid
import os
from pathlib import Path
from typing import List
import json
import shutil

from fastapi import (APIRouter, HTTPException, status, Depends)
import tortoise
import pydantic

import models
from dependencies.dependency import get_current_user
from api.scenario_form_model_deprecated import ScenarioData, CloneScenarioInputModel
from custom_models import ScenarioMetaDataResponseModel, SimpleLabelModel

DATA_PATH = os.getenv('DATA_PATH')

router = APIRouter(
    prefix="/scenario",
    tags=["scenario"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=List[ScenarioMetaDataResponseModel])
async def get_all_scenarios(
    user: models.user_pydantic = Depends(get_current_user)):

    scen_data = await models.ScenarioMetadata.all().filter(
        user=await models.Users.get(username=user.username)
    ).prefetch_related('scen_meta')


    all_scenarios = []
    for scen in scen_data:
        scen_dict = dict(scen)
        scen_labels = list(scen.scen_meta)

        scen_labels_pydantic = []
        for scen_label in scen_labels:
            await scen_label.fetch_related('label')

            scen_labels_pydantic.append(
                SimpleLabelModel(labelname=scen_label.label.labelname)
            )

        all_scenarios.append(
            ScenarioMetaDataResponseModel(
                **scen_dict,
                labels=scen_labels_pydantic
            )
        )

    return all_scenarios

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
        
@router.patch('/{id}', response_model=models.scenmeta_pydantic)
async def update_scenario_metadta(
    id: int,
    body: ScenarioData,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Update scenario. """
    try:
        scenario_obj = await models.ScenarioMetadata.get(
            id=id,
            user=await models.Users.get(username=user.username)
        )

        filename = str(uuid.uuid4()) + '.json'
        folder_path = Path(DATA_PATH) / user.username / 'scenarios'
        filepath = folder_path / scenario_obj.filename
        filepath.unlink(missing_ok=True)

        scenario_obj.update_from_dict({
            'name':body.basic.scenarioName,
            'solar': 'solar' in body.basic.technologies,
            'ev': 'ev' in body.basic.technologies,
            'storage': 'energy_storage' in body.basic.technologies,
            'filename':  filename
        })

        await scenario_obj.save()

        with open(folder_path / filename, 'w') as fout:
            fout.write(body.json())

        return await models.scenmeta_pydantic.from_tortoise_orm(scenario_obj)

    except tortoise.exceptions.DoesNotExist as e: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Scenario with id {id} does not exist!')

@router.post('/clone/{id}', response_model=models.scenmeta_pydantic)
async def create_scenario_metadta(
    id: int,
    body: CloneScenarioInputModel,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Clone scenario. """
    try:
        scenario_obj = await models.ScenarioMetadata.get(
            id=id,
            user=await models.Users.get(username=user.username)
        )

        filename = str(uuid.uuid4()) + '.json'
        
        folder_path = Path(DATA_PATH) / user.username / 'scenarios'
        with open(folder_path / scenario_obj.filename, "r") as fp:
            json_body = json.load(fp)

        json_body['basic']['scenarioName'] = body.name

        scenario_obj_clone = models.ScenarioMetadata(
            user= await models.Users.get(username=user.username),
            name=body.name,
            description='Description not yet passed from UI.',
            solar = scenario_obj.solar,
            ev = scenario_obj.ev,
            storage = scenario_obj.storage,
            filename = filename
        )

        with open(folder_path / filename, 'w') as fout:
            json.dump(json_body, fout)

        await scenario_obj_clone.save()
        return await models.scenmeta_pydantic.from_tortoise_orm(scenario_obj_clone)

    except tortoise.exceptions.DoesNotExist as e: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Scenario with id {id} does not exist!')

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
    
    # TODO: Find all the report and delete them as well
    try:
        reports = await models.ReportMetadata.all().filter(
            scenario= scen_data,
            user=await models.Users.get(username=user.username)
        )

        for report in reports:

            report_data_path = (
                Path(DATA_PATH) / user.username / "reports_data" / str(report.id)
            )

            report_json_file = (
                Path(DATA_PATH) / user.username / "reports" / f"{str(report.id)}.json"
            )

            report_zip_path = (
                Path(DATA_PATH) / user.username / "reports_data" / f"{str(report.id)}.zip"
            )
            shutil.rmtree(report_data_path, ignore_errors=True)
            os.remove(report_json_file)
            os.remove(report_zip_path)

    except Exception as e:
        print('Warning: ', e)

    file_name = scen_data.filename
    file_path = Path(DATA_PATH) / user.username / 'scenarios' / file_name
    await scen_data.delete()
    file_path.unlink(missing_ok=True)
    