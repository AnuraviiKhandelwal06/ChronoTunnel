import json
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
METRICS_DIR = OUTPUTS_DIR / "metrics"
FIGURES_DIR = OUTPUTS_DIR / "figures"
MAPS_DIR = OUTPUTS_DIR / "maps"

HOURLY_DATA_PATH = PROCESSED_DIR / "hourly_ridership_sample_station_level_2020_2024.csv"

MONTHLY_DATA_PATH = PROCESSED_DIR / "monthly_ridership_station_level_2020_2024.csv"

COORDINATES_PATH = PROCESSED_DIR / "station_coordinates.csv"


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

PROJECT_NAME = "ChronoTunnel"

PROJECT_TAGLINE = "Turning Transit Data into Smarter Mobility Decisions."

STUDY_START_YEAR = 2020
STUDY_END_YEAR = 2024

TOTAL_RIDERSHIP = 4_802_664_920
TOTAL_TRANSFERS = 197_901_742

TOTAL_STATIONS = 428
TOTAL_BOROUGHS = 5
TOTAL_TRANSIT_MODES = 3


# --------------------------------------------------
# THEME COLORS
# --------------------------------------------------

COLORS = {
    "background": "#102D26",
    "surface": "#173F35",
    "surface_light": "#1E4A3E",
    "primary": "#1F6A54",
    "secondary": "#91B7A5",
    "accent": "#B8E6CF",
    "text": "#F5F5F0",
    "muted": "#A2AEA7",
    "border": "rgba(245,245,240,0.14)",
    "warning": "#C4A574",
    "graphite": "#202724",
    "offwhite": "#F5F5F0",
    "canvas": "#F3F0E8",
    "ink": "#14241F",
}

DASHBOARD = {
    "canvas": "#F3F0E8",
    "card": "#FBF9F4",
    "ink": "#14241F",
    "muted": "#5E6F68",
    "line": "#E4DDD1",
    "accent": "#1F6A54",
    "sidebar": "#102D26",
    "mint": "#B8E6CF",
}


# --------------------------------------------------
# ANALYTICAL COLORS
# --------------------------------------------------

BOROUGH_COLORS = {
    "Manhattan": "#173F35",
    "Brooklyn": "#3E7C68",
    "Queens": "#91B7A5",
    "Bronx": "#C4A574",
    "Staten Island": "#6E8B84",
}

MODE_LABELS = {
    "subway": "Subway",
    "tram": "Tram",
    "staten_island_railway": "Staten Island Railway",
}

MODE_COLORS = {
    "subway": "#173F35",
    "tram": "#7EAA96",
    "staten_island_railway": "#C4A574",
}

BOROUGH_ORDER = [
    "Manhattan",
    "Brooklyn",
    "Queens",
    "Bronx",
    "Staten Island",
]


# --------------------------------------------------
# DASHBOARD NAVIGATION
# --------------------------------------------------

NAV_ITEMS = [
    (
        "pages/00_Home.py",
        "Dashboard Home",
        ":material/space_dashboard:",
    ),
    (
        "pages/01_Overview.py",
        "Overview",
        ":material/monitoring:",
    ),
    (
        "pages/02_Temporal_Analysis.py",
        "Temporal Analysis",
        ":material/schedule:",
    ),
    (
        "pages/03_Station_Analysis.py",
        "Station Analysis",
        ":material/train:",
    ),
    (
        "pages/04_Borough_Analysis.py",
        "Borough Analysis",
        ":material/location_city:",
    ),
    (
        "pages/05_Geospatial_Analysis.py",
        "Geospatial Analysis",
        ":material/map:",
    ),
    (
        "pages/06_Insights_Recommendations.py",
        "Insights & Recommendations",
        ":material/lightbulb:",
    ),
]


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------


@st.cache_data
def load_csv(file_path: str) -> pd.DataFrame:
    """Load and cache a CSV dataset."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Required dataset not found: {path}")

    return pd.read_csv(path)


def load_metric(filename: str) -> pd.DataFrame:
    """Load an analytical metrics CSV."""

    return load_csv(str(METRICS_DIR / filename))


def load_hourly_data() -> pd.DataFrame:
    """Load processed hourly ridership data."""

    return load_csv(str(HOURLY_DATA_PATH))


def load_monthly_data() -> pd.DataFrame:
    """Load processed monthly ridership data."""

    return load_csv(str(MONTHLY_DATA_PATH))


def load_station_coordinates() -> pd.DataFrame:
    """Load station coordinate reference data."""

    return load_csv(str(COORDINATES_PATH))


@st.cache_data
def load_json_metric(filename: str) -> dict:
    """Load a cached JSON metrics file."""

    path = METRICS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Required dataset not found: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


# --------------------------------------------------
# SHARED PROJECT INFORMATION
# --------------------------------------------------


def get_project_info() -> dict:
    """Return shared project information."""

    return {
        "name": PROJECT_NAME,
        "tagline": PROJECT_TAGLINE,
        "study_period": (f"{STUDY_START_YEAR}–{STUDY_END_YEAR}"),
        "stations": TOTAL_STATIONS,
        "boroughs": TOTAL_BOROUGHS,
        "transit_modes": TOTAL_TRANSIT_MODES,
    }
