""" This modules manages custom models. """
import datetime

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