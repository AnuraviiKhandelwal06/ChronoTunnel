import duckdb
import pandas as pd


def _get_scalar(
    connection: duckdb.DuckDBPyConnection,
    query: str,
) -> int:
    """Execute a query that returns one numeric value."""
    return int(connection.execute(query).fetchone()[0])


def run_data_validation(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """
    Run structural and analytical validation checks
    on the ChronoTunnel datasets.

    Returns a report containing each check, its result,
    actual value, and expected value.
    """

    results = []

    def add_check(name, passed, actual, expected):
        results.append(
            {
                "check": name,
                "status": "PASS" if passed else "FAIL",
                "actual": actual,
                "expected": expected,
            }
        )

    def add_skipped(name, reason):
        results.append(
            {
                "check": name,
                "status": "SKIPPED",
                "actual": reason,
                "expected": "Check requires all required columns",
            }
        )

    # --------------------------------------------------
    # 1. REQUIRED COLUMNS
    # --------------------------------------------------

    required_columns = {
        "hourly": {
            "transit_timestamp",
            "transit_mode",
            "station_complex_id",
            "ridership",
            "transfers",
            "latitude",
            "longitude",
        },
        "monthly": {
            "month",
            "transit_mode",
            "station_complex_id",
            "ridership",
            "transfers",
            "latitude",
            "longitude",
        },
        "station_coordinates": {
            "station_complex_id",
            "transit_mode",
            "latitude",
            "longitude",
        },
    }

    available_columns = {}

    for dataset, required in required_columns.items():
        actual = {
            row[0]
            for row in connection.execute(
                f"DESCRIBE SELECT * FROM {dataset}"
            ).fetchall()
        }

        available_columns[dataset] = actual

        missing = required - actual

        add_check(
            f"{dataset}: required columns",
            len(missing) == 0,
            "All present" if not missing else sorted(missing),
            "All required columns present",
        )

    # --------------------------------------------------
    # 2. NULL VALUE CHECKS
    # --------------------------------------------------

    null_checks = {
        "hourly": {
            "columns": {
                "transit_timestamp",
                "transit_mode",
                "station_complex_id",
                "ridership",
                "transfers",
                "latitude",
                "longitude",
            },
            "query": """
                SELECT COUNT(*)
                FROM hourly
                WHERE transit_timestamp IS NULL
                   OR transit_mode IS NULL
                   OR station_complex_id IS NULL
                   OR ridership IS NULL
                   OR transfers IS NULL
                   OR latitude IS NULL
                   OR longitude IS NULL
            """,
        },
        "monthly": {
            "columns": {
                "month",
                "transit_mode",
                "station_complex_id",
                "ridership",
                "transfers",
                "latitude",
                "longitude",
            },
            "query": """
                SELECT COUNT(*)
                FROM monthly
                WHERE month IS NULL
                   OR transit_mode IS NULL
                   OR station_complex_id IS NULL
                   OR ridership IS NULL
                   OR transfers IS NULL
                   OR latitude IS NULL
                   OR longitude IS NULL
            """,
        },
        "station_coordinates": {
            "columns": {
                "station_complex_id",
                "transit_mode",
                "latitude",
                "longitude",
            },
            "query": """
                SELECT COUNT(*)
                FROM station_coordinates
                WHERE station_complex_id IS NULL
                   OR transit_mode IS NULL
                   OR latitude IS NULL
                   OR longitude IS NULL
            """,
        },
    }

    for dataset, check in null_checks.items():
        if not check["columns"].issubset(available_columns[dataset]):
            add_skipped(
                f"{dataset}: missing required values",
                "Required columns are missing",
            )
            continue

        null_count = _get_scalar(
            connection,
            check["query"],
        )

        add_check(
            f"{dataset}: missing required values",
            null_count == 0,
            null_count,
            0,
        )

    # --------------------------------------------------
    # 3. NEGATIVE RIDERSHIP AND TRANSFERS
    # --------------------------------------------------

    for dataset in ["hourly", "monthly"]:
        required = {"ridership", "transfers"}

        if not required.issubset(available_columns[dataset]):
            add_skipped(
                f"{dataset}: negative ridership/transfers",
                "Required columns are missing",
            )
            continue

        invalid_count = _get_scalar(
            connection,
            f"""
            SELECT COUNT(*)
            FROM {dataset}
            WHERE ridership < 0
               OR transfers < 0
            """,
        )

        add_check(
            f"{dataset}: negative ridership/transfers",
            invalid_count == 0,
            invalid_count,
            0,
        )

    # --------------------------------------------------
    # 4. COORDINATE RANGE CHECKS
    # --------------------------------------------------

    coordinate_columns = {
        "latitude",
        "longitude",
    }

    for dataset in [
        "hourly",
        "monthly",
        "station_coordinates",
    ]:
        if not coordinate_columns.issubset(available_columns[dataset]):
            add_skipped(
                f"{dataset}: invalid coordinates",
                "Required coordinate columns are missing",
            )
            continue

        invalid_count = _get_scalar(
            connection,
            f"""
            SELECT COUNT(*)
            FROM {dataset}
            WHERE latitude NOT BETWEEN -90 AND 90
               OR longitude NOT BETWEEN -180 AND 180
            """,
        )

        add_check(
            f"{dataset}: invalid coordinates",
            invalid_count == 0,
            invalid_count,
            0,
        )

    # --------------------------------------------------
    # 5. DUPLICATE ANALYTICAL GROUPS
    # --------------------------------------------------

    duplicate_checks = {
        "hourly": {
            "columns": {
                "transit_timestamp",
                "transit_mode",
                "station_complex_id",
            },
            "query": """
                SELECT COUNT(*)
                FROM (
                    SELECT
                        transit_timestamp,
                        transit_mode,
                        station_complex_id
                    FROM hourly
                    GROUP BY
                        transit_timestamp,
                        transit_mode,
                        station_complex_id
                    HAVING COUNT(*) > 1
                )
            """,
        },
        "monthly": {
            "columns": {
                "month",
                "transit_mode",
                "station_complex_id",
            },
            "query": """
                SELECT COUNT(*)
                FROM (
                    SELECT
                        month,
                        transit_mode,
                        station_complex_id
                    FROM monthly
                    GROUP BY
                        month,
                        transit_mode,
                        station_complex_id
                    HAVING COUNT(*) > 1
                )
            """,
        },
        "station_coordinates": {
            "columns": {
                "station_complex_id",
                "transit_mode",
            },
            "query": """
                SELECT COUNT(*)
                FROM (
                    SELECT
                        station_complex_id,
                        transit_mode
                    FROM station_coordinates
                    GROUP BY
                        station_complex_id,
                        transit_mode
                    HAVING COUNT(*) > 1
                )
            """,
        },
    }

    for dataset, check in duplicate_checks.items():
        if not check["columns"].issubset(available_columns[dataset]):
            add_skipped(
                f"{dataset}: duplicate analytical groups",
                "Required columns are missing",
            )
            continue

        duplicate_count = _get_scalar(
            connection,
            check["query"],
        )

        add_check(
            f"{dataset}: duplicate analytical groups",
            duplicate_count == 0,
            duplicate_count,
            0,
        )

    # --------------------------------------------------
    # 6. COORDINATE COVERAGE USING COMPOSITE KEYS
    # --------------------------------------------------

    for dataset in ["hourly", "monthly"]:
        required = {
            "station_complex_id",
            "transit_mode",
        }

        if not required.issubset(available_columns[dataset]) or not required.issubset(
            available_columns["station_coordinates"]
        ):
            add_skipped(
                f"{dataset}: missing coordinate matches",
                "Required station identity columns are missing",
            )
            continue

        missing_count = _get_scalar(
            connection,
            f"""
            SELECT COUNT(*)
            FROM (
                SELECT DISTINCT
                    d.station_complex_id,
                    d.transit_mode
                FROM {dataset} d
                LEFT JOIN station_coordinates c
                    ON d.station_complex_id = c.station_complex_id
                    AND d.transit_mode = c.transit_mode
                WHERE c.station_complex_id IS NULL
            )
            """,
        )

        add_check(
            f"{dataset}: missing coordinate matches",
            missing_count == 0,
            missing_count,
            0,
        )

    # --------------------------------------------------
    # 7. TEMPORAL COVERAGE
    # --------------------------------------------------

    if "transit_timestamp" not in available_columns["hourly"]:
        add_skipped(
            "hourly: distinct sampled dates",
            "transit_timestamp column is missing",
        )
    else:
        hourly_dates = _get_scalar(
            connection,
            """
            SELECT COUNT(DISTINCT CAST(transit_timestamp AS DATE))
            FROM hourly
            """,
        )

        add_check(
            "hourly: distinct sampled dates",
            hourly_dates == 120,
            hourly_dates,
            120,
        )

    if "month" not in available_columns["monthly"]:
        add_skipped(
            "monthly: distinct months",
            "month column is missing",
        )
    else:
        monthly_count = _get_scalar(
            connection,
            """
            SELECT COUNT(DISTINCT month)
            FROM monthly
            """,
        )

        add_check(
            "monthly: distinct months",
            monthly_count == 60,
            monthly_count,
            60,
        )

    # --------------------------------------------------
    # 8. FINAL REPORT
    # --------------------------------------------------

    return pd.DataFrame(results)
