from pydantic import BaseModel

class LabelCreateFormModel(BaseModel):
    name: str
    description: str

class ScenarioLabelFormModel(BaseModel):
    scenarioid: int 
    labelname: str



