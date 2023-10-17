""" This modules manages custom models. """
import datetime
from typing import List

from pydantic import BaseModel


class DataCommentInput(BaseModel):
    """Interface for data comment model."""

    comment: str


class DataCommentResponseModel(BaseModel):
    """Interface for data comment response model."""

    id: int
    comment: str
    updated_at: datetime.datetime
    edited: bool
    created_at: datetime.datetime
    timeseriesdata_id: int
    username: str


class SharedUserInfoModel(BaseModel):
    """Interface for shared user info model."""

    username: str
    shared_date: datetime.datetime


class TimeSeriesDataResponseModel(BaseModel):
    """Interface for time series data response model."""

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


class SimpleLabelModel(BaseModel):
    """Interface for scenario label model."""

    labelname: str


class ScenarioMetaDataResponseModel(BaseModel):
    """Interface for scenario metadata response model."""

    id: int
    created_at: datetime.datetime
    name: str
    description: str
    solar: bool
    ev: bool
    storage: bool
    filename: str
    labels: List[SimpleLabelModel]
