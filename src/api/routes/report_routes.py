""" Module for managing routes associated with labels. """
from typing import List 
import os
from pathlib import Path
import json

from fastapi import (APIRouter, HTTPException, status, Depends)
from pydantic import BaseModel
import tortoise

from dependencies.dependency import get_current_user
import models
import rabbit_mq


DATA_PATH = os.getenv('DATA_PATH')

class ReportCreateFormModel(BaseModel):
    name: str 
    description: str 

router = APIRouter(
    prefix="",
    tags=["report"],
    responses={404: {"description": "Not found"}},
)


@router.get('/scenario/{id}/report', response_model=List[models.report_pydantic])
async def get_all_reports(
    id: int,
    user: models.user_pydantic = Depends(get_current_user)):
    """ Get all reports for a given scenario id."""

    reports = await models.ReportMetadata.all().filter(
        user=await models.Users.get(username=user.username),
        scenario= await models.ScenarioMetadata.get(id=id)
    ).order_by('-created_at')

    return [await models.report_pydantic.from_tortoise_orm(report) 
        for report in reports]

@router.post('/scenario/{id}/report', response_model=models.report_pydantic)
async def create_report(
    id: int,
    body: ReportCreateFormModel,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Create report for a given scenario id. """

    scenario = await models.ScenarioMetadata.get(
            id=id, user=await models.Users.get(username=user.username))
    report_obj = models.ReportMetadata(
        user= await models.Users.get(username=user.username),
        name=body.name,
        description=body.description,
        status='SUBMITTED',
        scenario= scenario
    )

    folder_path = Path(DATA_PATH) / user.username / 'scenarios'
    json_path = folder_path / scenario.filename

    with open(json_path, "r") as fp:
        scen_dict = json.load(fp)

    await report_obj.save()
    report_response = await models.report_pydantic.from_tortoise_orm(report_obj)
    
    rabbit_mq.publish_message(
        json.dumps({
            "id": report_response.id,
            "username": user.username,
            "data": scen_dict
        })
    )
    return report_response
        

@router.delete('/report/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(id: int, user: models.user_pydantic = Depends(get_current_user)):
    """ Delete report data by id. """

    try:
        report_data = await models.ReportMetadata.get(
            id=id, 
            user=await models.Users.get(username=user.username)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized!")

    await report_data.delete()

@router.patch('/report/{id}', response_model=models.report_pydantic)
async def update_report(
    id: int,
    body: ReportCreateFormModel,
    user: models.user_pydantic = Depends(get_current_user)
):
    """ Update report by id """
    try:
        report_obj = await models.ReportMetadata.get(
            id=id,
            user=await models.Users.get(username=user.username)
        )

        report_obj.update_from_dict({
            'name':body.name,
            'description': body.description
        })

        await report_obj.save()

        return await models.report_pydantic.from_tortoise_orm(report_obj)

    except tortoise.exceptions.DoesNotExist as e: 

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Report with id {id} does not exist!')

