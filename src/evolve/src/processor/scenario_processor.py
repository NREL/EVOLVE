""" Module for handling RABBIT MQ Queue message."""

# Manage python standard imports
from pathlib import Path
import os

# Third-party imports
import polars


# Internal imports
from processor.input_config_model import InputConfigModel
from processor.helper_functions import DB_CONFIG, DATA_PATH

from processor.energy_storage import process_energy_storage
from processor.postgres_db_context import PostGresDB
from processor.base_load import get_load_df, compute_base_load_metrics
from processor.process_solar import process_solars


def update_report_status(id: int, status: str):
    print(DB_CONFIG)
    with PostGresDB(DB_CONFIG) as cursor:
        cursor.execute(
            f"""update reportmetadata 
                set status=%s where id=%s""",
            [status, id],
        )


def process_scenario(
    input_config: InputConfigModel,
):
    """Takes a full scenario json and simulates a scenario.

    Args
        input_config (Dict): Scenario JSON content along with
            report metadata.
    """

    # Update the status
    update_report_status(input_config.id, "RUNNING")

    base_path = (
        Path(DATA_PATH)
        / input_config.username
        / "reports_data"
        / str(input_config.id)
    )
    if not base_path.exists():
        base_path.mkdir(parents=True)

    try:
        load_df = get_load_df(
            input_config.data.basic.loadProfile,
            input_config.data.basic.startDate,
            input_config.data.basic.endDate,
            input_config.data.basic.resolution,
            input_config.data.basic.dataFillingStrategy,
        )
        load_df = load_df.sort(by="timestamp")
        compute_base_load_metrics(
            load_df,
            input_config.data.basic.resolution,
            base_path,
            prefix="base_load",
        )

        total_solar_power = None
        total_battery_power = None

        if input_config.data.solar:
            solar_df = process_solars(
                input_config.data.solar, base_path, input_config.data.basic
            )

            total_solar_power = list(
                solar_df.select(polars.col("*").exclude("timestamp")).sum(
                    axis=1
                )
            )

        if input_config.data.energy_storage:

            battery_df = process_energy_storage(
                input_config.data.energy_storage,
                load_df,
                base_path,
                input_config.data.basic.resolution,
            )

            total_battery_power = list(
                battery_df.select(polars.col("*").exclude("timestamp")).sum(
                    axis=1
                )
            )

        net_power = []
        for power in [
            load_df["kW"].to_list(),
            total_solar_power,
            total_battery_power,
        ]:
            if power and not net_power:
                net_power = power
            elif net_power and power:
                net_power = [el if el else 0 for el in net_power]
                power = [el if el else 0 for el in power]
                net_power = [a + b for a, b in zip(net_power, power)]

        if net_power:
            compute_base_load_metrics(
                polars.from_dict(
                    {
                        "timestamp": load_df["timestamp"].to_list(),
                        "kW": net_power,
                    }
                ),
                input_config.data.basic.resolution,
                base_path,
                prefix="net_load",
            )

        update_report_status(input_config.id, "COMPLETED")

    except Exception as e:
        with open(base_path / "error.txt", "w") as fp:
            fp.write(str(e))
        print(e)
        import traceback

        print(traceback.format_exc())
        update_report_status(input_config.id, "ERROR")


if __name__ == "__main__":

    import json
    import pydantic

    with open(
        r"C:\Users\KDUWADI\Desktop\NREL_Projects\TUNISIA\data\evolve_data_post\jake\reports\16.json",
        "r",
    ) as fp:
        json_content = json.load(fp)

    input_config = {"id": 16, "username": "jake", "data": json_content}

    input_config_pydantic = pydantic.parse_obj_as(
        InputConfigModel, input_config
    )
    process_scenario(input_config_pydantic)
