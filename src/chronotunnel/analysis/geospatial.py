import duckdb
import pandas as pd


def get_borough_geospatial_summary(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Summarize station locations and ridership by borough."""

    query = """
        SELECT
            borough,
            COUNT(*) AS station_mode_records,
            COUNT(DISTINCT station_complex_id) AS unique_station_ids,
            SUM(total_ridership) AS total_ridership,
            ROUND(AVG(total_ridership), 2) AS average_station_ridership,
            ROUND(
                100.0 * SUM(total_ridership) /
                NULLIF(SUM(SUM(total_ridership)) OVER (), 0),
                2
            ) AS ridership_share_percent
        FROM station_coordinates
        GROUP BY borough
        ORDER BY total_ridership DESC
    """

    return connection.execute(query).df()


def get_top_ridership_locations(
    connection: duckdb.DuckDBPyConnection,
    limit: int = 15,
) -> pd.DataFrame:
    """Identify station locations with the highest total ridership."""

    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    query = """
        SELECT
            station_complex_id,
            transit_mode,
            station_complex,
            borough,
            latitude,
            longitude,
            total_ridership,
            coordinate_variants
        FROM station_coordinates
        ORDER BY total_ridership DESC
        LIMIT ?
    """

    return connection.execute(query, [limit]).df()


def get_borough_weighted_centroids(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate ridership-weighted geographic centers for each borough."""

    query = """
        SELECT
            borough,
            ROUND(
                SUM(latitude * total_ridership) /
                NULLIF(SUM(total_ridership), 0),
                6
            ) AS weighted_latitude,
            ROUND(
                SUM(longitude * total_ridership) /
                NULLIF(SUM(total_ridership), 0),
                6
            ) AS weighted_longitude,
            SUM(total_ridership) AS total_ridership
        FROM station_coordinates
        GROUP BY borough
        ORDER BY total_ridership DESC
    """

    return connection.execute(query).df()


def get_coordinate_quality_summary(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Check coordinate coverage, duplicate keys, and coordinate validity."""

    query = """
        WITH duplicate_keys AS (
            SELECT
                station_complex_id,
                transit_mode
            FROM station_coordinates
            GROUP BY station_complex_id, transit_mode
            HAVING COUNT(*) > 1
        )
        SELECT
            COUNT(*) AS total_records,
            COUNT(DISTINCT station_complex_id) AS unique_station_ids,
            COUNT(DISTINCT (station_complex_id, transit_mode))
                AS unique_station_mode_keys,
            (SELECT COUNT(*) FROM duplicate_keys)
                AS duplicate_station_mode_groups,
            COUNT(*) FILTER (
                WHERE latitude < -90 OR latitude > 90
            ) AS invalid_latitude_records,
            COUNT(*) FILTER (
                WHERE longitude < -180 OR longitude > 180
            ) AS invalid_longitude_records,
            COUNT(*) FILTER (
                WHERE coordinate_variants > 1
            ) AS records_with_multiple_coordinate_variants,
            MAX(coordinate_variants) AS maximum_coordinate_variants
        FROM station_coordinates
    """

    return connection.execute(query).df()
