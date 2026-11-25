import html

import folium
import pandas as pd
from folium.plugins import HeatMap


def _validate_station_data(
    station_data: pd.DataFrame,
    required: set,
) -> pd.DataFrame:
    """Validate and prepare station data for geographic visualization."""

    missing = required - set(station_data.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if station_data.empty:
        raise ValueError("Station dataset is empty.")

    data = station_data.copy()

    numeric_columns = [
        column
        for column in ["latitude", "longitude", "total_ridership"]
        if column in required
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    data = data.dropna(subset=numeric_columns)

    data = data[
        data["latitude"].between(-90, 90) & data["longitude"].between(-180, 180)
    ].copy()

    data = data[data["total_ridership"] >= 0].copy()

    if data.empty:
        raise ValueError("No valid station records available for mapping.")

    return data


def create_station_ridership_map(
    station_data: pd.DataFrame,
    output_path: str,
) -> None:
    """Create an interactive station map with ridership-scaled markers."""

    required = {
        "station_complex",
        "borough",
        "latitude",
        "longitude",
        "total_ridership",
    }

    data = _validate_station_data(
        station_data,
        required,
    )

    center_lat = data["latitude"].mean()
    center_lon = data["longitude"].mean()

    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    station_layer = folium.FeatureGroup(
        name="Station ridership",
        show=True,
    )

    max_ridership = max(
        float(data["total_ridership"].max()),
        1.0,
    )

    for _, station in data.iterrows():
        ridership = float(station["total_ridership"])

        radius = 4 + 10 * (ridership / max_ridership) ** 0.5

        station_name = html.escape(str(station["station_complex"]))
        borough_name = html.escape(str(station["borough"]))

        popup_html = f"""
        <div style="font-family:Arial;min-width:180px;">
            <b>{station_name}</b>
            <hr>
            <b>Borough:</b> {borough_name}<br>
            <b>Total ridership:</b> {ridership:,.0f}
        </div>
        """

        folium.CircleMarker(
            location=[
                station["latitude"],
                station["longitude"],
            ],
            radius=radius,
            popup=folium.Popup(
                popup_html,
                max_width=300,
            ),
            tooltip=station_name,
            color="#174C3B",
            weight=1,
            fill=True,
            fill_color="#3E8064",
            fill_opacity=0.72,
        ).add_to(station_layer)

    station_layer.add_to(map_object)

    folium.LayerControl(
        collapsed=False,
    ).add_to(map_object)

    map_object.save(str(output_path))


def create_ridership_heatmap(
    station_data: pd.DataFrame,
    output_path: str,
) -> None:
    """Create a geographic heatmap weighted by total station ridership."""

    required = {
        "latitude",
        "longitude",
        "total_ridership",
    }

    data = _validate_station_data(
        station_data,
        required,
    )

    center_lat = data["latitude"].mean()
    center_lon = data["longitude"].mean()

    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    heat_data = data[["latitude", "longitude", "total_ridership"]].values.tolist()

    heat_layer = folium.FeatureGroup(
        name="Ridership heatmap",
        show=True,
    )

    HeatMap(
        heat_data,
        radius=18,
        blur=15,
        min_opacity=0.3,
        max_zoom=13,
    ).add_to(heat_layer)

    heat_layer.add_to(map_object)

    folium.LayerControl(
        collapsed=False,
    ).add_to(map_object)

    map_object.save(str(output_path))
