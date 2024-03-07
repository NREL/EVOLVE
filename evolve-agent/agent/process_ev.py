""" This module contains function to process solar."""
# standard imports
import datetime

# third-party imports
import polars
from common.electric_vehicle import EVFormData
from common.scenario import BasicFormData
from agent.ev_aggregate import SimulationInputConfig, LargeScaleEVSimulatorV1
from agent.helper_functions import populate_sliced_category, sort_metric_dataframe


def compute_ev_energy_metric(ev_power_df: polars.DataFrame, resolution: int):
    """Compute metrics for electric vehicle."""
    df = populate_sliced_category(ev_power_df)
    ev_metric_df = polars.DataFrame()

    for column in df.columns:
        if column not in ["timestamp", "category"]:
            df_ = (
                df.groupby("category")
                .agg([polars.col(column).sum(), polars.col("timestamp").min()])
                .with_columns((polars.col(column) * (resolution / 60)).alias(column))
                .select([column, "category", "timestamp"])
            )

            if not len(ev_metric_df):
                ev_metric_df = df_
            else:
                ev_metric_df = df_.join(ev_metric_df, on="category", how="left")
    return ev_metric_df


def process_ev(
    evs: list[EVFormData], base_path: str, basic_data: BasicFormData, num_steps: int
) -> polars.DataFrame:
    """Simulates electric vehicle."""

    config = SimulationInputConfig(
        start_time=basic_data.startDate, resolution_min=basic_data.resolution, steps=num_steps
    )

    ev_model = LargeScaleEVSimulatorV1(
        vehicles=[ev for ev in evs if ev.evType == "vehicle"],
        stations=[ev for ev in evs if ev.evType == "charging_station"],
    )
    trans_model = ev_model.simulate(config)
    ev_df = ev_model.aggregate_vehicle_results(trans_model)
    station_df = ev_model.aggregate_station_results(trans_model)

    ev_df.write_csv(base_path / "ev_timeseries.csv")
    station_df.write_csv(base_path / "station_timeseries.csv")
    ev_metric_df = compute_ev_energy_metric(ev_df, basic_data.resolution)

    ev_metric_df_sorted = sort_metric_dataframe(ev_metric_df)
    ev_metric_df_sorted.write_csv(base_path / "ev_metrics.csv")

    return ev_df
