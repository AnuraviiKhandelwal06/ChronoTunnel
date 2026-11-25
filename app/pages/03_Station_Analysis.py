import sys
from pathlib import Path

# Add ChronoTunnel project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.chronotunnel.data.load import create_connection

from components.sidebar import mount_dashboard

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

mount_dashboard()

# ChronoTunnel dropdown and search styling
st.markdown(
    """
    <style>
    /* Dropdown controls */
    div[data-testid="stSelectbox"] [data-baseweb="select"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] [role="combobox"] {
        background-color: #171B26 !important;
        background: #171B26 !important;
        border: 1px solid #343B4D !important;
        border-radius: 9px !important;
        color: #F5F6FA !important;
        box-shadow: none !important;
    }

    /* Selected value and dropdown text */
    div[data-testid="stSelectbox"] [data-baseweb="select"] *,
    div[data-testid="stSelectbox"] [role="combobox"] * {
        color: #F5F6FA !important;
        -webkit-text-fill-color: #F5F6FA !important;
    }

    /* Dropdown arrow */
    div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
        color: #A7B0C2 !important;
        fill: #A7B0C2 !important;
    }

    /* Dropdown options menu */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul {
        background-color: #171B26 !important;
    }

    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="popover"] [role="option"] * {
        background-color: #171B26 !important;
        color: #F5F6FA !important;
        -webkit-text-fill-color: #F5F6FA !important;
    }

    div[data-baseweb="popover"] [role="option"]:hover {
        background-color: #292E3C !important;
    }

    /* Search input */
    div[data-testid="stTextInput"] input {
        background-color: #171B26 !important;
        color: #F5F6FA !important;
        -webkit-text-fill-color: #F5F6FA !important;
        border: 1px solid #343B4D !important;
        border-radius: 9px !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #A7B0C2 !important;
        -webkit-text-fill-color: #A7B0C2 !important;
        opacity: 1 !important;
    }
    /* Dataframe column menu — coral accent */
    div[data-testid="stDataFrameColumnMenu"] div[title] {
        background-color: #FF354D !important;
        border-color: #FF354D !important;
        border-radius: 6px !important;
    }

    div[data-testid="stDataFrameColumnMenu"] div[title] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    /* Dropdown arrow button: match the dark dropdown background */
    div[data-testid="stSelectbox"] button[aria-label="Open"] {
        background-color: #171B26 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Dropdown arrow icon */
    div[data-testid="stSelectbox"] button[aria-label="Open"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Station Analysis")

st.caption(
    "Explore station-level ridership, compare transit locations, "
    "and investigate how demand varies across New York City."
)


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

CHART_PALETTE = [
    RED,
    BLUE,
    PINK,
    PURPLE,
    ORANGE,
]

BOROUGH_COLORS = {
    "Manhattan": RED,
    "Brooklyn": BLUE,
    "Queens": PINK,
    "Bronx": PURPLE,
    "Staten Island": ORANGE,
}

STATION_IDENTITY_COLUMNS = [
    "station_complex_id",
    "station_complex",
    "borough",
    "transit_mode",
]

NUMERIC_STATION_COLUMNS = [
    "total_ridership",
    "total_transfers",
    "months_recorded",
]

NUMERIC_MONTHLY_COLUMNS = [
    "ridership",
    "transfers",
]


# ---------------------------------------------------------
# VALIDATION HELPERS
# ---------------------------------------------------------


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
    dataset_name: str,
) -> None:
    """Ensure a dataframe contains all required columns."""

    missing_columns = sorted(set(required_columns) - set(dataframe.columns))

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: {', '.join(missing_columns)}"
        )


def validate_numeric_columns(
    dataframe: pd.DataFrame,
    columns: list[str],
    dataset_name: str,
) -> pd.DataFrame:
    """Convert selected columns to numeric and validate their values."""

    result = dataframe.copy()

    for column in columns:
        result[column] = pd.to_numeric(result[column], errors="coerce")

        if result[column].isna().any():
            raise ValueError(
                f"{dataset_name} contains missing or non-numeric values in '{column}'."
            )

        if not np.isfinite(result[column].to_numpy(dtype=float)).all():
            raise ValueError(f"{dataset_name} contains infinite values in '{column}'.")

        if (result[column] < 0).any():
            raise ValueError(f"{dataset_name} contains negative values in '{column}'.")

    return result


def validate_station_data(
    stations: pd.DataFrame,
    monthly: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Validate station-level and monthly station-level datasets."""

    station_columns = [
        *STATION_IDENTITY_COLUMNS,
        *NUMERIC_STATION_COLUMNS,
    ]

    monthly_columns = [
        "month",
        *STATION_IDENTITY_COLUMNS,
        *NUMERIC_MONTHLY_COLUMNS,
    ]

    validate_required_columns(
        stations,
        station_columns,
        "Station dataset",
    )

    validate_required_columns(
        monthly,
        monthly_columns,
        "Monthly dataset",
    )

    if stations.empty:
        raise ValueError("The station dataset contains no records.")

    if monthly.empty:
        raise ValueError("The monthly dataset contains no records.")

    stations = stations.copy()
    monthly = monthly.copy()

    # Normalize station identity fields.
    for column in STATION_IDENTITY_COLUMNS:
        stations[column] = (
            stations[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )

        monthly[column] = (
            monthly[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )

    # Validate numeric measures.
    stations = validate_numeric_columns(
        stations,
        NUMERIC_STATION_COLUMNS,
        "Station dataset",
    )

    monthly = validate_numeric_columns(
        monthly,
        NUMERIC_MONTHLY_COLUMNS,
        "Monthly dataset",
    )

    # Month values must be valid dates.
    monthly["month"] = pd.to_datetime(
        monthly["month"],
        errors="coerce",
    )

    if monthly["month"].isna().any():
        raise ValueError(
            "The monthly dataset contains invalid or missing month values."
        )

    # Normalize dates to the first day of each month.
    monthly["month"] = monthly["month"].dt.to_period("M").dt.to_timestamp()

    # Validate historical coverage.
    if (
        not monthly["month"]
        .between(
            pd.Timestamp("2020-01-01"),
            pd.Timestamp("2024-12-01"),
        )
        .all()
    ):
        raise ValueError(
            "The monthly dataset contains dates outside "
            "the January 2020–December 2024 analysis period."
        )

    # Validate recorded month counts.
    if (
        (stations["months_recorded"] < 1)
        | (stations["months_recorded"] > 60)
        | (stations["months_recorded"] % 1 != 0)
    ).any():
        raise ValueError("Station dataset contains invalid months_recorded values.")

    stations["months_recorded"] = stations["months_recorded"].astype(int)

    # Check station-level identity uniqueness.
    if stations.duplicated(STATION_IDENTITY_COLUMNS).any():
        raise ValueError(
            "The station dataset contains duplicate station-mode identities."
        )

    # Check monthly identity uniqueness.
    monthly_identity = [
        "month",
        *STATION_IDENTITY_COLUMNS,
    ]

    if monthly.duplicated(monthly_identity).any():
        raise ValueError(
            "The monthly dataset contains duplicate station-mode-month records."
        )

    # Ensure monthly data contains only known station identities.
    station_identities = stations[STATION_IDENTITY_COLUMNS].drop_duplicates()

    monthly_identities = monthly[STATION_IDENTITY_COLUMNS].drop_duplicates()

    unmatched = monthly_identities.merge(
        station_identities,
        on=STATION_IDENTITY_COLUMNS,
        how="left",
        indicator=True,
    )

    if (unmatched["_merge"] == "left_only").any():
        raise ValueError(
            "Some monthly records do not have a matching station identity."
        )

    # Confirm station-level totals agree with monthly records.
    monthly_totals = monthly.groupby(
        STATION_IDENTITY_COLUMNS,
        as_index=False,
    ).agg(
        total_ridership=("ridership", "sum"),
        total_transfers=("transfers", "sum"),
        months_recorded=("month", "nunique"),
    )

    comparison = stations.merge(
        monthly_totals,
        on=STATION_IDENTITY_COLUMNS,
        how="left",
        suffixes=("_station", "_monthly"),
        validate="one_to_one",
    )

    if comparison["total_ridership_monthly"].isna().any():
        raise ValueError(
            "Some station records have no matching monthly ridership history."
        )

    for metric in ["total_ridership", "total_transfers"]:
        station_values = comparison[f"{metric}_station"].to_numpy(dtype=float)
        monthly_values = comparison[f"{metric}_monthly"].to_numpy(dtype=float)

        if not np.allclose(
            station_values,
            monthly_values,
            rtol=1e-9,
            atol=1e-6,
        ):
            raise ValueError(
                f"Station-level and monthly '{metric}' totals do not match."
            )

    if not (
        comparison["months_recorded_station"] == comparison["months_recorded_monthly"]
    ).all():
        raise ValueError(
            "Station-level months_recorded values do not match the monthly dataset."
        )

    # Ensure ranking is numeric and deterministic.
    stations = stations.sort_values(
        "total_ridership",
        ascending=False,
        kind="stable",
    ).reset_index(drop=True)

    monthly = monthly.sort_values(
        ["month", *STATION_IDENTITY_COLUMNS],
        kind="stable",
    ).reset_index(drop=True)

    return stations, monthly


# ---------------------------------------------------------
# LOAD STATION DATA
# ---------------------------------------------------------


@st.cache_data(show_spinner="Loading station-level ridership...")
def load_station_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load station totals and monthly station-level records."""

    connection = create_connection()

    try:
        station_query = """
            SELECT
                station_complex_id,
                station_complex,
                borough,
                transit_mode,
                SUM(ridership) AS total_ridership,
                SUM(transfers) AS total_transfers,
                COUNT(DISTINCT month) AS months_recorded
            FROM monthly
            GROUP BY
                station_complex_id,
                station_complex,
                borough,
                transit_mode
            ORDER BY total_ridership DESC
        """

        monthly_query = """
            SELECT
                CAST(month AS DATE) AS month,
                station_complex_id,
                station_complex,
                borough,
                transit_mode,
                SUM(ridership) AS ridership,
                SUM(transfers) AS transfers
            FROM monthly
            GROUP BY
                month,
                station_complex_id,
                station_complex,
                borough,
                transit_mode
            ORDER BY month
        """

        stations = connection.execute(station_query).df()
        monthly = connection.execute(monthly_query).df()

    finally:
        connection.close()

    return validate_station_data(stations, monthly)


try:
    stations, monthly = load_station_data()

except Exception as error:
    st.error(
        "Could not load or validate station data. "
        "Please verify the monthly DuckDB view and its columns."
    )
    st.exception(error)
    st.stop()

if stations.empty:
    st.warning("No station records were found in the monthly dataset.")
    st.stop()


# ---------------------------------------------------------
# CHART STYLE
# ---------------------------------------------------------


def style_chart(fig: go.Figure, height: int = 380) -> go.Figure:
    """Apply the ChronoTunnel chart theme."""

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
        hoverlabel=dict(
            bgcolor="#171B27",
            bordercolor="rgba(255,255,255,0.12)",
            font=dict(
                family="DM Sans, sans-serif",
                color=INK,
                size=12,
            ),
        ),
        legend=dict(
            font=dict(color=MUTED),
            bgcolor="rgba(0,0,0,0)",
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


def format_number(value: float) -> str:
    """Format a numeric value for display."""

    return f"{value:,.0f}"


# ---------------------------------------------------------
# STATION DIRECTORY AND FILTERS
# ---------------------------------------------------------

st.divider()

st.subheader("Station Directory")

st.write(
    "Search and filter the network to find individual station "
    "complexes and compare their recorded ridership."
)

filter1, filter2, filter3 = st.columns([2, 1, 1])

with filter1:
    search_text = st.text_input(
        "Search station",
        placeholder="Enter a station name or ID...",
    )

with filter2:
    borough_options = ["All Boroughs"] + sorted(stations["borough"].unique().tolist())

    selected_borough = st.selectbox(
        "Borough",
        borough_options,
    )

with filter3:
    mode_options = ["All Modes"] + sorted(stations["transit_mode"].unique().tolist())

    selected_mode = st.selectbox(
        "Transit Mode",
        mode_options,
    )


filtered = stations.copy()

if search_text.strip():
    search_lower = search_text.strip().lower()

    station_name_matches = (
        filtered["station_complex"]
        .str.lower()
        .str.contains(
            search_lower,
            na=False,
            regex=False,
        )
    )

    station_id_matches = filtered["station_complex_id"].str.contains(
        search_lower,
        na=False,
        regex=False,
    )

    filtered = filtered[station_name_matches | station_id_matches]

if selected_borough != "All Boroughs":
    filtered = filtered[filtered["borough"] == selected_borough]

if selected_mode != "All Modes":
    filtered = filtered[filtered["transit_mode"] == selected_mode]

filtered = filtered.sort_values(
    "total_ridership",
    ascending=False,
    kind="stable",
)


# ---------------------------------------------------------
# FILTERED RESULTS
# ---------------------------------------------------------

result_col1, result_col2 = st.columns(2)

with result_col1:
    st.metric(
        "Matching station-mode records",
        f"{len(filtered):,}",
    )

with result_col2:
    st.metric(
        "Recorded ridership in selection",
        format_number(filtered["total_ridership"].sum()),
    )


if filtered.empty:
    st.info(
        "No stations match the selected search and filters. "
        "Try changing your search or selecting a different borough or mode."
    )

else:
    display_df = filtered[
        [
            "station_complex_id",
            "station_complex",
            "borough",
            "transit_mode",
            "total_ridership",
            "total_transfers",
            "months_recorded",
        ]
    ].rename(
        columns={
            "station_complex_id": "Station ID",
            "station_complex": "Station Complex",
            "borough": "Borough",
            "transit_mode": "Transit Mode",
            "total_ridership": "Total Ridership",
            "total_transfers": "Total Transfers",
            "months_recorded": "Months Recorded",
        }
    )

    styled_df = (
        display_df.style.format(
            {
                "Total Ridership": "{:,.0f}",
                "Total Transfers": "{:,.0f}",
                "Months Recorded": "{:,.0f}",
            }
        )
        .set_properties(
            **{
                "background-color": "#12151E",
                "color": "#F5F6FA",
                "border-color": "rgba(255,255,255,0.08)",
                "text-align": "left",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#1C2230"),
                        ("color", "#B8C5DA"),
                        ("font-weight", "600"),
                        ("border-color", "rgba(255,255,255,0.10)"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border-color", "rgba(255,255,255,0.07)"),
                    ],
                },
            ]
        )
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=350,
    )


# ---------------------------------------------------------
# TOP 10 STATIONS
# ---------------------------------------------------------

st.divider()

st.subheader("Top 10 Station-Mode Records")

st.write(
    "The ranking uses station ID and transit mode together. "
    "This avoids combining distinct transit modes that share an ID."
)

top10 = (
    stations.nlargest(10, "total_ridership")
    .sort_values("total_ridership", ascending=True)
    .copy()
)

top_fig = px.bar(
    top10,
    x="total_ridership",
    y="station_complex",
    color="transit_mode",
    orientation="h",
    color_discrete_sequence=CHART_PALETTE,
    hover_data=[
        "station_complex_id",
        "borough",
        "total_transfers",
    ],
    labels={
        "total_ridership": "Total recorded ridership",
        "station_complex": "Station complex",
        "transit_mode": "Transit mode",
        "station_complex_id": "Station ID",
        "borough": "Borough",
        "total_transfers": "Recorded transfers",
    },
    title="Highest-ridership station-mode records",
)

top_fig.update_layout(
    yaxis_title="",
    legend_title="Transit mode",
)

style_chart(top_fig, 480)

st.plotly_chart(
    top_fig,
    use_container_width=True,
    config={
        "displayModeBar": "hover",
        "displaylogo": False,
    },
)


# ---------------------------------------------------------
# BOROUGH DISTRIBUTION
# ---------------------------------------------------------

st.subheader("Station Ridership by Borough")

borough_data = (
    stations.groupby("borough", as_index=False)
    .agg(
        total_ridership=("total_ridership", "sum"),
        total_transfers=("total_transfers", "sum"),
    )
    .sort_values("total_ridership", ascending=False)
)

borough_fig = px.bar(
    borough_data,
    x="borough",
    y="total_ridership",
    color="borough",
    color_discrete_map=BOROUGH_COLORS,
    hover_data=["total_transfers"],
    labels={
        "borough": "Borough",
        "total_ridership": "Recorded ridership",
        "total_transfers": "Recorded transfers",
    },
    title="Combined station-mode ridership by borough",
)

borough_fig.update_layout(
    showlegend=False,
    xaxis_title="Borough",
    yaxis_title="Recorded ridership",
)

style_chart(borough_fig, 370)

st.plotly_chart(
    borough_fig,
    use_container_width=True,
    config={
        "displayModeBar": "hover",
        "displaylogo": False,
    },
)


# ---------------------------------------------------------
# INDIVIDUAL STATION INVESTIGATION
# ---------------------------------------------------------

st.divider()

st.subheader("Individual Station Investigation")

st.write("Select a station-mode record to inspect its monthly ridership history.")

station_options = stations.copy()

station_options["selection_label"] = (
    station_options["station_complex"]
    + " | "
    + station_options["transit_mode"]
    + " | ID "
    + station_options["station_complex_id"]
)

selected_station_label = st.selectbox(
    "Choose a station",
    station_options["selection_label"].tolist(),
)

selected_station = station_options.loc[
    station_options["selection_label"] == selected_station_label
].iloc[0]

# Match the complete station identity.
selected_monthly = monthly.copy()

for column in STATION_IDENTITY_COLUMNS:
    selected_monthly = selected_monthly[
        selected_monthly[column] == selected_station[column]
    ]

selected_monthly = selected_monthly.sort_values("month").reset_index(drop=True)


# ---------------------------------------------------------
# STATION PROFILE
# ---------------------------------------------------------

st.markdown("#### Station Profile")

profile1, profile2, profile3, profile4 = st.columns(4)

with profile1:
    st.metric("Borough", selected_station["borough"])

with profile2:
    st.metric("Transit mode", selected_station["transit_mode"])

with profile3:
    st.metric(
        "Total ridership",
        format_number(selected_station["total_ridership"]),
    )

with profile4:
    st.metric(
        "Total transfers",
        format_number(selected_station["total_transfers"]),
    )


# ---------------------------------------------------------
# MONTHLY STATION TREND
# ---------------------------------------------------------

if selected_monthly.empty:
    st.warning("No monthly history is available for the selected station.")

else:
    station_fig = go.Figure()

    station_fig.add_trace(
        go.Scatter(
            x=selected_monthly["month"],
            y=selected_monthly["ridership"],
            mode="lines+markers",
            name="Monthly ridership",
            line=dict(color=RED, width=2.8),
            marker=dict(
                size=5,
                color=RED,
            ),
            fill="tozeroy",
            fillcolor="rgba(255,53,77,0.09)",
            hovertemplate=("%{x|%B %Y}<br>Ridership: %{y:,.0f}<extra></extra>"),
        )
    )

    station_fig.update_layout(
        title=f"Monthly ridership · {selected_station['station_complex']}",
        xaxis_title="Month",
        yaxis_title="Recorded ridership",
    )

    style_chart(station_fig, 400)

    st.plotly_chart(
        station_fig,
        use_container_width=True,
        config={
            "displayModeBar": "hover",
            "displaylogo": False,
        },
    )

    # ---------------------------------------------------------
    # MONTHLY TRANSFERS TREND
    # ---------------------------------------------------------

    transfers_fig = go.Figure()

    transfers_fig.add_trace(
        go.Scatter(
            x=selected_monthly["month"],
            y=selected_monthly["transfers"],
            mode="lines",
            name="Monthly transfers",
            line=dict(color=BLUE, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(123,167,255,0.09)",
            hovertemplate=("%{x|%B %Y}<br>Transfers: %{y:,.0f}<extra></extra>"),
        )
    )

    transfers_fig.update_layout(
        title="Monthly recorded transfers",
        xaxis_title="Month",
        yaxis_title="Recorded transfers",
    )

    style_chart(transfers_fig, 350)

    st.plotly_chart(
        transfers_fig,
        use_container_width=True,
        config={
            "displayModeBar": "hover",
            "displaylogo": False,
        },
    )


# ---------------------------------------------------------
# METHODOLOGY NOTES
# ---------------------------------------------------------

st.divider()

st.subheader("How to Interpret Station Results")

st.markdown(
    """
    - Station rankings are based on total monthly recorded ridership
      across January 2020 to December 2024.
    - Station ID, station complex, borough, and transit mode are retained
      together as the analytical identity of each station-mode record.
    - Transfers are reported separately and are not added to ridership.
    - A station's historical total does not indicate its current
      operating conditions.
    - Ridership is not a direct measurement of occupancy,
      overcrowding, or passenger capacity.
    """
)

with st.expander("Station analysis limitations"):
    st.markdown(
        """
        **Historical coverage:** The monthly dataset contains
        60 months from January 2020 through December 2024.

        **Station identifiers:** Some station identifiers may be
        shared across transit modes. This page preserves the
        complete station identity.

        **Station coordinates:** If coordinates are used in the
        geospatial page, they represent ridership-weighted reference
        positions rather than exact station entrances.

        **Data interpretation:** Recorded ridership and transfers
        do not provide direct information about train frequency,
        passenger occupancy, or overcrowding.
        """
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "ChronoTunnel · Station Analysis · MTA Subway Ridership 2020–2024 "
    "· Historical analysis, not a live operations feed."
)
