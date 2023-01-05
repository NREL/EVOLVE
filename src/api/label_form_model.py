from pydantic import BaseModel

class LabelCreateFormModel(BaseModel):
    name: str
    description: str



