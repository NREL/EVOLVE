""" This module contains higher level functions to interact with
solar model and compute time series metrics. """

# standard python imports
from typing import List
from pathlib import Path


# third-party imports
import polars


# internal imports
from processor.input_config_model import SolarFormData, BasicFormData
from processor.postgres_db_context import PostGresDB
from processor.helper_functions import (
    DB_CONFIG,
    DATA_PATH,
    get_file_name_from_id,
    filter_by_date,
    downsample_df,
    upsample_interpolate_df,
    upsample_staircase_df,
    populate_sliced_category,
    sort_metric_dataframe
)


from solar import (
    FixedAxisModel,
    SingleAxisModel,
    DualAxisModel,
    SolarBasicModel,
    InverterModel,
    FixedAxisSolarModel,
    SingleAxisSolarModel,
    DualAxisSolarModel,
)


def solar_load_df(
    solar_id: int,
    start_date: str,
    end_date: str,
    resolution: int,
    strategy: str,
):
    """Returns a polars dataframe."""

    file_owner, filename, data_res = get_file_name_from_id(solar_id)
    file_path = (
        Path(DATA_PATH) / file_owner / "timeseries_data" / (filename + ".csv")
    )

    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist!")

    df = filter_by_date(
        polars.read_csv(file_path, parse_dates=True), start_date, end_date
    )

    if data_res > resolution:
        return {
            "interpolation": upsample_interpolate_df,
            "staircase": upsample_staircase_df,
        }.get(strategy)(df, resolution)

    df_merged = None
    for column in ["ghi", "dhi", "dni"]:
        df_ = downsample_df(df, resolution, column)
        if df_merged is None:
            df_merged = df_
        else:
            df_merged = df_merged.join(df_, on="timestamp")

    return df_merged


def compute_solar_energy_metric(
    solar_power_df: polars.DataFrame, resolution: int
):

    df = populate_sliced_category(solar_power_df)
    solar_metric_df = polars.DataFrame()

    for column in df.columns:
        if column not in ["timestamp", "category"]:

            df_ = (
                df.groupby("category")
                .agg(polars.col(column).sum())
                .with_column(
                    (polars.col(column) * (-resolution / 60)).alias(column)
                )
                .select([column, "category"])
            )

            if not len(solar_metric_df):
                solar_metric_df = df_
            else:
                solar_metric_df = df_.join(
                    solar_metric_df, on="category", how="left"
                )
    return solar_metric_df


def process_solars(
    solars: List[SolarFormData], base_path: str, basic_data: BasicFormData
):
    """Simulates solar."""

    solar_output = {}

    for solar in solars:
        solar_df = solar_load_df(
            solar.irradianceData,
            basic_data.startDate,
            basic_data.endDate,
            basic_data.resolution,
            basic_data.dataFillingStrategy,
        )
        solar_df = solar_df.fill_null(0)
        timestamps = solar_df["timestamp"].to_list()

        if solar.solarInstallationStrategy == "fixed":
            fixed = FixedAxisSolarModel(
                solar_basic_model=SolarBasicModel(
                    longitude=solar.longitude if solar.longitude else 36,
                    latitude=solar.latitude if solar.latitude else 9,
                    kw=solar.solarCapacity,
                    irradiance=solar_df.to_pandas(date_as_object=True),
                ),
                axis_model=FixedAxisModel(
                    surface_tilt=solar.panelTilt,
                    surface_azimuth=solar.panelAzimuth,
                ),
                inv_model=InverterModel(acdcratio=1 / solar.dcacRatio),
            )
            df = fixed.get_inverter_output()
            solar_output[solar.name] = list(df["AC_Output"])

        elif solar.solarInstallationStrategy == "single_axis":
            fixed = SingleAxisSolarModel(
                solar_basic_model=SolarBasicModel(
                    longitude=solar.longitude if solar.longitude else 36,
                    latitude=solar.latitude if solar.latitude else 9,
                    kw=solar.solarCapacity,
                    irradiance=solar_df.to_pandas(date_as_object=True),
                ),
                axis_model=SingleAxisModel(
                    axis_tilt=solar.panelTilt, axis_azimuth=solar.panelAzimuth
                ),
                inv_model=InverterModel(acdcratio=1 / solar.dcacRatio),
            )
            df = fixed.get_inverter_output()
            solar_output[solar.name] = list(df["AC_Output"])

        elif solar.solarInstallationStrategy == "dual_axis":
            fixed = DualAxisSolarModel(
                solar_basic_model=SolarBasicModel(
                    longitude=solar.longitude if solar.longitude else 36,
                    latitude=solar.latitude if solar.latitude else 9,
                    kw=solar.solarCapacity,
                    irradiance=solar_df.to_pandas(date_as_object=True),
                ),
                axis_model=DualAxisModel(),
                inv_model=InverterModel(acdcratio=1 / solar.dcacRatio),
            )
            df = fixed.get_inverter_output()
            solar_output[solar.name] = list(df["AC_Output"])

    if solars:
        solar_output.update({"timestamp": timestamps})
        solar_output_df = polars.from_dict(solar_output)

        solar_metric_df = compute_solar_energy_metric(
            solar_output_df, basic_data.resolution
        )

        solar_output_df.write_csv(base_path / "solar_power_timeseries.csv")

        solar_metric_df_sorted = sort_metric_dataframe(solar_metric_df)
        solar_metric_df_sorted.write_csv(base_path / "solar_metrics.csv")

        return solar_output_df
