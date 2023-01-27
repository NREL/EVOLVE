""" Module for managing routes associated with labels. """
from typing import List 
import os
from pathlib import Path
import json
import datetime
import shutil

from fastapi import (APIRouter, HTTPException, status, Depends)
from pydantic import BaseModel
import tortoise
import polars

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


@router.get('/report/{id}/load') # response_model=LoadTimeSeriesDataResponse
async def get_timeseries_baseload(
    id: int, 
    data_type: str,
    user: models.user_pydantic = Depends(get_current_user)
):
    
    data_type_to_file_name_mapping  = {
        'base_timeseries': 'base_load.csv',
        'base_energy_metrics': 'base_load_energy_metrics.csv',
        'base_power_metrics': 'base_load_peak_power_metrics.csv',
        'net_timeseries': 'net_load.csv',
        'net_energy_metrics': 'net_load_energy_metrics.csv',
        'net_power_metrics': 'net_load_peak_power_metrics.csv',
        'battery_power': 'battery_power_timeseries.csv'
    }
    try:
        df = polars.read_csv(Path(DATA_PATH) / user.username/ 'reports_data' / str(id)/ data_type_to_file_name_mapping.get(
            data_type, None
        ))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ran into an error reading file. >> {e}")

    if len(df) > 2000:
        df = df.limit(2000)
 
    return  df.to_dict(as_series=False)


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

    output_path = Path(DATA_PATH) / user.username / 'reports'

    if not output_path.exists():
        output_path.mkdir(parents=True)

    output_json_path = output_path / f"{report_response.id}.json"
    with open(output_json_path, "w") as fp:
        json.dump(scen_dict,fp)

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

    report_path = Path(DATA_PATH) /  user.username / 'reports_data' / str(report_data.id)
    shutil.rmtree(report_path, ignore_errors=True)

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

