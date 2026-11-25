import pandas as pd
import pytest
from src.chronotunnel.data.preprocess import (
    prepare_hourly_data,
    prepare_monthly_data,
)


@pytest.fixture
def hourly_sample():
    return pd.DataFrame(
        {
            "transit_timestamp": [
                "2024-01-06 09:00:00",
                "2024-01-05 08:00:00",
                "2024-01-07 10:00:00",
            ],
            "station_complex_id": [101, 101, 102],
            "transit_mode": ["subway", "subway", "subway"],
            "ridership": [1000, 1500, 800],
            "transfers": [100, 150, 80],
        }
    )


@pytest.fixture
def monthly_sample():
    return pd.DataFrame(
        {
            "month": [
                "2024-02-01",
                "2024-01-01",
                "2024-03-01",
            ],
            "station_complex_id": [101, 101, 102],
            "transit_mode": ["subway", "subway", "subway"],
            "ridership": [2000, 1500, 2500],
            "transfers": [200, 150, 250],
        }
    )


def test_prepare_hourly_data_generates_features(hourly_sample):
    result = prepare_hourly_data(hourly_sample)

    expected_columns = [
        "date",
        "hour",
        "day_of_week",
        "day_name",
        "month",
        "month_name",
        "year",
        "is_weekend",
    ]

    for column in expected_columns:
        assert column in result.columns

    assert result["year"].eq(2024).all()


def test_prepare_hourly_data_classifies_weekends(hourly_sample):
    result = prepare_hourly_data(hourly_sample)

    weekend_values = result.set_index("day_name")["is_weekend"]

    assert not weekend_values["Friday"]
    assert weekend_values["Saturday"]
    assert weekend_values["Sunday"]


def test_prepare_hourly_data_sorts_timestamps(hourly_sample):
    result = prepare_hourly_data(hourly_sample)

    assert result["transit_timestamp"].is_monotonic_increasing


def test_prepare_hourly_data_preserves_original_columns(hourly_sample):
    result = prepare_hourly_data(hourly_sample)

    for column in hourly_sample.columns:
        assert column in result.columns


def test_prepare_hourly_data_rejects_missing_columns():
    invalid_data = pd.DataFrame(
        {
            "transit_timestamp": ["2024-01-01 08:00:00"],
        }
    )

    with pytest.raises(ValueError, match="missing required columns"):
        prepare_hourly_data(invalid_data)


def test_prepare_hourly_data_rejects_empty_input():
    empty_data = pd.DataFrame(
        columns=[
            "transit_timestamp",
            "station_complex_id",
            "transit_mode",
            "ridership",
            "transfers",
        ]
    )

    with pytest.raises(ValueError, match="empty"):
        prepare_hourly_data(empty_data)


def test_prepare_monthly_data_generates_features(monthly_sample):
    result = prepare_monthly_data(monthly_sample)

    expected_columns = [
        "year",
        "month_number",
        "month_name",
    ]

    for column in expected_columns:
        assert column in result.columns

    assert result["year"].eq(2024).all()


def test_prepare_monthly_data_converts_month_to_datetime(monthly_sample):
    result = prepare_monthly_data(monthly_sample)

    assert pd.api.types.is_datetime64_any_dtype(result["month"])


def test_prepare_monthly_data_sorts_months(monthly_sample):
    result = prepare_monthly_data(monthly_sample)

    assert result["month"].is_monotonic_increasing


def test_prepare_monthly_data_preserves_original_columns(monthly_sample):
    result = prepare_monthly_data(monthly_sample)

    for column in monthly_sample.columns:
        assert column in result.columns


def test_prepare_monthly_data_rejects_missing_columns():
    invalid_data = pd.DataFrame(
        {
            "month": ["2024-01-01"],
        }
    )

    with pytest.raises(ValueError, match="missing required columns"):
        prepare_monthly_data(invalid_data)


def test_prepare_monthly_data_rejects_empty_input():
    empty_data = pd.DataFrame(
        columns=[
            "month",
            "station_complex_id",
            "transit_mode",
            "ridership",
            "transfers",
        ]
    )

    with pytest.raises(ValueError, match="empty"):
        prepare_monthly_data(empty_data)
