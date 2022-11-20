""" This modules manages custom models. """
import datetime
from typing import List

from pydantic import BaseModel

class DataCommentInput(BaseModel):
    comment: str


class DataCommentResponseModel(BaseModel):
    id: int
    comment: str
    updated_at: datetime.datetime
    edited: bool
    created_at: datetime.datetime
    timeseriesdata_id: int
    username: str


class SharedUserInfoModel(BaseModel):
    username: str 
    shared_date: datetime.datetime

class TimeSeriesDataResponseModel(BaseModel):
    id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    resolution_min: int
    created_at: datetime.datetime
    name: str 
    description: str 
    image: str 
    filename: str 
    category: str 
    owner: str
    shared_users: List[SharedUserInfoModel]


