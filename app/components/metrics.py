import math

import pandas as pd
import streamlit as st

from config import (
    HOURLY_DATA_PATH,
    METRICS_DIR,
    MODE_LABELS,
    load_json_metric,
    load_metric,
    load_monthly_data,
    load_station_coordinates,
)


def compact_number(value: float, digits: int | None = None) -> str:
    """Format a large count for display. The underlying value is unchanged."""

    number = float(value)
    absolute = abs(number)
    if absolute >= 1_000_000_000:
        places = 2 if digits is None else digits
        return f"{number / 1_000_000_000:.{places}f}B"
    if absolute >= 1_000_000:
        places = 1 if digits is None else digits
        return f"{number / 1_000_000:.{places}f}M"
    if absolute >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{number:,.0f}"


def format_p_value(p_value: float) -> str:
    if p_value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(p_value))))
    mantissa = p_value / (10**exponent)
    return f"{mantissa:.2f} × 10^{exponent}"


def short_station_name(name: str) -> str:
    return str(name).split(" (")[0]


def mode_label(mode: str) -> str:
    return MODE_LABELS.get(str(mode), str(mode).replace("_", " ").title())


def require_metrics(filenames: dict[str, str]) -> dict[str, pd.DataFrame]:
    """Load metric files or stop the page with a useful message."""

    loaded: dict[str, pd.DataFrame] = {}
    missing = []
    for key, filename in filenames.items():
        path = METRICS_DIR / filename
        if not path.exists():
            missing.append(str(path))
            continue
        try:
            loaded[key] = load_metric(filename)
        except Exception as error:  # pragma: no cover - surfaced in the UI
            st.error(f"Could not read {filename}: {error}")
            st.stop()
    if missing:
        st.error(
            "Required metric files are missing. Run the existing pipeline "
            "if these outputs have not been generated yet.\n\n" + "\n".join(missing)
        )
        st.stop()
    return loaded


def require_json(filename: str) -> dict:
    path = METRICS_DIR / filename
    if not path.exists():
        st.error(
            f"Required metric file is missing: {path}. "
            "The paired comparison cannot be shown without it."
        )
        st.stop()
    try:
        return load_json_metric(filename)
    except Exception as error:
        st.error(f"Could not read {filename}: {error}")
        st.stop()


@st.cache_data(show_spinner=False)
def load_station_catalog() -> pd.DataFrame:
    """Station-mode catalog. The key is station ID plus transit mode."""

    monthly = load_monthly_data().copy()
    grouped = monthly.groupby(
        ["station_complex_id", "transit_mode", "station_complex", "borough"],
        as_index=False,
    ).agg(
        total_ridership=("ridership", "sum"),
        total_transfers=("transfers", "sum"),
        months_observed=("month", "nunique"),
    )
    coordinates = load_station_coordinates()[
        [
            "station_complex_id",
            "transit_mode",
            "latitude",
            "longitude",
            "coordinate_variants",
        ]
    ]
    catalog = grouped.merge(
        coordinates,
        on=["station_complex_id", "transit_mode"],
        how="left",
    )
    catalog["mode_label"] = catalog["transit_mode"].map(mode_label)
    catalog["label"] = catalog["station_complex"] + " · " + catalog["mode_label"]
    catalog["station_key"] = (
        catalog["station_complex_id"].astype(str) + "|" + catalog["transit_mode"]
    )
    return catalog.sort_values(
        ["total_ridership", "station_complex"],
        ascending=[False, True],
    ).reset_index(drop=True)


@st.cache_data(show_spinner="Preparing the sampled hourly profiles…")
def load_hourly_year_slices() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Year slices of the published hourly definitions.

    Averages are means of observed network-hour totals. Missing station-hour
    rows are not filled with zero before the sum.
    """

    import duckdb

    path = HOURLY_DATA_PATH.resolve().as_posix()
    if not HOURLY_DATA_PATH.exists():
        raise FileNotFoundError(HOURLY_DATA_PATH)

    connection = duckdb.connect()
    profiles = connection.execute(
        f"""
        WITH hourly_totals AS (
            SELECT
                EXTRACT(YEAR FROM CAST(transit_timestamp AS TIMESTAMP))::INTEGER AS year,
                CAST(transit_timestamp AS DATE) AS sample_date,
                EXTRACT(DOW FROM CAST(transit_timestamp AS TIMESTAMP))::INTEGER AS day_of_week,
                STRFTIME(CAST(transit_timestamp AS TIMESTAMP), '%A') AS day_name,
                EXTRACT(HOUR FROM CAST(transit_timestamp AS TIMESTAMP))::INTEGER AS hour,
                SUM(ridership) AS total_ridership
            FROM read_csv_auto('{path}')
            GROUP BY 1, 2, 3, 4, 5
        )
        SELECT
            year,
            day_of_week,
            day_name,
            hour,
            ROUND(AVG(total_ridership), 2) AS average_ridership,
            COUNT(DISTINCT sample_date) AS sampled_dates
        FROM hourly_totals
        WHERE day_of_week IN (3, 6)
        GROUP BY 1, 2, 3, 4
        ORDER BY 1, 2, 4
        """
    ).df()
    peaks = connection.execute(
        f"""
        WITH daily_hourly AS (
            SELECT
                EXTRACT(YEAR FROM CAST(transit_timestamp AS TIMESTAMP))::INTEGER AS year,
                CAST(transit_timestamp AS DATE) AS sample_date,
                EXTRACT(DOW FROM CAST(transit_timestamp AS TIMESTAMP))::INTEGER AS day_of_week,
                EXTRACT(HOUR FROM CAST(transit_timestamp AS TIMESTAMP))::INTEGER AS hour,
                SUM(ridership) AS hourly_ridership
            FROM read_csv_auto('{path}')
            GROUP BY 1, 2, 3, 4
        ),
        daily_totals AS (
            SELECT
                year,
                sample_date,
                day_of_week,
                SUM(hourly_ridership) AS daily_ridership,
                SUM(
                    CASE
                        WHEN hour BETWEEN 7 AND 9 OR hour BETWEEN 16 AND 18
                        THEN hourly_ridership ELSE 0
                    END
                ) AS peak_period_ridership
            FROM daily_hourly
            GROUP BY 1, 2, 3
        )
        SELECT
            year,
            day_of_week,
            CASE
                WHEN day_of_week = 3 THEN 'Wednesday'
                WHEN day_of_week = 6 THEN 'Saturday'
            END AS day_name,
            COUNT(*) AS sampled_dates,
            ROUND(AVG(daily_ridership), 2) AS average_daily_ridership,
            ROUND(AVG(peak_period_ridership), 2) AS average_peak_period_ridership,
            ROUND(
                100.0 * SUM(peak_period_ridership) / NULLIF(SUM(daily_ridership), 0),
                2
            ) AS ridership_weighted_peak_share_percent,
            ROUND(
                AVG(100.0 * peak_period_ridership / NULLIF(daily_ridership, 0)),
                2
            ) AS average_daily_peak_share_percent
        FROM daily_totals
        WHERE day_of_week IN (3, 6)
        GROUP BY year, day_of_week
        ORDER BY year, day_of_week
        """
    ).df()
    connection.close()
    return profiles, peaks
