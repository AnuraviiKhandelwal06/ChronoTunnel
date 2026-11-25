from html import escape

import pandas as pd
import streamlit as st

from components.cards import kpi_row, page_footer, section_heading
from components.charts import (
    CHART_CONFIG,
    annual_ridership,
    borough_share,
    mode_distribution,
    top_stations,
)
from components.metrics import (
    compact_number,
    mode_label,
    require_metrics,
    short_station_name,
)
from components.render import show_html
from components.sidebar import mount_dashboard
from config import (
    STUDY_END_YEAR,
    STUDY_START_YEAR,
    TOTAL_BOROUGHS,
    TOTAL_RIDERSHIP,
    TOTAL_STATIONS,
    TOTAL_TRANSFERS,
)

st.set_page_config(
    page_title="Dashboard | ChronoTunnel",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

mount_dashboard()


def validate_metric_frame(
    frame: pd.DataFrame,
    name: str,
    required_columns: set[str],
) -> pd.DataFrame:
    """Validate a metric DataFrame before using it."""

    if not isinstance(frame, pd.DataFrame) or frame.empty:
        st.error(f"The {name} metric file contains no records.")
        st.stop()

    missing_columns = required_columns - set(frame.columns)

    if missing_columns:
        st.error(
            f"The {name} metric file is missing columns: "
            f"{', '.join(sorted(missing_columns))}."
        )
        st.stop()

    return frame.copy()


def numeric_column(
    frame: pd.DataFrame,
    column: str,
    name: str,
) -> pd.DataFrame:
    """Convert a metric column to numeric and validate its values."""

    frame[column] = pd.to_numeric(frame[column], errors="coerce")

    if frame[column].isna().any():
        st.error(f"The {name} metric contains missing or invalid values.")
        st.stop()

    if (
        not frame[column]
        .map(lambda value: pd.notna(value) and abs(value) != float("inf"))
        .all()
    ):
        st.error(f"The {name} metric contains non-finite values.")
        st.stop()

    if (frame[column] < 0).any():
        st.error(f"The {name} metric contains negative ridership values.")
        st.stop()

    return frame


def get_category_share(
    frame: pd.DataFrame,
    category_column: str,
    category_value: str,
    metric_name: str,
) -> float:
    """Calculate a category's share of the total recorded ridership."""

    selected = frame.loc[
        frame[category_column] == category_value,
        "total_ridership",
    ]

    total = frame["total_ridership"].sum()

    if selected.empty:
        st.error(f"The {metric_name} metric is missing {category_value} data.")
        st.stop()

    if total <= 0:
        st.error(f"The {metric_name} metric has an invalid total.")
        st.stop()

    return float(selected.iloc[0] / total * 100)


frames = require_metrics(
    {
        "yearly": "yearly_ridership.csv",
        "borough": "borough_ridership.csv",
        "modes": "transit_mode_ridership.csv",
        "stations": "top_stations.csv",
    }
)


# -------------------------------------------------------------------
# Validate and prepare yearly metrics
# -------------------------------------------------------------------

yearly = validate_metric_frame(
    frames["yearly"],
    "Yearly ridership",
    {"year", "total_ridership"},
)

yearly["year"] = pd.to_numeric(yearly["year"], errors="coerce")
yearly = numeric_column(yearly, "total_ridership", "Yearly ridership")

if yearly["year"].isna().any():
    st.error("Yearly ridership contains invalid year values.")
    st.stop()

if yearly["year"].duplicated().any():
    st.error("Yearly ridership contains duplicate year records.")
    st.stop()

yearly["year"] = yearly["year"].astype(int)
yearly = yearly.sort_values("year").reset_index(drop=True)

if yearly.empty:
    st.error("No yearly ridership records are available.")
    st.stop()

first = yearly.iloc[0]
last = yearly.iloc[-1]

if first["total_ridership"] <= 0:
    st.error("Cannot calculate annual growth from a zero starting value.")
    st.stop()

growth = (
    (last["total_ridership"] - first["total_ridership"])
    / first["total_ridership"]
    * 100
)


# -------------------------------------------------------------------
# Validate and prepare borough metrics
# -------------------------------------------------------------------

borough = validate_metric_frame(
    frames["borough"],
    "Borough ridership",
    {"borough", "total_ridership"},
)

borough = numeric_column(borough, "total_ridership", "Borough ridership")

manhattan_share = get_category_share(
    borough,
    "borough",
    "Manhattan",
    "Borough ridership",
)


# -------------------------------------------------------------------
# Validate and prepare transit mode metrics
# -------------------------------------------------------------------

modes = validate_metric_frame(
    frames["modes"],
    "Transit mode ridership",
    {"transit_mode", "total_ridership"},
)

modes = numeric_column(modes, "total_ridership", "Transit mode ridership")

subway_share = get_category_share(
    modes,
    "transit_mode",
    "subway",
    "Transit mode ridership",
)

mode_sentence = ", ".join(
    f"{mode_label(row.transit_mode)} {compact_number(row.total_ridership)}"
    for row in modes.sort_values(
        "total_ridership",
        ascending=False,
    ).itertuples()
)


# -------------------------------------------------------------------
# Validate and prepare station metrics
# -------------------------------------------------------------------

stations = validate_metric_frame(
    frames["stations"],
    "Top stations",
    {"station_complex", "borough", "total_ridership"},
)

stations = numeric_column(stations, "total_ridership", "Top stations")

if stations.empty:
    st.error("No station ranking records are available.")
    st.stop()

stations = stations.sort_values(
    "total_ridership",
    ascending=False,
).reset_index(drop=True)

leader = stations.iloc[0]


# -------------------------------------------------------------------
# Dashboard welcome section
# -------------------------------------------------------------------

show_html(
    f"""
    <div class="mp-welcome">
        <div>
            <h1>Welcome to ChronoTunnel.</h1>
            <p>A historical reading of New York City transit ridership
            from January {STUDY_START_YEAR} through December {STUDY_END_YEAR}.
            The figures below describe recorded activity, not a live network.</p>
        </div>
        <div class="mp-period">
            <span>DATASET PERIOD</span>
            <strong>{STUDY_START_YEAR}–{STUDY_END_YEAR}</strong>
            <small>Recorded history, not a live feed</small>
        </div>
    </div>
    """
)


# -------------------------------------------------------------------
# Headline KPIs
# -------------------------------------------------------------------

kpi_row(
    [
        (
            "TOTAL RIDERSHIP",
            compact_number(TOTAL_RIDERSHIP),
            "Five-year recorded total",
        ),
        (
            "TOTAL TRANSFERS",
            compact_number(TOTAL_TRANSFERS),
            "Already included in ridership",
        ),
        (
            "STATION IDENTIFIERS",
            f"{TOTAL_STATIONS:,}",
            "Unique station IDs in the study",
        ),
        (
            "BOROUGHS",
            str(TOTAL_BOROUGHS),
            "New York City coverage",
        ),
    ]
)


# -------------------------------------------------------------------
# Annual ridership and borough distribution
# -------------------------------------------------------------------

left, right = st.columns([1.35, 0.85], gap="medium")

with left:
    section_heading(
        "Annual ridership",
        "Recorded ridership by year. The path describes the series; it does not identify a cause.",
    )

    st.plotly_chart(
        annual_ridership(yearly),
        use_container_width=True,
        config=CHART_CONFIG,
    )

with right:
    section_heading(
        "Borough distribution",
        "Share of recorded ridership.",
    )

    st.plotly_chart(
        borough_share(borough),
        use_container_width=True,
        config=CHART_CONFIG,
    )


# -------------------------------------------------------------------
# Transit mode and leading stations
# -------------------------------------------------------------------

left, right = st.columns([0.85, 1.15], gap="medium")

with left:
    section_heading(
        "Transit mode",
        "Subway dominates the recorded total. The smaller modes remain visible in the hover values.",
    )

    st.plotly_chart(
        mode_distribution(modes),
        use_container_width=True,
        config=CHART_CONFIG,
    )

with right:
    section_heading(
        "Leading station complexes",
        "Highest recorded totals in the published station ranking.",
    )

    st.plotly_chart(
        top_stations(stations, limit=8),
        use_container_width=True,
        config=CHART_CONFIG,
    )


# -------------------------------------------------------------------
# Key network insights
# -------------------------------------------------------------------

section_heading(
    "Key network insights",
    "Observations computed from the published metric files.",
)

insights = [
    (
        "ANNUAL CHANGE",
        (
            f"Recorded ridership moved from "
            f"{compact_number(first.total_ridership)} in {int(first.year)} "
            f"to {compact_number(last.total_ridership)} in {int(last.year)}, "
            f"an increase of {growth:.1f}%."
        ),
    ),
    (
        "BOROUGH SHARE",
        (
            f"Manhattan accounts for {manhattan_share:.2f}% of recorded "
            "ridership. Borough shares describe where rides were recorded, "
            "not passenger origins."
        ),
    ),
    (
        "LEADING STATION",
        (
            f"{short_station_name(leader.station_complex)} leads the "
            f"published ranking at "
            f"{compact_number(leader.total_ridership)}, "
            f"in {leader.borough}."
        ),
    ),
    (
        "MODE MIX",
        (
            f"Subway accounts for {subway_share:.1f}% of recorded ridership. "
            f"Mode totals: {mode_sentence}."
        ),
    ),
]

for row_start in range(0, len(insights), 2):
    insight_columns = st.columns(2, gap="small")

    row_insights = insights[row_start : row_start + 2]

    for column, (label, text) in zip(
        insight_columns,
        row_insights,
        strict=True,
    ):
        with column:
            show_html(
                f"""
                <div class="mp-finding mp-observed">
                    <div class="mp-kicker">{escape(label)}</div>
                    <p>{escape(text)}</p>
                </div>
                """
            )

# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------

page_footer()
