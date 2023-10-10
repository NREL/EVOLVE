""" This module contains functions to get base load 
data and compute metrics."""

# standard imports
from pathlib import Path
from typing import Dict

# third-party imports
import polars


# internal imports
from processor.helper_functions import (
    upsample_interpolate_df,
    upsample_staircase_df,
    downsample_df,
    filter_by_date,
    DATA_PATH,
    populate_sliced_category,
    get_file_name_from_id,
    sort_metric_dataframe
)


def compute_energy_metric(
    df: polars.DataFrame, resolution: int, column_name="kW"
):
    """Compute energy for different category"""

    df = populate_sliced_category(df)

    import_df = (
        df.filter(polars.col(column_name) > 0)
        .groupby("category")
        .agg(polars.col(column_name).sum())
        .with_column(
            (polars.col(column_name) * resolution / 60).alias("import_kWh")
        )
        .select(["import_kWh", "category"])
    )

    export_df = (
        df.filter(polars.col(column_name) <= 0)
        .groupby("category")
        .agg(polars.col(column_name).sum())
        .with_column(
            (polars.col(column_name) * resolution / 60).alias("export_kWh")
        )
        .select(["export_kWh", "category"])
    )

    return import_df.join(export_df, on="category", how="left")


def compute_max_power(df: polars.DataFrame, column_name="kW"):
    """Compute max power"""

    df = populate_sliced_category(df)

    import_df = (
        df.filter(polars.col(column_name) > 0)
        .groupby("category")
        .agg(polars.col(column_name).max())
        .with_column((polars.col(column_name)).alias("import_peak_kW"))
        .select(["import_peak_kW", "category"])
    )

    export_df = (
        df.filter(polars.col(column_name) <= 0)
        .groupby("category")
        .agg(polars.col(column_name).max())
        .with_column((polars.col(column_name)).alias("export_peak_kW"))
        .select(["export_peak_kW", "category"])
    )

    return import_df.join(export_df, on="category", how="left")


def compute_base_load_metrics(
    load_df: polars.DataFrame, resolution: int, base_path: str, prefix: str
):

    base_load_energy_df = compute_energy_metric(load_df, resolution)
    base_load_power_df = compute_max_power(load_df)

    load_df.write_csv(base_path / f"{prefix}.csv")

    base_load_energy_df_sorted = sort_metric_dataframe(base_load_energy_df)
    base_load_energy_df_sorted.write_csv(base_path / f"{prefix}_energy_metrics.csv")
    
    base_load_power_df_sorted = sort_metric_dataframe(base_load_power_df)
    base_load_power_df_sorted.write_csv(base_path / f"{prefix}_peak_power_metrics.csv")


def get_load_df(
    load_id: int,
    start_date: str,
    end_date: str,
    resolution: int,
    strategy: str,
):

    """Returns a polars dataframe."""
    file_owner, filename, data_res = get_file_name_from_id(load_id)
    file_path = (
        Path(DATA_PATH) / file_owner / "timeseries_data" / (filename + ".csv")
    )

    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist!")

    df = filter_by_date(
        polars.read_csv(file_path, parse_dates=True), start_date, end_date
    )

    if data_res <= resolution:
        return downsample_df(df, resolution, "kW")
    else:
        return {
            "interpolation": upsample_interpolate_df,
            "staircase": upsample_staircase_df,
        }.get(strategy)(df, resolution)
