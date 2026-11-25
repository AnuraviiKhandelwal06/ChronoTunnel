import pandas as pd
import streamlit as st

from components.cards import callout, kpi_row, page_footer, page_header, section_heading
from components.charts import (
    CHART_CONFIG,
    annual_ridership,
    borough_share,
    mode_distribution,
    monthly_timeline,
    top_stations,
)
from components.metrics import (
    compact_number,
    mode_label,
    require_metrics,
    short_station_name,
)
from components.sidebar import mount_dashboard
from config import TOTAL_BOROUGHS, TOTAL_RIDERSHIP, TOTAL_STATIONS, TOTAL_TRANSFERS

st.set_page_config(
    page_title="Overview | ChronoTunnel",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

mount_dashboard()


# -------------------------------------------------------------------
# Load published metrics
# -------------------------------------------------------------------

frames = require_metrics(
    {
        "yearly": "yearly_ridership.csv",
        "borough": "borough_ridership.csv",
        "stations": "top_stations.csv",
        "modes": "transit_mode_ridership.csv",
        "monthly": "monthly_ridership.csv",
    }
)


# -------------------------------------------------------------------
# Metric validation helpers
# -------------------------------------------------------------------


def prepare_numeric_metric(
    frame: pd.DataFrame,
    name: str,
    required_columns: set[str],
    numeric_columns: set[str],
) -> pd.DataFrame:
    """Validate required fields and prepare numeric metric columns."""

    if not isinstance(frame, pd.DataFrame) or frame.empty:
        st.error(f"The {name} metric contains no records.")
        st.stop()

    missing = required_columns - set(frame.columns)

    if missing:
        st.error(f"The {name} metric is missing columns: {', '.join(sorted(missing))}.")
        st.stop()

    data = frame.copy()

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

        if data[column].isna().any():
            st.error(f"The {name} metric contains missing or invalid {column} values.")
            st.stop()

        if (
            not data[column]
            .map(lambda value: pd.notna(value) and abs(value) != float("inf"))
            .all()
        ):
            st.error(f"The {name} metric contains non-finite values.")
            st.stop()

        if (data[column] < 0).any():
            st.error(f"The {name} metric contains negative values in {column}.")
            st.stop()

    return data


def category_share(
    frame: pd.DataFrame,
    category_column: str,
    category_value: str,
    metric_name: str,
) -> float:
    """Calculate the percentage contribution of one category."""

    selected = frame.loc[
        frame[category_column] == category_value,
        "total_ridership",
    ]

    if len(selected) != 1:
        st.error(
            f"The {metric_name} metric must contain exactly one "
            f"record for {category_value}."
        )
        st.stop()

    total = frame["total_ridership"].sum()

    if total <= 0:
        st.error(f"The {metric_name} metric has an invalid total.")
        st.stop()

    return float(selected.iloc[0] / total * 100)


# -------------------------------------------------------------------
# Prepare yearly metrics
# -------------------------------------------------------------------

yearly = prepare_numeric_metric(
    frames["yearly"],
    "Yearly ridership",
    {"year", "total_ridership"},
    {"year", "total_ridership"},
)

if not yearly["year"].mod(1).eq(0).all():
    st.error("Yearly ridership contains non-integer year values.")
    st.stop()

if yearly["year"].duplicated().any():
    st.error("Yearly ridership contains duplicate year records.")
    st.stop()

yearly["year"] = yearly["year"].astype(int)

yearly = yearly.sort_values(
    "year",
).reset_index(drop=True)

if len(yearly) < 2:
    st.error("At least two yearly records are required to calculate growth.")
    st.stop()

starting_ridership = yearly.iloc[0]["total_ridership"]

if starting_ridership <= 0:
    st.error("Cannot calculate annual growth from a zero starting value.")
    st.stop()

growth = (
    (yearly.iloc[-1]["total_ridership"] - starting_ridership) / starting_ridership * 100
)


# -------------------------------------------------------------------
# Prepare borough metrics
# -------------------------------------------------------------------

borough = prepare_numeric_metric(
    frames["borough"],
    "Borough ridership",
    {"borough", "total_ridership"},
    {"total_ridership"},
)

if borough["borough"].isna().any():
    st.error("Borough ridership contains missing borough names.")
    st.stop()

leader_borough = borough.sort_values(
    "total_ridership",
    ascending=False,
).iloc[0]

share = category_share(
    borough,
    "borough",
    leader_borough["borough"],
    "Borough ridership",
)


# -------------------------------------------------------------------
# Prepare transit mode metrics
# -------------------------------------------------------------------

modes = prepare_numeric_metric(
    frames["modes"],
    "Transit mode ridership",
    {"transit_mode", "total_ridership"},
    {"total_ridership"},
)

if modes["transit_mode"].isna().any():
    st.error("Transit mode metrics contain missing mode names.")
    st.stop()

subway_share = category_share(
    modes,
    "transit_mode",
    "subway",
    "Transit mode ridership",
)


# -------------------------------------------------------------------
# Prepare station metrics
# -------------------------------------------------------------------

stations = prepare_numeric_metric(
    frames["stations"],
    "Station ridership",
    {"station_complex", "borough", "total_ridership"},
    {"total_ridership"},
)

if stations[["station_complex", "borough"]].isna().any().any():
    st.error("Station metrics contain missing station or borough names.")
    st.stop()

station = stations.sort_values(
    "total_ridership",
    ascending=False,
).iloc[0]


# -------------------------------------------------------------------
# Page header
# -------------------------------------------------------------------

page_header(
    "NETWORK PERFORMANCE",
    "Ridership Overview",
    "A network-wide view of recorded New York City transit activity from 2020 to 2024.",
)


# -------------------------------------------------------------------
# Headline KPIs
# -------------------------------------------------------------------

kpi_row(
    [
        (
            "TOTAL RIDERSHIP",
            compact_number(TOTAL_RIDERSHIP),
            "January 2020–December 2024",
        ),
        (
            "TOTAL TRANSFERS",
            compact_number(TOTAL_TRANSFERS),
            "Included in the ridership total",
        ),
        (
            "STATION IDENTIFIERS",
            f"{TOTAL_STATIONS:,}",
            "Unique IDs in the reference data",
        ),
        (
            "BOROUGHS",
            str(TOTAL_BOROUGHS),
            "Citywide coverage",
        ),
    ]
)


# -------------------------------------------------------------------
# Annual ridership
# -------------------------------------------------------------------

section_heading(
    "Annual ridership trend",
    "Recorded ridership for each study year.",
)

st.plotly_chart(
    annual_ridership(yearly),
    use_container_width=True,
    config=CHART_CONFIG,
)


# -------------------------------------------------------------------
# Borough and transit mode distribution
# -------------------------------------------------------------------

left, right = st.columns(2, gap="medium")

with left:
    section_heading(
        "Borough contribution",
        "Share of total recorded ridership.",
    )

    st.plotly_chart(
        borough_share(borough),
        use_container_width=True,
        config=CHART_CONFIG,
    )

with right:
    section_heading(
        "Transit mode distribution",
        "Recorded ridership by mode.",
    )

    st.plotly_chart(
        mode_distribution(modes),
        use_container_width=True,
        config=CHART_CONFIG,
    )


# -------------------------------------------------------------------
# Leading station complexes
# -------------------------------------------------------------------

section_heading(
    "Top 15 stations",
    "The fifteen station complexes with the highest recorded ridership. "
    "Names are shortened on the axis; the hover shows the full complex name.",
)

st.plotly_chart(
    top_stations(stations, limit=15),
    use_container_width=True,
    config=CHART_CONFIG,
)


# -------------------------------------------------------------------
# Monthly ridership timeline
# -------------------------------------------------------------------

section_heading(
    "Monthly ridership timeline",
    "Systemwide monthly totals from the complete monthly dataset.",
)

st.plotly_chart(
    monthly_timeline(frames["monthly"]),
    use_container_width=True,
    config=CHART_CONFIG,
)


# -------------------------------------------------------------------
# Reading the overview
# -------------------------------------------------------------------

section_heading("Reading the overview")

callout(
    "OBSERVED",
    f"{leader_borough.borough} contributes {share:.2f}% of recorded ridership. "
    f"{mode_label('subway')} accounts for {subway_share:.1f}%. "
    f"{short_station_name(station.station_complex)} leads the station ranking. "
    f"Annual recorded ridership was {growth:.1f}% higher in "
    f"{int(yearly.iloc[-1].year)} than in {int(yearly.iloc[0].year)}. "
    "These are descriptions of the recorded series, not explanations of why it changed.",
)

callout(
    "DATA NOTE",
    "Monthly charts use the complete monthly dataset. Hourly views elsewhere "
    "use 120 sampled dates: one Wednesday and one Saturday per month. "
    "Transfers are shown separately and are already included in ridership.",
)


# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------

page_footer()
