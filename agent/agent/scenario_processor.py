""" Module for handling RABBIT MQ Queue message."""

# Manage python standard imports
from pathlib import Path
import traceback

# Third-party imports
import polars
import numpy as np


# Internal imports
from agent.agent_config import AgentConfig
from agent.helper_functions import DB_CONFIG, DATA_PATH

from agent.energy_storage import process_energy_storage
from agent.postgres_db_context import PostGresDB
from agent.base_load import get_load_df, compute_base_load_metrics
from agent.process_solar import process_solars
from agent.process_ev import process_ev


def update_report_status(id: int, status: str):
    """Update report status."""
    print(DB_CONFIG)
    with PostGresDB(DB_CONFIG) as cursor:
        cursor.execute(
            """update reportmetadata 
                set status=%s where id=%s""",
            [status, id],
        )


def process_scenario(
    input_config: AgentConfig,
):
    """Takes a full scenario json and simulates a scenario.

    Args
        input_config (AgentConfig): Scenario JSON content along with
            report metadata.
    """

    # Update the status
    update_report_status(input_config.id, "RUNNING")

    base_path = Path(DATA_PATH) / input_config.username / "reports_data" / str(input_config.id)
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

        net_load_ = False
        if input_config.data.solar:
            solar_df = process_solars(input_config.data.solar, base_path, input_config.data.basic)

            total_solar_power = list(
                solar_df.select(polars.col("*").exclude("timestamp")).sum(axis=1)
            )

            load_df = load_df.with_columns([polars.col("kW") - np.array(total_solar_power)])
            net_load_ = True

        if input_config.data.energy_storage:
            battery_df = process_energy_storage(
                input_config.data.energy_storage,
                load_df,
                base_path,
                input_config.data.basic.resolution,
            )

            total_battery_power = list(
                battery_df.select(polars.col("*").exclude("timestamp")).sum(axis=1)
            )
            total_battery_power = [-el for el in total_battery_power]
            load_df = load_df.with_columns([polars.col("kW") + np.array(total_battery_power)])
            net_load_ = True

        if input_config.data.ev:
            ev_df = process_ev(
                input_config.data.ev, base_path, input_config.data.basic, len(load_df)
            )
            total_ev_power = list(ev_df.select(polars.col("*").exclude("timestamp")).sum(axis=1))
            load_df = load_df.with_columns([polars.col("kW") + np.array(total_ev_power)])
            net_load_ = True

        if net_load_:
            compute_base_load_metrics(
                load_df,
                input_config.data.basic.resolution,
                base_path,
                prefix="net_load",
            )

        update_report_status(input_config.id, "COMPLETED")

    except Exception as e:
        with open(base_path / "error.txt", "w", encoding="utf-8") as fp:
            fp.write(str(e))
            fp.write(traceback.format_exc())

        update_report_status(input_config.id, "ERROR")
