""" This module contains helper functions. """

# Standard imports
import datetime
import os

# Third-party imports
import polars

# Internal imports
from dotenv import load_dotenv
from processor.postgres_db_context import PostGresDB


load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": str(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME"),
}
DATA_PATH = os.getenv("DATA_PATH")


def populate_sliced_category(df: polars.DataFrame):

    start_date = df.select(polars.col("timestamp")).min()[0, 0]
    end_date = df.select(polars.col("timestamp")).max()[0, 0]
    duration_hr = (end_date - start_date).total_seconds() / 3600

    # Data is more than one month makes sense to aggregate by months
    if duration_hr >= 960:
        format_code = "%b"
    elif duration_hr < 960 and duration_hr > 168:
        format_code = "%W"
    elif duration_hr <= 168 and duration_hr > 24:
        format_code = "%a"
    elif duration_hr < 24:
        format_code = "%I %p"
    else:
        format_code = "%Y"

    return df.with_column(
        polars.col("timestamp")
        .apply(lambda x: x.strftime(format_code))
        .alias("category")
    )


def upsample_interpolate_df(df: polars.DataFrame, resolution: int):
    return (
        df.upsample("timestamp", every=f"{resolution}m")
        .interpolate()
        .fill_null("forward")
    )


def upsample_staircase_df(df: polars.DataFrame, resolution: int):
    return df.upsample("timestamp", every=f"{resolution}m").select(
        polars.all().forward_fill()
    )


def downsample_df(df: polars.DataFrame, resolution: int, column_name: str):
    return df.groupby_dynamic("timestamp", every=f"{resolution}m").agg(
        polars.col(column_name).mean()
    )


def filter_by_date(
    df: polars.DataFrame, start_date: datetime.date, end_date: datetime.date
):
    return df.filter(
        (polars.col("timestamp") > start_date)
        & (polars.col("timestamp") < end_date)
    )


def get_file_name_from_id(id: int):
    """Get the filename."""
    with PostGresDB(DB_CONFIG) as cursor:
        cursor.execute(
            f"""select users.username, timeseriesdata.filename, timeseriesdata.resolution_min 
                from timeseriesdata 
                inner join users 
                on timeseriesdata.user_id = users.id
                where timeseriesdata.id=%s""",
            [id],
        )
        record = cursor.fetchone()
    return record
