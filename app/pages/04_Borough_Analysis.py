import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------
# PROJECT IMPORTS
# --------------------------------------------------

from src.chronotunnel.analysis.eda import get_borough_ridership
from src.chronotunnel.data.load import create_connection

from components.sidebar import mount_dashboard

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Borough Analysis | ChronoTunnel",
    page_icon="◆",
    layout="wide",
)

mount_dashboard()

# --------------------------------------------------
# DATAFRAME COLUMN MENU ACCENT
# --------------------------------------------------

st.markdown(
    """
    <style>
    div[data-testid="stDataFrameColumnMenu"] div[title] {
        background-color: #FF354D !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# THEME
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


def style_chart(fig, height=350):
    """Apply the shared ChronoTunnel dark chart theme."""

    fig.update_layout(
        height=height,
        font=dict(
            family=FONT,
            color=INK,
            size=12,
        ),
        title_font=dict(
            family=FONT,
            color=INK,
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
        tickfont=dict(color=MUTED, size=11),
        title_font=dict(color=MUTED),
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(color=INK, size=12),
        title_font=dict(color=MUTED),
    )

    return fig


# --------------------------------------------------
# HELPERS
# --------------------------------------------------


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


def format_number(value):
    return f"{float(value):,.0f}"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------


@st.cache_data(show_spinner=False)
def load_borough_data():
    connection = create_connection()

    try:
        return get_borough_ridership(connection)
    finally:
        connection.close()


try:
    borough_df = load_borough_data()

except Exception as error:
    st.error(
        "Could not load borough analysis data. "
        "Please verify the monthly dataset and DuckDB connection."
    )
    st.exception(error)
    st.stop()

if borough_df.empty:
    st.warning("No borough-level records are available.")
    st.stop()

# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------

borough_df = borough_df.copy()

borough_df["borough"] = borough_df["borough"].fillna("Unknown").astype(str).str.strip()

borough_df["borough"] = borough_df["borough"].replace("", "Unknown")

numeric_columns = [
    "total_ridership",
    "total_transfers",
    "unique_stations",
]

for column in numeric_columns:
    borough_df[column] = pd.to_numeric(
        borough_df[column],
        errors="coerce",
    ).fillna(0)

borough_df = borough_df.sort_values(
    "total_ridership",
    ascending=False,
).reset_index(drop=True)

total_ridership = borough_df["total_ridership"].sum()
total_transfers = borough_df["total_transfers"].sum()
total_stations = borough_df["unique_stations"].sum()
borough_count = borough_df["borough"].nunique()

if total_ridership > 0:
    borough_df["ridership_share"] = (
        borough_df["total_ridership"] / total_ridership * 100
    )
else:
    borough_df["ridership_share"] = 0.0

borough_df["average_ridership_per_station"] = (
    borough_df["total_ridership"] / borough_df["unique_stations"].replace(0, pd.NA)
).fillna(0)

borough_df["transfer_ratio"] = (
    borough_df["total_transfers"]
    / borough_df["total_ridership"].replace(0, pd.NA)
    * 100
).fillna(0)

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="page-eyebrow">GEOGRAPHIC INTELLIGENCE</div>
    <h1 class="page-title">Borough Analysis</h1>
    <p class="page-subtitle">
        Compare subway demand across New York City's boroughs,
        examine station coverage, and understand how ridership
        is distributed across the urban network.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

st.markdown("### Borough performance at a glance")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.metric(
        "Total ridership",
        compact_number(total_ridership),
    )

with metric_2:
    st.metric(
        "Total transfers",
        compact_number(total_transfers),
    )

with metric_3:
    st.metric(
        "Station complexes",
        format_number(total_stations),
    )

with metric_4:
    st.metric(
        "Boroughs represented",
        format_number(borough_count),
    )

st.markdown("---")

# --------------------------------------------------
# RIDERSHIP COMPARISON
# --------------------------------------------------

st.markdown("### Ridership distribution")

st.caption(
    "Compare the cumulative ridership recorded in each borough "
    "throughout the 2020–2024 study period."
)

chart_left, chart_right = st.columns(
    [1.6, 1],
    gap="large",
)

# --------------------------------------------------
# TOTAL RIDERSHIP BY BOROUGH
# --------------------------------------------------

with chart_left:
    ridership_plot = borough_df.sort_values(
        "total_ridership",
        ascending=True,
    )

    fig_ridership = px.bar(
        ridership_plot,
        x="total_ridership",
        y="borough",
        orientation="h",
        text="total_ridership",
        color="borough",
        color_discrete_map=BOROUGH_COLORS,
        category_orders={"borough": ridership_plot["borough"].tolist()},
        labels={
            "total_ridership": "Total ridership",
            "borough": "",
        },
    )

    fig_ridership.update_traces(
        texttemplate="%{text:.3s}",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=("<b>%{y}</b><br>Ridership: %{x:,.0f}<extra></extra>"),
    )

    fig_ridership = style_chart(
        fig_ridership,
        height=360,
    )

    fig_ridership.update_layout(
        margin=dict(l=10, r=65, t=15, b=10),
        showlegend=False,
    )

    fig_ridership.update_xaxes(
        showgrid=True,
        showticklabels=False,
        title=None,
    )

    st.plotly_chart(
        fig_ridership,
        use_container_width=True,
        config={"displayModeBar": False},
    )

# --------------------------------------------------
# RIDERSHIP SHARE
# --------------------------------------------------

with chart_right:
    fig_share = px.pie(
        borough_df,
        names="borough",
        values="total_ridership",
        hole=0.66,
        color="borough",
        color_discrete_map=BOROUGH_COLORS,
    )

    fig_share.update_traces(
        textposition="outside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Ridership: %{value:,.0f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
        marker=dict(
            line=dict(
                color="#08090D",
                width=3,
            )
        ),
    )

    fig_share = style_chart(
        fig_share,
        height=360,
    )

    fig_share.update_layout(
        margin=dict(l=10, r=10, t=15, b=35),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.16,
            xanchor="center",
            x=0.5,
            font=dict(
                family=FONT,
                size=10,
                color=MUTED,
            ),
        ),
        annotations=[
            dict(
                text="RIDERSHIP<br>SHARE",
                x=0.5,
                y=0.5,
                font=dict(
                    family=FONT,
                    size=12,
                    color=MUTED,
                ),
                showarrow=False,
            )
        ],
    )

    st.plotly_chart(
        fig_share,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.markdown("---")

# --------------------------------------------------
# STATION COVERAGE AND INTENSITY
# --------------------------------------------------

st.markdown("### Station coverage and demand intensity")

st.caption(
    "Explore how station coverage relates to cumulative ridership across boroughs."
)

coverage_left, coverage_right = st.columns(
    [1.3, 1],
    gap="large",
)

# --------------------------------------------------
# STATION COMPLEX COVERAGE
# --------------------------------------------------

with coverage_left:
    coverage_plot = borough_df.sort_values(
        "unique_stations",
        ascending=True,
    )

    fig_coverage = px.bar(
        coverage_plot,
        x="unique_stations",
        y="borough",
        orientation="h",
        text="unique_stations",
        color="borough",
        color_discrete_map=BOROUGH_COLORS,
        labels={
            "unique_stations": "Station complexes",
            "borough": "",
        },
    )

    fig_coverage.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=("<b>%{y}</b><br>Station complexes: %{x:,.0f}<extra></extra>"),
    )

    fig_coverage = style_chart(
        fig_coverage,
        height=330,
    )

    fig_coverage.update_layout(
        margin=dict(l=10, r=45, t=15, b=10),
        showlegend=False,
    )

    fig_coverage.update_xaxes(
        title=None,
    )

    st.plotly_chart(
        fig_coverage,
        use_container_width=True,
        config={"displayModeBar": False},
    )

# --------------------------------------------------
# AVERAGE RIDERSHIP PER STATION
# --------------------------------------------------

with coverage_right:
    intensity_plot = borough_df.sort_values(
        "average_ridership_per_station",
        ascending=True,
    )

    fig_intensity = px.bar(
        intensity_plot,
        x="average_ridership_per_station",
        y="borough",
        orientation="h",
        text="average_ridership_per_station",
        color="borough",
        color_discrete_map=BOROUGH_COLORS,
        labels={
            "average_ridership_per_station": ("Average ridership per station complex"),
            "borough": "",
        },
    )

    fig_intensity.update_traces(
        texttemplate="%{text:.3s}",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=("<b>%{y}</b><br>Average ridership: %{x:,.0f}<extra></extra>"),
    )

    fig_intensity = style_chart(
        fig_intensity,
        height=330,
    )

    fig_intensity.update_layout(
        margin=dict(l=10, r=55, t=15, b=10),
        showlegend=False,
    )

    fig_intensity.update_xaxes(
        showticklabels=False,
        title=None,
    )

    st.plotly_chart(
        fig_intensity,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.markdown("---")

# --------------------------------------------------
# BOROUGH DETAIL TABLE
# --------------------------------------------------

st.markdown("### Borough performance directory")

st.caption(
    "A detailed comparison of ridership, transfers, station "
    "complexes, and each borough's share of system-wide ridership."
)

display_df = borough_df[
    [
        "borough",
        "total_ridership",
        "total_transfers",
        "unique_stations",
        "ridership_share",
        "average_ridership_per_station",
        "transfer_ratio",
    ]
].copy()

display_df = display_df.rename(
    columns={
        "borough": "Borough",
        "total_ridership": "Total ridership",
        "total_transfers": "Total transfers",
        "unique_stations": "Station complexes",
        "ridership_share": "Ridership share (%)",
        "average_ridership_per_station": "Average ridership / station",
        "transfer_ratio": "Transfers / ridership (%)",
    }
)

styled_df = (
    display_df.style.format(
        {
            "Total ridership": "{:,.0f}",
            "Total transfers": "{:,.0f}",
            "Station complexes": "{:,.0f}",
            "Ridership share (%)": "{:.2f}%",
            "Average ridership / station": "{:,.0f}",
            "Transfers / ridership (%)": "{:.2f}%",
        }
    )
    .set_properties(
        **{
            "background-color": "#12151E",
            "color": "#F5F6FA",
            "border-color": "#343B4D",
        }
    )
    .set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#1B2030"),
                    ("color", "#FF6B9A"),
                    ("border-color", "#343B4D"),
                    ("font-weight", "600"),
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
        ]
    )
)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# KEY OBSERVATION
# --------------------------------------------------

top_borough = borough_df.iloc[0]

top_intensity = borough_df.loc[borough_df["average_ridership_per_station"].idxmax()]

st.markdown("---")

st.markdown("### What stands out?")

insight_left, insight_right = st.columns(2, gap="large")

with insight_left:
    st.markdown(
        f"""
        **Highest cumulative ridership**

        {top_borough["borough"]} records the highest cumulative
        ridership in the study period, with approximately
        **{compact_number(top_borough["total_ridership"])}**
        recorded entries.
        """
    )

with insight_right:
    st.markdown(
        f"""
        **Highest average ridership per station complex**

        {top_intensity["borough"]} has the highest average
        ridership per station complex, at approximately
        **{compact_number(top_intensity["average_ridership_per_station"])}**.
        """
    )

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------

with st.expander("Understanding the borough analysis"):
    st.markdown(
        """
        - **Study period:** January 2020 to December 2024.
        - **Ridership:** Sum of reported monthly ridership records
          for station complexes assigned to each borough.
        - **Transfers:** Sum of the separately reported transfer
          measure. Transfers are not added to ridership.
        - **Station complexes:** Distinct station complex IDs
          represented in the monthly dataset for each borough.
        - **Ridership share:** Borough ridership divided by
          total ridership across all boroughs.
        - **Average ridership per station:** Borough cumulative
          ridership divided by its distinct station complex count.

        These are cumulative historical measures, not live
        passenger counts or measures of station capacity.
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
        ChronoTunnel · BOROUGH INTELLIGENCE · HISTORICAL DATA 2020–2024
    </div>
    """,
    unsafe_allow_html=True,
)
