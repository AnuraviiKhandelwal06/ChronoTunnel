import sys
from html import escape
from pathlib import Path

import folium
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from folium.plugins import HeatMap

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------
# PROJECT IMPORTS
# --------------------------------------------------

from src.chronotunnel.analysis.geospatial import (
    get_borough_geospatial_summary,
    get_borough_weighted_centroids,
    get_coordinate_quality_summary,
    get_top_ridership_locations,
)
from src.chronotunnel.data.load import create_connection

from components.sidebar import mount_dashboard

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Geospatial Analysis | ChronoTunnel",
    page_icon="◆",
    layout="wide",
)

mount_dashboard()

# --------------------------------------------------
# CHRONOTUNNEL WIDGET STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* =============================================
       CHRONOTUNNEL — SELECTBOX CLOSED CONTROL
    ============================================= */

    div[data-testid="stSelectbox"] label {
        color: #F5F6FA !important;
    }

    /* Main selectbox container */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        background: #171B26 !important;
        background-color: #171B26 !important;
        border-radius: 8px !important;
    }

    /* Actual visible control */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
        background: #171B26 !important;
        background-color: #171B26 !important;
        border: 1px solid #343B4D !important;
        color: #F5F6FA !important;
        box-shadow: none !important;
    }

    /* Nested wrappers — prevent inherited green backgrounds */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div > div > div {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Selected value and text */
    div[data-testid="stSelectbox"] [data-baseweb="select"] *,
    div[data-testid="stSelectbox"] [data-baseweb="select"] input {
        color: #F5F6FA !important;
        -webkit-text-fill-color: #F5F6FA !important;
    }

    /* Dropdown arrow */
    div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
        fill: #FF6B9A !important;
        color: #FF6B9A !important;
    }

    /* Focus and active states */
    div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within,
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
        background: #171B26 !important;
        background-color: #171B26 !important;
        border-color: #FF354D !important;
        box-shadow: 0 0 0 1px #FF354D !important;
    }
    /* Streamlit 1.67 React Aria closed selectbox */
div[data-testid="stSelectbox"] .react-aria-ComboBox [data-rac][role="group"] {
    background: #171B26 !important;
    background-color: #171B26 !important;
    border: 1px solid #343B4D !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

/* Selected borough text */
div[data-testid="stSelectbox"] .react-aria-ComboBox input[role="combobox"] {
    background: transparent !important;
    color: #F5F6FA !important;
    -webkit-text-fill-color: #F5F6FA !important;
}

/* Dropdown arrow button */
div[data-testid="stSelectbox"] .react-aria-ComboBox button {
    background: transparent !important;
    color: #A7B0C2 !important;
}
    /* =============================================
       SELECTBOX — OPEN DROPDOWN MENU
    ============================================= */

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] [data-baseweb="menu"],
    div[data-baseweb="popover"] [role="listbox"],
    div[data-baseweb="popover"] ul {
        background: #171B26 !important;
        background-color: #171B26 !important;
        border-color: #343B4D !important;
    }

    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] [data-baseweb="menu-item"] {
        background: #171B26 !important;
        background-color: #171B26 !important;
        color: #F5F6FA !important;
        -webkit-text-fill-color: #F5F6FA !important;
    }

    div[data-baseweb="popover"] [role="option"]:hover,
    div[data-baseweb="popover"] [role="option"][aria-selected="true"],
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] [data-baseweb="menu-item"]:hover {
        background: #29202B !important;
        background-color: #29202B !important;
        color: #FF6B9A !important;
        -webkit-text-fill-color: #FF6B9A !important;
    }

    /* =============================================
       SLIDER — MAIN STYLING
    ============================================= */

    :root {
        --primary-color: #FF354D !important;
    }

    [data-testid="stAppViewContainer"] {
        --primary-color: #FF354D !important;
    }

    div[data-testid="stSlider"] {
        --slider-color: #FF354D !important;
        accent-color: #FF354D !important;
    }

    div[data-testid="stSlider"] label {
        color: #F5F6FA !important;
    }

    div[data-testid="stSlider"] [data-baseweb="slider"] {
        accent-color: #FF354D !important;
    }

    div[data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] {
        background: #FF354D !important;
        background-color: #FF354D !important;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background: #FF354D !important;
        background-color: #FF354D !important;
        border: 2px solid #FF6B9A !important;
        box-shadow: 0 0 0 3px rgba(255, 53, 77, 0.20) !important;
    }

    div[data-testid="stSlider"] [role="slider"]:hover {
        background: #FF6B9A !important;
        background-color: #FF6B9A !important;
        border-color: #FF6B9A !important;
        box-shadow: 0 0 0 5px rgba(255, 53, 77, 0.18) !important;
    }

    div[data-testid="stSlider"] [role="slider"]:focus,
    div[data-testid="stSlider"] [role="slider"]:focus-visible {
        outline: 2px solid #FF6B9A !important;
        outline-offset: 3px !important;
        box-shadow: 0 0 0 4px rgba(255, 53, 77, 0.24) !important;
    }

    /* Slider filled track */
    div[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"],
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2),
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
        background: #FF354D !important;
        background-color: #FF354D !important;
    }

    /* Slider displayed value */
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #FF6B9A !important;
    }

    /* =============================================
       NUMBER INPUT / TEXTAREA FOCUS
    ============================================= */

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #FF354D !important;
        box-shadow: 0 0 0 1px #FF354D !important;
    }

    /* =============================================
       STATIC TABLE
    ============================================= */

    div[data-testid="stTable"] {
        border: 1px solid #343B4D !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background-color: #12151E !important;
    }

    div[data-testid="stTable"] table {
        background-color: #12151E !important;
        border-collapse: collapse !important;
        width: 100% !important;
    }

    div[data-testid="stTable"] th {
        background-color: #1B2030 !important;
        color: #FF6B9A !important;
        border: 1px solid #343B4D !important;
    }

    div[data-testid="stTable"] td {
        background-color: #12151E !important;
        color: #F5F6FA !important;
        border: 1px solid #343B4D !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# CHRONOTUNNEL THEME
# --------------------------------------------------

FONT = "DM Sans, sans-serif"

INK = "#F5F6FA"
MUTED = "#A7B0C2"
GRID = "rgba(255,255,255,0.09)"

RED = "#FF354D"
PINK = "#FF6B9A"
BLUE = "#7BA7FF"
PURPLE = "#A78BFA"
ORANGE = "#FFAD70"

BOROUGH_COLORS = {
    "Manhattan": RED,
    "Brooklyn": BLUE,
    "Queens": PINK,
    "Bronx": PURPLE,
    "Staten Island": ORANGE,
    "Unknown": "#9299A8",
}

CHART_PALETTE = [
    RED,
    BLUE,
    PINK,
    PURPLE,
    ORANGE,
]

# --------------------------------------------------
# CHART STYLING
# --------------------------------------------------


def style_chart(fig, height=350):
    """Apply the shared ChronoTunnel dark chart theme."""

    fig.update_layout(
        height=height,
        font=dict(
            family=FONT,
            color=INK,
            size=12,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=12,
            r=35,
            t=20,
            b=15,
        ),
        hoverlabel=dict(
            bgcolor="#171B26",
            bordercolor="#343B4D",
            font=dict(
                family=FONT,
                color=INK,
                size=12,
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(
            family=FONT,
            color=MUTED,
            size=11,
        ),
        title_font=dict(color=MUTED),
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(
            family=FONT,
            color=INK,
            size=12,
        ),
        title_font=dict(color=MUTED),
    )

    return fig


# --------------------------------------------------
# TABLE STYLING
# --------------------------------------------------


def style_dark_table(dataframe, formats=None):
    """Apply consistent dark styling to static analytical tables."""

    styled = dataframe.style

    if formats:
        styled = styled.format(formats)

    styled = styled.set_properties(
        **{
            "background-color": "#12151E",
            "color": "#F5F6FA",
            "border-color": "#343B4D",
        }
    )

    styled = styled.set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#1B2030"),
                    ("color", "#FF6B9A"),
                    ("border-color", "#343B4D"),
                    ("font-weight", "600"),
                    ("text-align", "left"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("background-color", "#12151E"),
                    ("color", "#F5F6FA"),
                    ("border-color", "#343B4D"),
                ],
            },
            {
                "selector": "table",
                "props": [
                    ("width", "100%"),
                    ("border-collapse", "collapse"),
                    ("background-color", "#12151E"),
                ],
            },
        ]
    )

    # Hide the pandas index in the rendered table.
    styled = styled.hide(axis="index")

    return styled


# --------------------------------------------------
# VALIDATION HELPERS
# --------------------------------------------------


def validate_required_columns(dataframe, required_columns, dataset_name):
    """Ensure an analytical dataframe contains its expected schema."""

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"{dataset_name} must be a pandas DataFrame.")

    missing_columns = sorted(set(required_columns) - set(dataframe.columns))

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: {', '.join(missing_columns)}"
        )


def validate_numeric_columns(dataframe, columns, dataset_name):
    """Convert numeric columns and reject missing or non-finite values."""

    dataframe = dataframe.copy()

    for column in columns:
        if column not in dataframe.columns:
            raise ValueError(f"{dataset_name} is missing numeric column '{column}'.")

        converted = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

        invalid_mask = converted.isna() | ~np.isfinite(converted)

        if invalid_mask.any():
            raise ValueError(
                f"{dataset_name}.{column} contains "
                f"{int(invalid_mask.sum())} invalid numeric values."
            )

        dataframe[column] = converted

    return dataframe


def validate_nonnegative_columns(dataframe, columns, dataset_name):
    """Reject negative values in nonnegative analytical measures."""

    for column in columns:
        if (dataframe[column] < 0).any():
            raise ValueError(f"{dataset_name}.{column} contains negative values.")


def compact_number(value):
    """Format large numbers for dashboard metrics."""

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


# --------------------------------------------------
# LOAD GEOSPATIAL DATA
# --------------------------------------------------


@st.cache_data(show_spinner=False)
def load_geospatial_data():
    """Load geospatial summaries and diagnostics from DuckDB."""

    connection = create_connection()

    try:
        borough_summary = get_borough_geospatial_summary(connection)

        station_locations = get_top_ridership_locations(
            connection,
            limit=1000,
        )

        weighted_centroids = get_borough_weighted_centroids(connection)

        coordinate_quality = get_coordinate_quality_summary(connection)

        return (
            borough_summary,
            station_locations,
            weighted_centroids,
            coordinate_quality,
        )

    finally:
        connection.close()


try:
    (
        borough_df,
        station_df,
        centroid_df,
        quality_df,
    ) = load_geospatial_data()

except Exception as error:
    st.error(
        "Could not load geospatial data. "
        "Please verify the station_coordinates view and DuckDB connection."
    )
    st.exception(error)
    st.stop()

# --------------------------------------------------
# DATA PREPARATION AND VALIDATION
# --------------------------------------------------

try:
    validate_required_columns(
        borough_df,
        [
            "borough",
            "station_mode_records",
            "unique_station_ids",
            "total_ridership",
            "average_station_ridership",
            "ridership_share_percent",
        ],
        "Borough geospatial summary",
    )

    validate_required_columns(
        station_df,
        [
            "station_complex_id",
            "transit_mode",
            "station_complex",
            "borough",
            "latitude",
            "longitude",
            "total_ridership",
            "coordinate_variants",
        ],
        "Station location data",
    )

    validate_required_columns(
        centroid_df,
        [
            "borough",
            "weighted_latitude",
            "weighted_longitude",
            "total_ridership",
        ],
        "Borough weighted centroids",
    )

    validate_required_columns(
        quality_df,
        [
            "total_records",
            "unique_station_ids",
            "unique_station_mode_keys",
            "duplicate_station_mode_groups",
            "invalid_latitude_records",
            "invalid_longitude_records",
            "records_with_multiple_coordinate_variants",
            "maximum_coordinate_variants",
        ],
        "Coordinate quality summary",
    )

    if borough_df.empty:
        raise ValueError("No borough-level geospatial records are available.")

    if station_df.empty:
        raise ValueError("No station coordinate records are available.")

    borough_df = borough_df.copy()
    station_df = station_df.copy()
    centroid_df = centroid_df.copy()
    quality_df = quality_df.copy()

    # Borough summary validation

    borough_df["borough"] = (
        borough_df["borough"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    borough_df = validate_numeric_columns(
        borough_df,
        [
            "station_mode_records",
            "unique_station_ids",
            "total_ridership",
            "average_station_ridership",
            "ridership_share_percent",
        ],
        "Borough geospatial summary",
    )

    validate_nonnegative_columns(
        borough_df,
        [
            "station_mode_records",
            "unique_station_ids",
            "total_ridership",
            "average_station_ridership",
            "ridership_share_percent",
        ],
        "Borough geospatial summary",
    )

    if borough_df["borough"].duplicated().any():
        raise ValueError(
            "Borough geospatial summary contains duplicate borough records."
        )

    if not borough_df["ridership_share_percent"].between(0, 100).all():
        raise ValueError("Borough ridership shares must be between 0 and 100.")

    borough_total = borough_df["total_ridership"].sum()

    if borough_total > 0:
        share_total = borough_df["ridership_share_percent"].sum()

        if not np.isclose(share_total, 100.0, atol=0.1):
            raise ValueError(
                "Borough ridership shares do not sum to approximately 100%."
            )

    borough_df = borough_df.sort_values(
        "total_ridership",
        ascending=False,
    ).reset_index(drop=True)

    # Station coordinate preparation

    station_df["borough"] = (
        station_df["borough"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    station_df["station_complex"] = (
        station_df["station_complex"]
        .fillna("Unnamed station")
        .astype(str)
        .str.strip()
        .replace("", "Unnamed station")
    )

    station_df["transit_mode"] = (
        station_df["transit_mode"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    station_df = station_df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    for column in [
        "latitude",
        "longitude",
        "total_ridership",
        "coordinate_variants",
    ]:
        station_df[column] = pd.to_numeric(
            station_df[column],
            errors="coerce",
        )

    station_df = station_df.dropna(
        subset=[
            "latitude",
            "longitude",
            "total_ridership",
            "coordinate_variants",
        ]
    )

    station_df = station_df[
        station_df["latitude"].between(-90, 90)
        & station_df["longitude"].between(-180, 180)
        & (station_df["total_ridership"] >= 0)
        & (station_df["coordinate_variants"] >= 0)
    ].copy()

    if station_df.empty:
        raise ValueError("No valid station coordinate records remain after validation.")

    # Weighted centroid validation

    if not centroid_df.empty:
        centroid_df["borough"] = (
            centroid_df["borough"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )

        centroid_df = validate_numeric_columns(
            centroid_df,
            [
                "weighted_latitude",
                "weighted_longitude",
                "total_ridership",
            ],
            "Borough weighted centroids",
        )

        validate_nonnegative_columns(
            centroid_df,
            ["total_ridership"],
            "Borough weighted centroids",
        )

        if not centroid_df["weighted_latitude"].between(-90, 90).all():
            raise ValueError(
                "Weighted centroid latitude values are outside valid bounds."
            )

        if not centroid_df["weighted_longitude"].between(-180, 180).all():
            raise ValueError(
                "Weighted centroid longitude values are outside valid bounds."
            )

    # Coordinate quality validation

    if not quality_df.empty:
        if len(quality_df) != 1:
            raise ValueError(
                "Coordinate quality summary should contain exactly one row."
            )

        quality_df = validate_numeric_columns(
            quality_df,
            [
                "total_records",
                "unique_station_ids",
                "unique_station_mode_keys",
                "duplicate_station_mode_groups",
                "invalid_latitude_records",
                "invalid_longitude_records",
                "records_with_multiple_coordinate_variants",
                "maximum_coordinate_variants",
            ],
            "Coordinate quality summary",
        )

        validate_nonnegative_columns(
            quality_df,
            [
                "total_records",
                "unique_station_ids",
                "unique_station_mode_keys",
                "duplicate_station_mode_groups",
                "invalid_latitude_records",
                "invalid_longitude_records",
                "records_with_multiple_coordinate_variants",
                "maximum_coordinate_variants",
            ],
            "Coordinate quality summary",
        )

except Exception as error:
    st.error("Geospatial data validation failed.")
    st.exception(error)
    st.stop()

# --------------------------------------------------
# DERIVED METRICS
# --------------------------------------------------

total_locations = len(station_df)

total_geo_ridership = station_df["total_ridership"].sum()

borough_count = station_df["borough"].nunique()

coordinate_variants = station_df["coordinate_variants"].sum()

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="page-eyebrow">SPATIAL INTELLIGENCE</div>

    <h1 class="page-title">Geospatial Analysis</h1>

    <p class="page-subtitle">
        Explore the geographic distribution of subway demand,
        locate high-ridership station complexes, and investigate
        how mobility patterns are distributed across New York City.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

st.markdown("### Geographic network overview")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.metric(
        "Mapped station locations",
        f"{total_locations:,}",
    )

with metric_2:
    st.metric(
        "Geographic ridership",
        compact_number(total_geo_ridership),
    )

with metric_3:
    st.metric(
        "Boroughs represented",
        f"{borough_count:,}",
    )

with metric_4:
    st.metric(
        "Coordinate variants",
        f"{int(coordinate_variants):,}",
    )

st.markdown("---")

# --------------------------------------------------
# INTERACTIVE STATION MAP
# --------------------------------------------------

st.markdown("### Explore the station network")

st.caption(
    "Select a borough to investigate its station locations. "
    "Use the map layer control to switch between station markers "
    "and the ridership heatmap."
)

borough_options = ["All boroughs"] + sorted(station_df["borough"].unique().tolist())

selected_borough = st.selectbox(
    "Select borough",
    borough_options,
    key="geospatial_borough_selector",
)

if selected_borough == "All boroughs":
    map_df = station_df.copy()
else:
    map_df = station_df[station_df["borough"] == selected_borough].copy()

if map_df.empty:
    st.warning("No valid station locations are available for this selection.")
    st.stop()

# --------------------------------------------------
# BUILD FOLIUM MAP
# --------------------------------------------------

center_lat = float(map_df["latitude"].mean())
center_lon = float(map_df["longitude"].mean())

map_object = folium.Map(
    location=[
        center_lat,
        center_lon,
    ],
    zoom_start=11,
    tiles=None,
    control_scale=True,
)

folium.TileLayer(
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attr="&copy; OpenStreetMap contributors",
    name="OpenStreetMap",
    overlay=False,
    control=True,
    show=True,
    max_zoom=19,
).add_to(map_object)

# --------------------------------------------------
# STATION RIDERSHIP LAYER
# --------------------------------------------------

station_layer = folium.FeatureGroup(
    name="Station ridership",
    show=True,
)

heat_layer = folium.FeatureGroup(
    name="Ridership heatmap",
    show=False,
)

max_ridership = max(
    float(map_df["total_ridership"].max()),
    1.0,
)

for _, station in map_df.iterrows():
    ridership = float(station["total_ridership"])

    radius = 4 + 10 * (ridership / max_ridership) ** 0.5

    station_name = escape(str(station["station_complex"]))
    borough_name = escape(str(station["borough"]))
    transit_mode = escape(str(station["transit_mode"]))

    popup_html = f"""
    <div style="
        font-family:Arial,sans-serif;
        min-width:190px;
        color:#171B26;
    ">
        <b>{station_name}</b>
        <hr style="margin:6px 0;">

        <b>Borough:</b> {borough_name}<br>
        <b>Transit mode:</b> {transit_mode}<br>
        <b>Ridership:</b> {ridership:,.0f}<br>
        <b>Latitude:</b> {station["latitude"]:.5f}<br>
        <b>Longitude:</b> {station["longitude"]:.5f}
    </div>
    """

    folium.CircleMarker(
        location=[
            float(station["latitude"]),
            float(station["longitude"]),
        ],
        radius=radius,
        popup=folium.Popup(
            popup_html,
            max_width=300,
        ),
        tooltip=station_name,
        color=RED,
        weight=1.4,
        fill=True,
        fill_color=PINK,
        fill_opacity=0.78,
    ).add_to(station_layer)

station_layer.add_to(map_object)

# --------------------------------------------------
# RIDERSHIP HEATMAP LAYER
# --------------------------------------------------

heat_data = map_df[
    [
        "latitude",
        "longitude",
        "total_ridership",
    ]
].values.tolist()

HeatMap(
    heat_data,
    radius=19,
    blur=16,
    min_opacity=0.3,
    max_zoom=13,
    gradient={
        0.20: "#7BA7FF",
        0.40: "#A78BFA",
        0.60: "#FF6B9A",
        0.80: "#FF354D",
        1.00: "#FFAD70",
    },
).add_to(heat_layer)

heat_layer.add_to(map_object)

# --------------------------------------------------
# MAP CONTROLS
# --------------------------------------------------

folium.LayerControl(
    collapsed=False,
).add_to(map_object)

# --------------------------------------------------
# DISPLAY MAP
# --------------------------------------------------

map_html = map_object.get_root().render()

components.html(
    map_html,
    height=620,
    scrolling=False,
)

st.caption(
    f"Displaying {len(map_df):,} station-mode coordinate records"
    + (
        f" for {selected_borough}."
        if selected_borough != "All boroughs"
        else " across all boroughs."
    )
)

st.markdown("---")

# --------------------------------------------------
# TOP RIDERSHIP LOCATIONS
# --------------------------------------------------

st.markdown("### Highest-ridership station locations")

st.caption(
    "The locations below are ranked using cumulative ridership "
    "from the station coordinate dataset."
)

slider_minimum = min(5, len(station_df))
slider_maximum = min(20, len(station_df))
slider_default = min(15, slider_maximum)

if slider_minimum < slider_maximum:
    top_n = st.slider(
        "Number of locations",
        min_value=slider_minimum,
        max_value=slider_maximum,
        value=slider_default,
        step=1,
        key="geospatial_top_locations_slider",
    )
else:
    top_n = slider_maximum
    st.caption(f"Showing all {top_n} available station locations.")

top_df = station_df.nlargest(
    top_n,
    "total_ridership",
).sort_values(
    "total_ridership",
    ascending=True,
)

fig_top = px.bar(
    top_df,
    x="total_ridership",
    y="station_complex",
    orientation="h",
    color="borough",
    color_discrete_map=BOROUGH_COLORS,
    hover_data=[
        "transit_mode",
        "latitude",
        "longitude",
    ],
    labels={
        "total_ridership": "Total ridership",
        "station_complex": "",
        "borough": "Borough",
        "transit_mode": "Transit mode",
    },
)

fig_top.update_traces(
    marker_line_width=0,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Ridership: %{x:,.0f}<br>"
        "Borough: %{fullData.name}"
        "<extra></extra>"
    ),
)

fig_top = style_chart(
    fig_top,
    height=max(380, top_n * 29),
)

fig_top.update_layout(
    margin=dict(
        l=10,
        r=35,
        t=15,
        b=10,
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.18,
        xanchor="center",
        x=0.5,
        font=dict(
            color=MUTED,
            size=10,
        ),
    ),
)

st.plotly_chart(
    fig_top,
    use_container_width=True,
    config={"displayModeBar": False},
)

st.markdown("---")

# --------------------------------------------------
# BOROUGH GEOGRAPHIC SUMMARY
# --------------------------------------------------

st.markdown("### Geographic distribution by borough")

borough_chart = borough_df.copy()

geo_left, geo_right = st.columns(
    [1.3, 1],
    gap="large",
)

# --------------------------------------------------
# BOROUGH RIDERSHIP
# --------------------------------------------------

with geo_left:
    borough_ridership_plot = borough_chart.sort_values(
        "total_ridership",
        ascending=True,
    )

    fig_borough = px.bar(
        borough_ridership_plot,
        x="total_ridership",
        y="borough",
        orientation="h",
        text="ridership_share_percent",
        color="borough",
        color_discrete_map=BOROUGH_COLORS,
        labels={
            "total_ridership": "Total ridership",
            "borough": "",
            "ridership_share_percent": "Ridership share (%)",
        },
    )

    fig_borough.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig_borough = style_chart(
        fig_borough,
        height=350,
    )

    fig_borough.update_layout(
        margin=dict(
            l=10,
            r=55,
            t=15,
            b=10,
        ),
        showlegend=False,
    )

    fig_borough.update_xaxes(
        title=None,
    )

    st.plotly_chart(
        fig_borough,
        use_container_width=True,
        config={"displayModeBar": False},
    )

# --------------------------------------------------
# STATION DISTRIBUTION
# --------------------------------------------------

with geo_right:
    station_count_plot = borough_chart.sort_values(
        "unique_station_ids",
        ascending=True,
    )

    fig_station_count = px.bar(
        station_count_plot,
        x="unique_station_ids",
        y="borough",
        orientation="h",
        text="unique_station_ids",
        color="borough",
        color_discrete_map=BOROUGH_COLORS,
        labels={
            "unique_station_ids": "Unique station IDs",
            "borough": "",
        },
    )

    fig_station_count.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
    )

    fig_station_count = style_chart(
        fig_station_count,
        height=350,
    )

    fig_station_count.update_layout(
        margin=dict(
            l=10,
            r=45,
            t=15,
            b=10,
        ),
        showlegend=False,
    )

    fig_station_count.update_xaxes(
        title=None,
    )

    st.plotly_chart(
        fig_station_count,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.markdown("---")

# --------------------------------------------------
# RIDERSHIP-WEIGHTED BOROUGH CENTROIDS
# --------------------------------------------------

st.markdown("### Ridership-weighted geographic centers")

st.caption(
    "These representative centers are calculated by weighting "
    "station coordinates according to their cumulative ridership. "
    "They are not official borough centers."
)

if not centroid_df.empty:
    centroid_display = centroid_df.rename(
        columns={
            "borough": "Borough",
            "weighted_latitude": "Weighted latitude",
            "weighted_longitude": "Weighted longitude",
            "total_ridership": "Total ridership",
        }
    )

    # Static Pandas Styler table: no interactive column menu.
    st.table(
        style_dark_table(
            centroid_display,
            {
                "Weighted latitude": "{:.6f}",
                "Weighted longitude": "{:.6f}",
                "Total ridership": "{:,.0f}",
            },
        )
    )
else:
    st.info("No weighted centroid records are available.")

# --------------------------------------------------
# COORDINATE QUALITY
# --------------------------------------------------

st.markdown("---")

st.markdown("### Coordinate quality assessment")

st.caption(
    "A diagnostic view of coordinate coverage, station-mode "
    "identifiers, and coordinate consistency."
)

if not quality_df.empty:
    quality = quality_df.iloc[0]

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.metric(
            "Coordinate records",
            f"{int(quality['total_records']):,}",
        )

    with q2:
        st.metric(
            "Unique station-mode keys",
            f"{int(quality['unique_station_mode_keys']):,}",
        )

    with q3:
        st.metric(
            "Duplicate station-mode groups",
            f"{int(quality['duplicate_station_mode_groups']):,}",
        )

    with q4:
        invalid_coordinates = int(quality["invalid_latitude_records"]) + int(
            quality["invalid_longitude_records"]
        )

        st.metric(
            "Invalid coordinate records",
            f"{invalid_coordinates:,}",
        )

    with st.expander("View full coordinate diagnostics"):
        quality_display = pd.DataFrame(
            {
                "Diagnostic": [
                    "Total coordinate records",
                    "Unique station IDs",
                    "Unique station-mode keys",
                    "Duplicate station-mode groups",
                    "Invalid latitude records",
                    "Invalid longitude records",
                    "Records with multiple coordinate variants",
                    "Maximum coordinate variants",
                ],
                "Value": [
                    quality["total_records"],
                    quality["unique_station_ids"],
                    quality["unique_station_mode_keys"],
                    quality["duplicate_station_mode_groups"],
                    quality["invalid_latitude_records"],
                    quality["invalid_longitude_records"],
                    quality["records_with_multiple_coordinate_variants"],
                    quality["maximum_coordinate_variants"],
                ],
            }
        )

        # Static Pandas Styler table: no interactive column menu.
        st.table(style_dark_table(quality_display))
else:
    st.info("No coordinate quality diagnostics are available.")

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------

with st.expander("Understanding the geospatial analysis"):
    st.markdown(
        """
        **Station coordinates**

        Station locations are represented using the coordinate
        records in the station coordinate dataset. Where multiple
        coordinate variants exist, the selected representative
        coordinate should not be interpreted as an exact station
        entrance.

        **Ridership-scaled markers**

        Marker size is scaled using the square root of station
        ridership so that differences remain visually readable.

        **Heatmap**

        The heatmap uses station latitude, longitude, and cumulative
        ridership as its intensity weight.

        **Weighted centroids**

        Each borough's weighted center is calculated using
        station coordinates weighted by cumulative ridership.

        **Station identity**

        Station-mode records are retained separately because a
        station complex ID can appear under more than one transit
        mode. The composite station-mode key is therefore important
        when interpreting coordinate records.

        **Data limitations**

        This is a historical geographic analysis of MTA ridership
        records from 2020–2024. It is not a live passenger-density
        map, a station-capacity map, or a real-time operations feed.
        """
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div style="
        margin-top: 2rem;
        padding: 1rem 0;
        border-top: 1px solid rgba(255,255,255,0.10);
        color: #A7B0C2;
        font-size: 0.78rem;
    ">
        ChronoTunnel · SPATIAL INTELLIGENCE · HISTORICAL DATA 2020–2024
    </div>
    """,
    unsafe_allow_html=True,
)
