""" Module for handling RABBIT MQ Queue message."""

# Manage python standard imports
from pathlib import Path
import os

# Third-party imports
import polars


# Internal imports
from processor.input_config_model import InputConfigModel
from processor.helper_functions import (
    DB_CONFIG,
    DATA_PATH
)

from processor.energy_storage import process_energy_storage
from processor.postgres_db_context import PostGresDB
from processor.base_load import get_load_df, compute_base_load_metrics



def update_report_status(id:int, status:str):
    with PostGresDB(DB_CONFIG) as cursor:
        cursor.execute(
            f"""update reportmetadata 
                set status=%s where id=%s""", [status, id]
        )



def process_scenario(
    input_config: InputConfigModel,
):
    """ Takes a full scenario json and simulates a scenario. 
    
    Args
        input_config (Dict): Scenario JSON content along with
            report metadata.
    """
    
    # Update the status
    update_report_status(input_config.id, 'RUNNING')

    base_path = Path(DATA_PATH) / input_config.username / 'reports_data' / str(input_config.id)
    if not base_path.exists():
        base_path.mkdir(parents=True)

    try:
        load_df = get_load_df(
            input_config.data.basic.loadProfile,
            input_config.data.basic.startDate,
            input_config.data.basic.endDate,
            input_config.data.basic.resolution,
            input_config.data.basic.dataFillingStrategy
        )
        load_df = load_df.sort(by='timestamp')
        compute_base_load_metrics(load_df, input_config.data.basic.resolution, base_path,
            prefix='base_load')
        
        if input_config.data.energy_storage:
            net_load_df = process_energy_storage(
                input_config.data.energy_storage,
                load_df,
                base_path,
                input_config.data.basic.resolution
            )
            compute_base_load_metrics(net_load_df, input_config.data.basic.resolution, base_path,
                prefix='net_load')
        
        update_report_status(input_config.id, 'COMPLETED')


    except Exception as e:
        with open(base_path / 'error.txt', 'w') as fp:
            fp.write(str(e))
        print(e)
        update_report_status(input_config.id, 'ERROR')



if __name__ == '__main__':
    
    import json
    import pydantic 
    with open(r"C:\Users\KDUWADI\Desktop\NREL_Projects\TUNISIA\data\evolve_data_post\jake\reports\12.json", "r") as fp:
        json_content = json.load(fp)

    input_config = {
        "id": 12,
        "username": "jake",
        "data": json_content
    }

    input_config_pydantic= pydantic.parse_obj_as(InputConfigModel, input_config)
    process_scenario(input_config_pydantic)





