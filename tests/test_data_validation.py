import duckdb
import pandas as pd
import pytest
from src.chronotunnel.data.validate import run_data_validation


@pytest.fixture
def connection():
    """Create small in-memory datasets for validation tests."""
    conn = duckdb.connect(database=":memory:")

    conn.execute("""
        CREATE TABLE hourly (
            transit_timestamp TIMESTAMP,
            transit_mode VARCHAR,
            station_complex_id INTEGER,
            ridership BIGINT,
            transfers BIGINT,
            latitude DOUBLE,
            longitude DOUBLE
        )
    """)

    conn.execute("""
        CREATE TABLE monthly (
            month DATE,
            transit_mode VARCHAR,
            station_complex_id INTEGER,
            ridership BIGINT,
            transfers BIGINT,
            latitude DOUBLE,
            longitude DOUBLE
        )
    """)

    conn.execute("""
        CREATE TABLE station_coordinates (
            station_complex_id INTEGER,
            transit_mode VARCHAR,
            latitude DOUBLE,
            longitude DOUBLE
        )
    """)

    # One valid hourly record.
    conn.execute("""
        INSERT INTO hourly VALUES
        ('2024-01-06 08:00:00', 'subway', 101,
         1000, 100, 40.7500, -73.9900)
    """)

    # One valid monthly record.
    conn.execute("""
        INSERT INTO monthly VALUES
        ('2024-01-01', 'subway', 101,
         25000, 2500, 40.7500, -73.9900)
    """)

    # Matching station coordinate.
    conn.execute("""
        INSERT INTO station_coordinates VALUES
        (101, 'subway', 40.7500, -73.9900)
    """)

    yield conn
    conn.close()


def get_status(report, check_name):
    """Return the status for a specific validation check."""
    result = report.loc[report["check"] == check_name, "status"]

    assert not result.empty, f"Missing validation check: {check_name}"

    return result.iloc[0]


def test_validation_returns_dataframe(connection):
    report = run_data_validation(connection)

    assert isinstance(report, pd.DataFrame)
    assert {
        "check",
        "status",
        "actual",
        "expected",
    }.issubset(report.columns)


def test_valid_data_passes_validation(connection):
    report = run_data_validation(connection)

    required_checks = [
        "hourly: required columns",
        "monthly: required columns",
        "station_coordinates: required columns",
        "hourly: missing required values",
        "monthly: missing required values",
        "station_coordinates: missing required values",
        "hourly: negative ridership/transfers",
        "monthly: negative ridership/transfers",
        "hourly: invalid coordinates",
        "monthly: invalid coordinates",
        "station_coordinates: invalid coordinates",
        "hourly: duplicate analytical groups",
        "monthly: duplicate analytical groups",
        "station_coordinates: duplicate analytical groups",
        "hourly: missing coordinate matches",
        "monthly: missing coordinate matches",
    ]

    for check in required_checks:
        assert get_status(report, check) == "PASS"


def test_missing_required_column_is_detected(connection):
    connection.execute("""
        ALTER TABLE hourly
        DROP COLUMN transfers
    """)

    report = run_data_validation(connection)

    assert get_status(report, "hourly: required columns") == "FAIL"

    assert get_status(report, "hourly: missing required values") == "SKIPPED"


def test_null_values_are_detected(connection):
    connection.execute("""
        INSERT INTO hourly VALUES
        ('2024-01-07 08:00:00', 'subway', 101,
         NULL, 100, 40.7500, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "hourly: missing required values") == "FAIL"


def test_negative_ridership_is_detected(connection):
    connection.execute("""
        INSERT INTO hourly VALUES
        ('2024-01-07 08:00:00', 'subway', 101,
         -100, 10, 40.7500, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "hourly: negative ridership/transfers") == "FAIL"


def test_negative_transfers_are_detected(connection):
    connection.execute("""
        INSERT INTO monthly VALUES
        ('2024-02-01', 'subway', 101,
         1000, -10, 40.7500, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "monthly: negative ridership/transfers") == "FAIL"


def test_invalid_coordinates_are_detected(connection):
    connection.execute("""
        INSERT INTO station_coordinates VALUES
        (102, 'subway', 95.0, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "station_coordinates: invalid coordinates") == "FAIL"


def test_duplicate_hourly_groups_are_detected(connection):
    connection.execute("""
        INSERT INTO hourly VALUES
        ('2024-01-06 08:00:00', 'subway', 101,
         2000, 200, 40.7500, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "hourly: duplicate analytical groups") == "FAIL"


def test_duplicate_monthly_groups_are_detected(connection):
    connection.execute("""
        INSERT INTO monthly VALUES
        ('2024-01-01', 'subway', 101,
         30000, 3000, 40.7500, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "monthly: duplicate analytical groups") == "FAIL"


def test_missing_coordinate_match_is_detected(connection):
    connection.execute("""
        INSERT INTO hourly VALUES
        ('2024-01-07 08:00:00', 'subway', 999,
         500, 50, 40.7500, -73.9900)
    """)

    report = run_data_validation(connection)

    assert get_status(report, "hourly: missing coordinate matches") == "FAIL"


def test_hourly_temporal_coverage_is_checked(connection):
    report = run_data_validation(connection)

    assert get_status(report, "hourly: distinct sampled dates") == "FAIL"


def test_monthly_temporal_coverage_is_checked(connection):
    report = run_data_validation(connection)

    assert get_status(report, "monthly: distinct months") == "FAIL"
