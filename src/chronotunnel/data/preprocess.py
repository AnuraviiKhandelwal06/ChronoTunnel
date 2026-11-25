import pandas as pd


def prepare_hourly_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare hourly ridership data for analysis.

    Adds date, hour, weekday, month, year, and weekend features.
    Preserves all original columns.
    """
    required_columns = [
        "transit_timestamp",
        "station_complex_id",
        "transit_mode",
        "ridership",
        "transfers",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Hourly data is missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("Hourly data is empty.")

    data = df.copy()

    data["transit_timestamp"] = pd.to_datetime(
        data["transit_timestamp"], errors="raise"
    )

    if data["transit_timestamp"].isna().any():
        raise ValueError("Hourly data contains missing transit timestamps.")

    data["date"] = data["transit_timestamp"].dt.date
    data["hour"] = data["transit_timestamp"].dt.hour
    data["day_of_week"] = data["transit_timestamp"].dt.day_of_week
    data["day_name"] = data["transit_timestamp"].dt.day_name()
    data["month"] = data["transit_timestamp"].dt.month
    data["month_name"] = data["transit_timestamp"].dt.month_name()
    data["year"] = data["transit_timestamp"].dt.year
    data["is_weekend"] = data["day_of_week"].isin([5, 6])

    data = data.sort_values(
        by=[
            "transit_timestamp",
            "station_complex_id",
            "transit_mode",
        ]
    ).reset_index(drop=True)

    return data


def prepare_monthly_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare monthly ridership data for analysis.

    Adds year, month number, and month name features.
    Preserves all original columns.
    """
    required_columns = [
        "month",
        "station_complex_id",
        "transit_mode",
        "ridership",
        "transfers",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Monthly data is missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("Monthly data is empty.")

    data = df.copy()

    data["month"] = pd.to_datetime(data["month"], errors="raise")

    if data["month"].isna().any():
        raise ValueError("Monthly data contains missing month values.")

    data["year"] = data["month"].dt.year
    data["month_number"] = data["month"].dt.month
    data["month_name"] = data["month"].dt.month_name()

    data = data.sort_values(
        by=[
            "month",
            "station_complex_id",
            "transit_mode",
        ]
    ).reset_index(drop=True)

    return data
