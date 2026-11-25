import duckdb
import pandas as pd


def get_overall_summary(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate overall monthly dataset statistics."""

    return connection.execute("""
        SELECT
            SUM(ridership) AS total_ridership,
            SUM(transfers) AS total_transfers,
            COUNT(DISTINCT station_complex_id) AS unique_stations,
            COUNT(DISTINCT borough) AS boroughs,
            COUNT(DISTINCT transit_mode) AS transit_modes,
            COUNT(DISTINCT month) AS months,
            AVG(ridership) AS average_station_month_ridership
        FROM monthly
    """).df()


def get_yearly_ridership(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate total ridership and transfers by year."""

    return connection.execute("""
        SELECT
            EXTRACT(YEAR FROM month)::INTEGER AS year,
            SUM(ridership) AS total_ridership,
            SUM(transfers) AS total_transfers
        FROM monthly
        GROUP BY year
        ORDER BY year
    """).df()


def get_monthly_ridership_trend(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate system-wide monthly ridership."""

    return connection.execute("""
        SELECT
            month,
            SUM(ridership) AS total_ridership,
            SUM(transfers) AS total_transfers
        FROM monthly
        GROUP BY month
        ORDER BY month
    """).df()


def get_borough_ridership(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Compare ridership across boroughs."""

    return connection.execute("""
        SELECT
            borough,
            SUM(ridership) AS total_ridership,
            SUM(transfers) AS total_transfers,
            COUNT(DISTINCT station_complex_id) AS unique_stations
        FROM monthly
        GROUP BY borough
        ORDER BY total_ridership DESC
    """).df()


def get_transit_mode_ridership(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Compare ridership across transit modes."""

    return connection.execute("""
        SELECT
            transit_mode,
            SUM(ridership) AS total_ridership,
            SUM(transfers) AS total_transfers,
            COUNT(DISTINCT station_complex_id) AS unique_stations
        FROM monthly
        GROUP BY transit_mode
        ORDER BY total_ridership DESC
    """).df()


def get_top_stations(
    connection: duckdb.DuckDBPyConnection,
    limit: int = 10,
) -> pd.DataFrame:
    """Find the highest-ridership station complexes."""

    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    return connection.execute(
        """
        SELECT
            station_complex_id,
            station_complex,
            borough,
            SUM(ridership) AS total_ridership,
            SUM(transfers) AS total_transfers
        FROM monthly
        GROUP BY
            station_complex_id,
            station_complex,
            borough
        ORDER BY total_ridership DESC
        LIMIT ?
    """,
        [limit],
    ).df()


def get_hourly_day_comparison(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """
    Compare hourly ridership patterns on sampled Wednesdays
    and Saturdays.

    Important: the hourly dataset contains selected dates,
    not continuous hourly observations.
    """

    return connection.execute("""
        SELECT
            EXTRACT(DOW FROM transit_timestamp)::INTEGER
                AS day_of_week,
            STRFTIME(transit_timestamp, '%A') AS day_name,
            EXTRACT(HOUR FROM transit_timestamp)::INTEGER
                AS hour,
            SUM(ridership) AS total_ridership,
            COUNT(DISTINCT CAST(transit_timestamp AS DATE))
                AS sampled_dates
        FROM hourly
        GROUP BY day_of_week, day_name, hour
        ORDER BY day_of_week, hour
    """).df()
