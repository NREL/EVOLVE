""" This modules manages custom models. """

from pydantic import BaseModel

class DataCommentInput(BaseModel):
    comment: str