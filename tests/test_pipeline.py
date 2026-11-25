import json
from unittest.mock import MagicMock

import pandas as pd
import pytest
import src.chronotunnel.pipeline.run as pipeline


@pytest.fixture
def mock_pipeline(monkeypatch, tmp_path):
    """Mock pipeline dependencies and use temporary output folders."""

    figures_dir = tmp_path / "figures"
    maps_dir = tmp_path / "maps"
    metrics_dir = tmp_path / "metrics"

    monkeypatch.setattr(pipeline, "FIGURES_DIR", figures_dir)
    monkeypatch.setattr(pipeline, "MAPS_DIR", maps_dir)
    monkeypatch.setattr(pipeline, "METRICS_DIR", metrics_dir)

    connection = MagicMock()

    station_coordinates = pd.DataFrame(
        {
            "station_complex_id": [101],
            "transit_mode": ["subway"],
            "latitude": [40.75],
            "longitude": [-73.99],
        }
    )

    connection.execute.return_value.df.return_value = station_coordinates

    monkeypatch.setattr(
        pipeline,
        "create_connection",
        lambda: connection,
    )

    validation = pd.DataFrame(
        {
            "check": ["test validation"],
            "status": ["PASS"],
            "actual": [0],
            "expected": [0],
        }
    )

    monkeypatch.setattr(
        pipeline,
        "run_data_validation",
        lambda conn: validation,
    )

    # Mock all analysis functions.
    analysis_functions = [
        "get_yearly_ridership",
        "get_monthly_ridership_trend",
        "get_borough_ridership",
        "get_transit_mode_ridership",
        "get_top_stations",
        "get_year_over_year_growth",
        "get_monthly_seasonality",
        "get_weekday_weekend_comparison",
        "get_peak_hour_concentration",
        "get_ridership_distribution",
        "get_borough_statistics",
        "get_transit_mode_statistics",
        "get_borough_geospatial_summary",
        "get_top_ridership_locations",
        "get_borough_weighted_centroids",
        "get_coordinate_quality_summary",
    ]

    for function_name in analysis_functions:
        monkeypatch.setattr(
            pipeline,
            function_name,
            lambda *args, **kwargs: pd.DataFrame(
                {
                    "metric": [1],
                }
            ),
        )

    monkeypatch.setattr(
        pipeline,
        "compare_paired_weekday_weekend_ridership",
        lambda conn: {"p_value": 0.01},
    )

    # Mock visualization functions.
    visualization_functions = [
        "create_station_ridership_map",
        "create_ridership_heatmap",
        "create_borough_ridership_chart",
        "create_top_stations_chart",
        "create_hourly_ridership_chart",
        "create_monthly_ridership_chart",
    ]

    for function_name in visualization_functions:
        monkeypatch.setattr(
            pipeline,
            function_name,
            MagicMock(),
        )

    return {
        "connection": connection,
        "figures_dir": figures_dir,
        "maps_dir": maps_dir,
        "metrics_dir": metrics_dir,
    }


def test_pipeline_completes_successfully(mock_pipeline):
    pipeline.run_pipeline()

    mock_pipeline["connection"].close.assert_called_once()


def test_pipeline_creates_output_directories(mock_pipeline):
    pipeline.run_pipeline()

    assert mock_pipeline["figures_dir"].exists()
    assert mock_pipeline["maps_dir"].exists()
    assert mock_pipeline["metrics_dir"].exists()


def test_pipeline_saves_validation_report(mock_pipeline):
    pipeline.run_pipeline()

    report_path = mock_pipeline["metrics_dir"] / "data_validation.csv"

    assert report_path.exists()

    report = pd.read_csv(report_path)

    assert "status" in report.columns
    assert report.iloc[0]["status"] == "PASS"


def test_pipeline_saves_analysis_metrics(mock_pipeline):
    pipeline.run_pipeline()

    expected_files = [
        "yearly_ridership.csv",
        "monthly_ridership.csv",
        "borough_ridership.csv",
        "transit_mode_ridership.csv",
        "top_stations.csv",
        "year_over_year_growth.csv",
        "monthly_seasonality.csv",
        "weekday_weekend_comparison.csv",
        "peak_hour_concentration.csv",
        "ridership_distribution.csv",
        "borough_statistics.csv",
        "transit_mode_statistics.csv",
        "borough_summary.csv",
        "top_locations.csv",
        "weighted_centroids.csv",
        "coordinate_quality.csv",
    ]

    for filename in expected_files:
        assert (mock_pipeline["metrics_dir"] / filename).exists(), (
            f"Missing output: {filename}"
        )


def test_pipeline_saves_paired_comparison_json(mock_pipeline):
    pipeline.run_pipeline()

    json_path = mock_pipeline["metrics_dir"] / "paired_weekday_weekend_comparison.json"

    assert json_path.exists()

    with open(json_path, encoding="utf-8") as file:
        result = json.load(file)

    assert result["p_value"] == 0.01


def test_pipeline_stops_when_validation_fails(
    mock_pipeline,
    monkeypatch,
):
    failed_validation = pd.DataFrame(
        {
            "check": ["test validation"],
            "status": ["FAIL"],
            "actual": [5],
            "expected": [0],
        }
    )

    monkeypatch.setattr(
        pipeline,
        "run_data_validation",
        lambda conn: failed_validation,
    )

    with pytest.raises(
        RuntimeError,
        match="Data validation failed",
    ):
        pipeline.run_pipeline()

    mock_pipeline["connection"].close.assert_called_once()


def test_pipeline_closes_connection_on_analysis_error(
    mock_pipeline,
    monkeypatch,
):
    def raise_error(connection):
        raise ValueError("Simulated analysis failure")

    monkeypatch.setattr(
        pipeline,
        "get_yearly_ridership",
        raise_error,
    )

    with pytest.raises(
        ValueError,
        match="Simulated analysis failure",
    ):
        pipeline.run_pipeline()

    mock_pipeline["connection"].close.assert_called_once()
