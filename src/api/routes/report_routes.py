""" Module for managing routes associated with labels. """
from typing import List 
import os
from pathlib import Path
import json
import datetime

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


@router.get('/report/{id}/load/base') # response_model=LoadTimeSeriesDataResponse
async def get_timeseries_baseload(
    id: int, 
    resolution: int,
    user: models.user_pydantic = Depends(get_current_user)
):
    report_data = await models.ReportMetadata.get(
        id=id, 
        user=await models.Users.get(username=user.username)
    )

    report_json_path = Path(DATA_PATH) / user.username / 'reports' / f"{id}.json"

    if not report_json_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='JSON file not found!'
        )

    with open(report_json_path, "r") as fp:
        json_content = json.load(fp)

    data_obj = await models.TimeseriesData.get(
        id=json_content['basic']['loadProfile']
    )

    csv_file_path = Path(DATA_PATH) / user.username / 'timeseries_data' / f'{data_obj.filename}.csv'
    if not csv_file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Data CSV file not found!'
        )

    df = polars.read_csv(csv_file_path, parse_dates=True)

    df = df.groupby_dynamic("timestamp", every=f"{resolution}m").agg(polars.col("kW").mean()).filter(
        (polars.col('timestamp') > datetime.datetime.strptime(json_content['basic']['startDate'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))  & \
        (polars.col('timestamp') < datetime.datetime.strptime(json_content['basic']['endDate'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    )

    df_to_dict = df.to_dict(as_series=False)

    return {
        'data': [round(el, 2) for el in df_to_dict['kW']],
        'start_date': str(df.select(polars.col('timestamp')).min()[0,0]),
        'end_date':str(df.select(polars.col('timestamp')).max()[0,0]),
        'resolution': resolution
    }

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

