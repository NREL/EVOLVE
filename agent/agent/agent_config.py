from pydantic import BaseModel
from common.scenario import ScenarioData


class AgentConfig(BaseModel):
    """Interface for input config model."""

    id: int
    username: str
    data: ScenarioData
