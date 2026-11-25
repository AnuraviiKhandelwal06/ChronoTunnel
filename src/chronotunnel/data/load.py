import duckdb
import pandas as pd
from src.chronotunnel.config.settings import (
    HOURLY_DATA_PATH,
    MONTHLY_DATA_PATH,
    STATION_COORDINATES_PATH,
)

# --------------------------------------------------
# CONNECTION
# --------------------------------------------------


def create_connection() -> duckdb.DuckDBPyConnection:
    """
    Create an in-memory DuckDB connection and register
    the processed MetroPulse datasets as views.
    """

    connection = duckdb.connect(database=":memory:")

    register_datasets(connection)

    return connection


# --------------------------------------------------
# DATASET REGISTRATION
# --------------------------------------------------


def register_datasets(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    """
    Register processed CSV datasets as DuckDB views.
    """

    datasets = {
        "hourly": HOURLY_DATA_PATH,
        "monthly": MONTHLY_DATA_PATH,
        "station_coordinates": STATION_COORDINATES_PATH,
    }

    for view_name, file_path in datasets.items():
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        connection.read_csv(str(file_path)).create_view(
            view_name,
            replace=True,
        )


# --------------------------------------------------
# MONTHLY DATA LOADER
# --------------------------------------------------


def load_monthly_data(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """
    Load the monthly station-level dataset.
    """

    return connection.execute(
        """
        SELECT *
        FROM monthly
        ORDER BY month, station_complex_id
        """
    ).df()


# --------------------------------------------------
# STATION COORDINATE LOADER
# --------------------------------------------------


def load_station_coordinates(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """
    Load the station coordinate reference.
    """

    return connection.execute(
        """
        SELECT *
        FROM station_coordinates
        ORDER BY station_complex_id, transit_mode
        """
    ).df()


# --------------------------------------------------
# HOURLY DATA QUERY
# --------------------------------------------------


def query_hourly_data(
    connection: duckdb.DuckDBPyConnection,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
    station_complex_id: str | None = None,
    transit_mode: str | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    """
    Query hourly ridership without loading the
    complete hourly dataset into pandas.

    All filters are optional.
    """

    conditions = []
    parameters = []

    if start_timestamp is not None:
        conditions.append("transit_timestamp >= ?")
        parameters.append(start_timestamp)

    if end_timestamp is not None:
        conditions.append("transit_timestamp <= ?")
        parameters.append(end_timestamp)

    if station_complex_id is not None:
        conditions.append("station_complex_id = ?")
        parameters.append(str(station_complex_id))

    if transit_mode is not None:
        conditions.append("transit_mode = ?")
        parameters.append(transit_mode)

    query = "SELECT * FROM hourly"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY transit_timestamp"

    if limit is not None:
        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        query += " LIMIT ?"
        parameters.append(limit)

    return connection.execute(
        query,
        parameters,
    ).df()
