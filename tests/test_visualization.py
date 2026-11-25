import pandas as pd
import pytest
from src.chronotunnel.visualization.charts import (
    create_borough_ridership_chart,
    create_hourly_ridership_chart,
    create_monthly_ridership_chart,
    create_top_stations_chart,
)
from src.chronotunnel.visualization.maps import (
    create_ridership_heatmap,
    create_station_ridership_map,
)


def _assert_plotly_chart(
    chart_function,
    data,
    tmp_path,
    filename,
):
    output_path = tmp_path / filename

    chart_function(data, str(output_path))

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    html_content = output_path.read_text(encoding="utf-8")

    assert "plotly.min.js" in html_content
    assert (tmp_path / "plotly.min.js").exists()


def test_borough_ridership_chart_generation(tmp_path):
    data = pd.DataFrame(
        {
            "borough": ["Manhattan", "Brooklyn"],
            "total_ridership": [1000000, 750000],
        }
    )

    _assert_plotly_chart(
        create_borough_ridership_chart,
        data,
        tmp_path,
        "borough_ridership.html",
    )


def test_top_stations_chart_generation(tmp_path):
    data = pd.DataFrame(
        {
            "station_complex": [
                "Times Sq-42 St",
                "Grand Central-42 St",
            ],
            "borough": ["Manhattan", "Manhattan"],
            "total_ridership": [500000, 350000],
        }
    )

    _assert_plotly_chart(
        create_top_stations_chart,
        data,
        tmp_path,
        "top_stations.html",
    )


def test_hourly_ridership_chart_generation(tmp_path):
    data = pd.DataFrame(
        {
            "hour": [7, 8, 9, 10],
            "average_ridership": [
                120000,
                150000,
                140000,
                90000,
            ],
            "day_name": [
                "Wednesday",
                "Wednesday",
                "Saturday",
                "Saturday",
            ],
        }
    )

    _assert_plotly_chart(
        create_hourly_ridership_chart,
        data,
        tmp_path,
        "hourly_ridership.html",
    )


def test_monthly_ridership_chart_generation(tmp_path):
    data = pd.DataFrame(
        {
            "month": [
                "2024-01-01",
                "2024-02-01",
                "2024-03-01",
            ],
            "total_ridership": [
                1000000,
                1100000,
                1250000,
            ],
        }
    )

    _assert_plotly_chart(
        create_monthly_ridership_chart,
        data,
        tmp_path,
        "monthly_ridership.html",
    )


def test_station_ridership_map_generation(tmp_path):
    data = pd.DataFrame(
        {
            "station_complex": ["Times Sq-42 St"],
            "borough": ["Manhattan"],
            "latitude": [40.755],
            "longitude": [-73.987],
            "total_ridership": [500000],
        }
    )

    output_path = tmp_path / "station_map.html"

    create_station_ridership_map(
        data,
        str(output_path),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    html_content = output_path.read_text(encoding="utf-8")

    assert "Times Sq-42 St" in html_content
    assert "tile.openstreetmap.org" in html_content


def test_station_map_escapes_html_values(tmp_path):
    data = pd.DataFrame(
        {
            "station_complex": ["<script>alert('test')</script>"],
            "borough": ["Queens & Brooklyn"],
            "latitude": [40.755],
            "longitude": [-73.987],
            "total_ridership": [100000],
        }
    )

    output_path = tmp_path / "escaped_station_map.html"

    create_station_ridership_map(
        data,
        str(output_path),
    )

    html_content = output_path.read_text(encoding="utf-8")

    assert "&lt;script&gt;" in html_content
    assert "<script>alert('test')</script>" not in html_content
    assert "Queens &amp; Brooklyn" in html_content


def test_ridership_heatmap_generation(tmp_path):
    data = pd.DataFrame(
        {
            "latitude": [40.755, 40.748],
            "longitude": [-73.987, -73.985],
            "total_ridership": [500000, 350000],
        }
    )

    output_path = tmp_path / "ridership_heatmap.html"

    create_ridership_heatmap(
        data,
        str(output_path),
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    html_content = output_path.read_text(encoding="utf-8")

    assert "tile.openstreetmap.org" in html_content
    assert "heatLayer" in html_content


def test_station_map_rejects_invalid_coordinates(tmp_path):
    data = pd.DataFrame(
        {
            "station_complex": ["Invalid Station"],
            "borough": ["Manhattan"],
            "latitude": [100.0],
            "longitude": [-73.987],
            "total_ridership": [100000],
        }
    )

    output_path = tmp_path / "invalid_map.html"

    with pytest.raises(
        ValueError,
        match="No valid station records",
    ):
        create_station_ridership_map(
            data,
            str(output_path),
        )
