import sys
from pathlib import Path

# Add ChronoTunnel project root to Python import path.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.chronotunnel.analysis.temporal import (
    get_monthly_seasonality,
    get_peak_hour_concentration,
    get_weekday_weekend_comparison,
    get_year_over_year_growth,
)
from src.chronotunnel.data.load import create_connection

from components.sidebar import mount_dashboard

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Temporal Analysis | ChronoTunnel",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

mount_dashboard()

st.title("Temporal Analysis")

st.caption(
    "Explore how New York City's recorded transit ridership "
    "changed over time and across sampled hours of the day."
)

st.markdown(
    """
    This analysis examines monthly ridership trends, year-over-year
    changes, monthly patterns, and differences between sampled
    Wednesday and Saturday ridership.
    """
)


# ---------------------------------------------------------
# DATA VALIDATION HELPERS
# ---------------------------------------------------------


def validate_frame(
    frame: pd.DataFrame,
    name: str,
    required_columns: set[str],
) -> pd.DataFrame:
    """Validate an analysis DataFrame and its required columns."""

    if not isinstance(frame, pd.DataFrame) or frame.empty:
        st.error(f"{name} contains no records.")
        st.stop()

    missing = required_columns - set(frame.columns)

    if missing:
        st.error(f"{name} is missing required columns: {', '.join(sorted(missing))}.")
        st.stop()

    return frame.copy()


def validate_numeric_columns(
    frame: pd.DataFrame,
    name: str,
    columns: set[str],
    allow_missing: set[str] | None = None,
    allow_negative: set[str] | None = None,
) -> pd.DataFrame:
    """Convert selected columns to numeric and validate their values."""

    allow_missing = allow_missing or set()
    allow_negative = allow_negative or set()

    data = frame.copy()

    for column in columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

        if column not in allow_missing and data[column].isna().any():
            st.error(f"{name} contains missing or invalid values in {column}.")
            st.stop()

        finite_values = data[column].dropna()

        if not finite_values.map(lambda value: abs(value) != float("inf")).all():
            st.error(f"{name} contains non-finite values in {column}.")
            st.stop()

        if column not in allow_negative and (finite_values < 0).any():
            st.error(f"{name} contains negative values in {column}.")
            st.stop()

    return data


def validate_category_values(
    frame: pd.DataFrame,
    name: str,
    column: str,
) -> None:
    """Ensure a categorical field contains no missing values."""

    if frame[column].isna().any():
        st.error(f"{name} contains missing values in {column}.")
        st.stop()


# ---------------------------------------------------------
# LOAD ANALYSIS DATA
# ---------------------------------------------------------


@st.cache_data(show_spinner="Analyzing temporal ridership patterns...")
def load_temporal_data():
    """Load all temporal analysis outputs using one database connection."""

    connection = create_connection()

    try:
        yearly_growth = get_year_over_year_growth(connection)
        seasonality = get_monthly_seasonality(connection)
        hourly_comparison = get_weekday_weekend_comparison(connection)
        peak_concentration = get_peak_hour_concentration(connection)

    finally:
        connection.close()

    return (
        yearly_growth,
        seasonality,
        hourly_comparison,
        peak_concentration,
    )


try:
    (
        yearly_growth,
        seasonality,
        hourly_comparison,
        peak_concentration,
    ) = load_temporal_data()

except Exception as error:
    st.error(
        "Unable to load temporal analysis data. "
        "Please check that the data pipeline has completed successfully."
    )
    st.exception(error)
    st.stop()


# ---------------------------------------------------------
# PREPARE MONTHLY RIDERSHIP DATA
# ---------------------------------------------------------

monthly = validate_frame(
    yearly_growth,
    "Monthly ridership analysis",
    {"month", "total_ridership", "yoy_growth_percent"},
)

monthly["month"] = pd.to_datetime(
    monthly["month"],
    errors="coerce",
)

if monthly["month"].isna().any():
    st.error("Monthly ridership contains invalid month values.")
    st.stop()

monthly = validate_numeric_columns(
    monthly,
    "Monthly ridership analysis",
    {"total_ridership", "yoy_growth_percent"},
    allow_missing={"yoy_growth_percent"},
    allow_negative={"yoy_growth_percent"},
)

if monthly["month"].duplicated().any():
    st.error("Monthly ridership contains duplicate month records.")
    st.stop()

monthly = monthly.sort_values("month").reset_index(drop=True)

if monthly["total_ridership"].sum() <= 0:
    st.error("Monthly ridership has an invalid total.")
    st.stop()

monthly["year"] = monthly["month"].dt.year
monthly["month_number"] = monthly["month"].dt.month

annual_totals = monthly.groupby("year")["total_ridership"].transform("sum")

if (annual_totals <= 0).any():
    st.error("At least one year has an invalid ridership total.")
    st.stop()

monthly["annual_share_percent"] = (monthly["total_ridership"] / annual_totals) * 100


# ---------------------------------------------------------
# PREPARE MONTHLY SEASONALITY DATA
# ---------------------------------------------------------

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

season = validate_frame(
    seasonality,
    "Monthly seasonality analysis",
    {
        "month_name",
        "average_ridership_2020_2024",
        "average_ridership_2021_2024",
    },
)

validate_category_values(
    season,
    "Monthly seasonality analysis",
    "month_name",
)

season = validate_numeric_columns(
    season,
    "Monthly seasonality analysis",
    {
        "average_ridership_2020_2024",
        "average_ridership_2021_2024",
    },
)

if season["month_name"].duplicated().any():
    st.error("Monthly seasonality contains duplicate calendar months.")
    st.stop()

if set(season["month_name"]) != set(month_order):
    st.error("Monthly seasonality must contain exactly the twelve calendar months.")
    st.stop()

season["month_name"] = pd.Categorical(
    season["month_name"],
    categories=month_order,
    ordered=True,
)

season = season.sort_values("month_name")


# ---------------------------------------------------------
# PREPARE HOURLY COMPARISON DATA
# ---------------------------------------------------------

hourly = validate_frame(
    hourly_comparison,
    "Hourly ridership comparison",
    {"hour", "average_ridership", "day_name"},
)

validate_category_values(
    hourly,
    "Hourly ridership comparison",
    "day_name",
)

hourly = validate_numeric_columns(
    hourly,
    "Hourly ridership comparison",
    {"hour", "average_ridership"},
)

if not hourly["hour"].mod(1).eq(0).all():
    st.error("Hourly comparison contains non-integer hour values.")
    st.stop()

hourly["hour"] = hourly["hour"].astype(int)

if not hourly["hour"].between(0, 23).all():
    st.error("Hourly comparison contains hours outside 0–23.")
    st.stop()

day_names = ["Wednesday", "Saturday"]

hourly = hourly[hourly["day_name"].isin(day_names)].copy()

if hourly.empty:
    st.error("No Wednesday or Saturday hourly records are available.")
    st.stop()

if hourly.duplicated(subset=["day_name", "hour"]).any():
    st.error("Hourly comparison contains duplicate day/hour records.")
    st.stop()


# ---------------------------------------------------------
# PREPARE PEAK-PERIOD DATA
# ---------------------------------------------------------

peak = validate_frame(
    peak_concentration,
    "Peak-period concentration",
    {
        "day_name",
        "ridership_weighted_peak_share_percent",
        "average_daily_peak_share_percent",
        "average_daily_ridership",
        "average_peak_period_ridership",
    },
)

validate_category_values(
    peak,
    "Peak-period concentration",
    "day_name",
)

peak = validate_numeric_columns(
    peak,
    "Peak-period concentration",
    {
        "ridership_weighted_peak_share_percent",
        "average_daily_peak_share_percent",
        "average_daily_ridership",
        "average_peak_period_ridership",
    },
)

peak = peak[peak["day_name"].isin(day_names)].copy()

if peak["day_name"].duplicated().any():
    st.error("Peak-period concentration contains duplicate day records.")
    st.stop()

for column in (
    "ridership_weighted_peak_share_percent",
    "average_daily_peak_share_percent",
):
    if not peak[column].between(0, 100).all():
        st.error(f"Peak-period concentration contains invalid percentages in {column}.")
        st.stop()


# ---------------------------------------------------------
# CHRONOTUNNEL CHART THEME
# ---------------------------------------------------------

RED = "#FF354D"
BLUE = "#7BA7FF"
PINK = "#FF6B9A"
PURPLE = "#A78BFA"
ORANGE = "#FFAD70"

INK = "#F5F6FA"
MUTED = "#A7B0C2"
GRID = "rgba(255,255,255,0.09)"

CHART_PALETTE = [RED, BLUE, PINK, PURPLE, ORANGE]


def style_chart(fig, height=390):
    """Apply the shared ChronoTunnel dark chart theme."""

    fig.update_layout(
        height=height,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, sans-serif",
            color=INK,
            size=12,
        ),
        title=dict(
            font=dict(
                family="Space Grotesk, sans-serif",
                size=17,
                color=INK,
            ),
            x=0.01,
            xanchor="left",
        ),
        margin=dict(l=15, r=15, t=55, b=15),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=MUTED),
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor="#171B27",
            bordercolor="rgba(255,255,255,0.12)",
            font=dict(
                family="DM Sans, sans-serif",
                color=INK,
                size=12,
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linecolor=GRID,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
        zeroline=False,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    return fig


def format_number(value):
    """Format a numeric value with thousands separators."""

    return f"{value:,.0f}"


# ---------------------------------------------------------
# SECTION 1: MONTHLY RIDERSHIP TREND
# ---------------------------------------------------------

st.divider()

st.subheader("01 · Monthly Ridership Trend")

st.markdown(
    """
    Track monthly network-wide ridership across the five-year
    study period. The trend highlights the major decline in 2020
    and the subsequent recovery in recorded ridership.
    """
)

total_months = monthly["month"].nunique()
total_ridership = monthly["total_ridership"].sum()
latest_month = monthly.iloc[-1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Months analyzed",
        f"{total_months}",
        help="Complete monthly coverage from January 2020 to December 2024.",
    )

with col2:
    st.metric(
        "Total recorded ridership",
        format_number(total_ridership),
        help="Sum of monthly ridership across the five-year study period.",
    )

with col3:
    st.metric(
        "Latest month",
        latest_month["month"].strftime("%b %Y"),
        help="Most recent month in the prepared dataset.",
    )


trend_fig = go.Figure()

trend_fig.add_trace(
    go.Scatter(
        x=monthly["month"],
        y=monthly["total_ridership"],
        mode="lines",
        name="Monthly ridership",
        line=dict(
            color=RED,
            width=2.8,
        ),
        fill="tozeroy",
        fillcolor="rgba(255,53,77,0.10)",
        hovertemplate=("%{x|%B %Y}<br>Ridership: %{y:,.0f}<extra></extra>"),
    )
)

trend_fig.update_layout(
    title="Monthly network-wide ridership · 2020–2024",
    xaxis_title="Month",
    yaxis_title="Recorded ridership",
)

style_chart(trend_fig, 420)

st.plotly_chart(
    trend_fig,
    use_container_width=True,
    config={"displayModeBar": "hover", "displaylogo": False},
)


# ---------------------------------------------------------
# SECTION 2: YEAR-OVER-YEAR GROWTH
# ---------------------------------------------------------

st.subheader("Year-over-Year Change")

st.markdown(
    """
    Compare each month's ridership with the same month in the
    preceding year. This helps distinguish annual change from
    ordinary month-to-month variation.
    """
)

growth = monthly.dropna(subset=["yoy_growth_percent"]).copy()

if growth.empty:
    st.warning("No valid year-over-year growth observations are available.")
else:
    growth_fig = go.Figure()

    growth_fig.add_trace(
        go.Bar(
            x=growth["month"],
            y=growth["yoy_growth_percent"],
            marker_color=[
                BLUE if value >= 0 else RED for value in growth["yoy_growth_percent"]
            ],
            name="Year-over-year change",
            hovertemplate=("%{x|%B %Y}<br>Change: %{y:.2f}%<extra></extra>"),
        )
    )

    growth_fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=MUTED,
        line_width=1,
    )

    growth_fig.update_layout(
        title="Monthly year-over-year ridership change",
        xaxis_title="Month",
        yaxis_title="Change compared with previous year (%)",
    )

    style_chart(growth_fig, 370)

    st.plotly_chart(
        growth_fig,
        use_container_width=True,
        config={"displayModeBar": "hover", "displaylogo": False},
    )


# ---------------------------------------------------------
# SECTION 3: MONTHLY SEASONALITY
# ---------------------------------------------------------

st.divider()

st.subheader("02 · Monthly Ridership Patterns")

st.markdown(
    """
    Compare average ridership across calendar months using two
    study windows: the complete 2020–2024 period and 2021–2024,
    which excludes the exceptional first pandemic year.
    """
)

season_fig = go.Figure()

season_fig.add_trace(
    go.Bar(
        x=season["month_name"].astype(str),
        y=season["average_ridership_2020_2024"],
        name="Average · 2020–2024",
        marker_color=BLUE,
        opacity=0.72,
        hovertemplate=(
            "%{x}<br>Average ridership (2020–2024): %{y:,.0f}<extra></extra>"
        ),
    )
)

season_fig.add_trace(
    go.Bar(
        x=season["month_name"].astype(str),
        y=season["average_ridership_2021_2024"],
        name="Average · 2021–2024",
        marker_color=RED,
        hovertemplate=(
            "%{x}<br>Average ridership (2021–2024): %{y:,.0f}<extra></extra>"
        ),
    )
)

season_fig.update_layout(
    title="Average ridership by calendar month",
    xaxis_title="Calendar month",
    yaxis_title="Average recorded ridership",
    barmode="group",
)

style_chart(season_fig, 390)

st.plotly_chart(
    season_fig,
    use_container_width=True,
    config={"displayModeBar": "hover", "displaylogo": False},
)


# ---------------------------------------------------------
# NORMALIZED MONTHLY SHARE
# ---------------------------------------------------------

st.subheader("Monthly Share Within Each Year")

st.markdown(
    """
    To reduce the influence of differences in total annual
    ridership, compare each month's share of its own year's
    ridership total.
    """
)

share_fig = go.Figure()

for index, year in enumerate(sorted(monthly["year"].unique())):
    year_data = monthly[monthly["year"] == year].sort_values("month_number")

    share_fig.add_trace(
        go.Scatter(
            x=year_data["month_number"],
            y=year_data["annual_share_percent"],
            mode="lines+markers",
            name=str(year),
            line=dict(
                color=CHART_PALETTE[index % len(CHART_PALETTE)],
                width=2.2,
            ),
            marker=dict(size=6),
            hovertemplate=(
                f"{year} · Month %{{x}}<br>"
                "Share of annual ridership: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

share_fig.update_layout(
    title="Each month's contribution to its own year's ridership",
    xaxis=dict(
        title="Calendar month",
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    ),
    yaxis_title="Share of annual ridership (%)",
)

style_chart(share_fig, 400)

st.plotly_chart(
    share_fig,
    use_container_width=True,
    config={"displayModeBar": "hover", "displaylogo": False},
)


# ---------------------------------------------------------
# SECTION 4: WEDNESDAY VS SATURDAY HOURLY PROFILE
# ---------------------------------------------------------

st.divider()

st.subheader("03 · Wednesday vs Saturday")

st.markdown(
    """
    Examine how the hourly distribution of recorded ridership
    differs between the selected Wednesdays and Saturdays.

    Each day type contains 60 sampled dates, with one selected
    date per month from 2020 through 2024.
    """
)

hourly_fig = go.Figure()

day_colors = {
    "Wednesday": BLUE,
    "Saturday": PINK,
}

for day in ["Wednesday", "Saturday"]:
    day_data = hourly[hourly["day_name"] == day].sort_values("hour")

    if not day_data.empty:
        hourly_fig.add_trace(
            go.Scatter(
                x=day_data["hour"],
                y=day_data["average_ridership"],
                mode="lines+markers",
                name=day,
                line=dict(
                    color=day_colors[day],
                    width=2.8,
                ),
                marker=dict(size=6),
                hovertemplate=(
                    f"{day}<br>"
                    "Hour: %{x}:00<br>"
                    "Average ridership: %{y:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

hourly_fig.update_layout(
    title="Average hourly ridership by sampled day",
    xaxis=dict(
        title="Hour of day",
        tickmode="linear",
        dtick=1,
        range=[0, 23],
    ),
    yaxis_title="Average recorded ridership",
)

style_chart(hourly_fig, 420)

st.plotly_chart(
    hourly_fig,
    use_container_width=True,
    config={"displayModeBar": "hover", "displaylogo": False},
)


# ---------------------------------------------------------
# SECTION 5: PEAK-PERIOD CONCENTRATION
# ---------------------------------------------------------

st.subheader("Peak-Period Concentration")

st.markdown(
    """
    Compare the share of sampled daily ridership recorded during
    the selected peak windows: 07:00–09:00 and 16:00–18:00.

    These are analytical time windows used in this project,
    not an independently verified official MTA peak-period definition.
    """
)

wed = peak[peak["day_name"] == "Wednesday"]
sat = peak[peak["day_name"] == "Saturday"]

if not wed.empty and not sat.empty:
    wed_row = wed.iloc[0]
    sat_row = sat.iloc[0]

    wed_weighted_share = wed_row["ridership_weighted_peak_share_percent"]
    sat_weighted_share = sat_row["ridership_weighted_peak_share_percent"]

    wed_average_share = wed_row["average_daily_peak_share_percent"]
    sat_average_share = sat_row["average_daily_peak_share_percent"]

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Wednesday weighted peak share",
            f"{wed_weighted_share:.2f}%",
            help=(
                "Peak-period ridership divided by total ridership "
                "across sampled Wednesdays."
            ),
        )

    with metric2:
        st.metric(
            "Saturday weighted peak share",
            f"{sat_weighted_share:.2f}%",
            help=(
                "Peak-period ridership divided by total ridership "
                "across sampled Saturdays."
            ),
        )

    with metric3:
        difference = wed_weighted_share - sat_weighted_share

        st.metric(
            "Weighted share difference",
            f"{difference:.2f} pp",
            help=("Wednesday weighted peak share minus Saturday weighted peak share."),
        )

    peak_fig = go.Figure()

    peak_fig.add_trace(
        go.Bar(
            x=peak["day_name"],
            y=peak["average_daily_ridership"],
            name="Average daily ridership",
            marker_color=BLUE,
            opacity=0.72,
            hovertemplate=("%{x}<br>Average daily ridership: %{y:,.0f}<extra></extra>"),
        )
    )

    peak_fig.add_trace(
        go.Bar(
            x=peak["day_name"],
            y=peak["average_peak_period_ridership"],
            name="Average peak-window ridership",
            marker_color=RED,
            hovertemplate=(
                "%{x}<br>Average peak-window ridership: %{y:,.0f}<extra></extra>"
            ),
        )
    )

    peak_fig.update_layout(
        title="Average daily ridership and selected peak-window ridership",
        barmode="group",
        xaxis_title="Sampled day",
        yaxis_title="Average recorded ridership",
    )

    style_chart(peak_fig, 370)

    st.plotly_chart(
        peak_fig,
        use_container_width=True,
        config={"displayModeBar": "hover", "displaylogo": False},
    )

    with st.expander("Compare peak-share calculation methods"):
        st.markdown(
            """
            The analysis provides two different summaries:

            - **Ridership-weighted peak share:** Total peak-window
              ridership divided by total daily ridership across
              all sampled dates of that day type.
            - **Average daily peak share:** The arithmetic mean
              of the individual sampled dates' peak-period shares.

            These measures can differ because sampled dates have
            different total ridership levels.
            """
        )

        comparison = pd.DataFrame(
            {
                "Sampled day": ["Wednesday", "Saturday"],
                "Ridership-weighted peak share (%)": [
                    wed_weighted_share,
                    sat_weighted_share,
                ],
                "Average daily peak share (%)": [
                    wed_average_share,
                    sat_average_share,
                ],
            }
        )

        st.dataframe(
            comparison,
            hide_index=True,
            use_container_width=True,
        )

else:
    st.warning(
        "Peak-period comparison could not be displayed because "
        "one or both sampled day groups are missing."
    )


# ---------------------------------------------------------
# SECTION 6: INTERPRETATION AND DATA LIMITATIONS
# ---------------------------------------------------------

st.divider()

st.subheader("04 · What the Temporal Patterns Tell Us")

st.markdown(
    """
    **How to interpret this analysis**

    - Monthly ridership shows the network's longer-term trajectory
      across the 2020–2024 study period.
    - Year-over-year percentages compare the same calendar month
      across consecutive years.
    - The seasonality comparison shows how including or excluding
      2020 changes the average ridership pattern.
    - The normalized monthly-share chart compares each month
      relative to its own year's total.
    - Wednesday and Saturday profiles describe the selected
      dates in the hourly sample, not every Wednesday or Saturday.
    - Peak-window shares describe recorded ridership concentration
      within the project's chosen time windows.
    """
)

with st.expander("Dataset and methodology limitations"):
    st.markdown(
        """
        1. **Historical coverage:** Monthly records cover January
           2020 through December 2024.

        2. **Hourly sampling:** Hourly comparisons use 120 selected
           dates: one Wednesday and one Saturday per month.

        3. **Sampling interpretation:** The hourly dataset is not a
           continuous time series and should not be generalized to
           every day in the year.

        4. **Missing station-hour rows:** An absent station-hour
           record should not automatically be interpreted as zero
           ridership.

        5. **Ridership vs. capacity:** The data measures recorded
           ridership and transfers. It does not directly measure
           passenger occupancy, overcrowding, train capacity,
           or train frequency.

        6. **Transfers:** Transfers are already included in
           ridership and must not be added to it.

        7. **Seasonality:** The 2020–2024 averages include the
           exceptional pandemic period. The 2021–2024 comparison
           provides an additional perspective but does not remove
           all year-to-year differences.
        """
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "ChronoTunnel · Temporal Analysis · MTA Subway Hourly Ridership "
    "2020–2024 · Historical analysis, not a live operations feed."
)
