""" Module for testing evolve agent for processing DER scenarios."""

# standard imports
import json
from pathlib import Path

# third-party imports
from agent.scenario_processor import process_scenario
from agent.agent_config import AgentConfig


def test_agent_function():
    """Test agent functions."""

    data_folder = Path("./data")
    for file in data_folder.iterdir():
        if file.suffix != ".json":
            continue

        with open(file, "r", encoding="utf-8") as file_pointer:
            json_content = json.load(file_pointer)

        

        # process_scenario(AgentConfig.model_validate({
        #     "id": ,
        #     "username": ,
        #     "data": json_content
        # }))
