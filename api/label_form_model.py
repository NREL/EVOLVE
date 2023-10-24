from pydantic import BaseModel


class LabelCreateFormModel(BaseModel):
    """Interface for label model used in crating it."""

    name: str
    description: str


class ScenarioLabelFormModel(BaseModel):
    """Interface for scenario label."""

    scenarioid: int
    labelname: str
