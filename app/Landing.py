import streamlit as st

from components.landing import render_landing
from components.metrics import compact_number
from components.styles import inject_landing_styles
from config import (
    STUDY_END_YEAR,
    STUDY_START_YEAR,
    TOTAL_BOROUGHS,
    TOTAL_RIDERSHIP,
    TOTAL_STATIONS,
    TOTAL_TRANSFERS,
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ChronoTunnel | Urban Mobility Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# Dashboard page routes
# --------------------------------------------------

ROUTES = {
    "dashboard": "pages/00_Home.py",
    "overview": "pages/01_Overview.py",
    "temporal": "pages/02_Temporal_Analysis.py",
    "stations": "pages/03_Station_Analysis.py",
    "boroughs": "pages/04_Borough_Analysis.py",
    "geo": "pages/05_Geospatial_Analysis.py",
    "insights": "pages/06_Insights_Recommendations.py",
}


# --------------------------------------------------
# Handle navigation from landing-page links
# --------------------------------------------------

destination = st.query_params.get("nav")

if destination in ROUTES:
    st.switch_page(ROUTES[destination])


# --------------------------------------------------
# Render landing page
# --------------------------------------------------

inject_landing_styles()

render_landing(
    ridership=compact_number(TOTAL_RIDERSHIP),
    transfers=compact_number(TOTAL_TRANSFERS),
    stations=f"{TOTAL_STATIONS:,}",
    boroughs=str(TOTAL_BOROUGHS),
    period=f"{STUDY_START_YEAR}–{STUDY_END_YEAR}",
)
