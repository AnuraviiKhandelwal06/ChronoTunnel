import pandas as pd
import plotly.graph_objects as go

from components.metrics import mode_label, short_station_name

# ============================================================
# ChronoTunnel — DARK CHART DESIGN SYSTEM
# ============================================================

FONT = "DM Sans, sans-serif"
HEADING_FONT = "Space Grotesk, sans-serif"

INK = "#F5F6FA"
MUTED = "#A7B0C2"
GRID = "rgba(255,255,255,0.09)"

RED = "#FF354D"
PINK = "#FF6B9A"
BLUE = "#7BA7FF"
PURPLE = "#A78BFA"
ORANGE = "#FFAD70"

ACCENT = RED

CHART_PALETTE = [RED, BLUE, PINK, PURPLE, ORANGE]

DASH_BOROUGH_COLORS = {
    "Manhattan": RED,
    "Brooklyn": BLUE,
    "Queens": PINK,
    "Bronx": PURPLE,
    "Staten Island": ORANGE,
}

DAY_COLORS = {
    "Wednesday": RED,
    "Saturday": BLUE,
}

DAY_ORDER = {
    "Wednesday": 0,
    "Saturday": 1,
}


# ============================================================
# SHARED INPUT VALIDATION
# ============================================================


def _validate_frame(
    frame: pd.DataFrame,
    required_columns: list[str],
    chart_name: str,
) -> pd.DataFrame:
    """Validate chart input and return a defensive copy."""

    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"{chart_name}: Expected a pandas DataFrame.")

    if frame.empty:
        raise ValueError(f"{chart_name}: Cannot generate a chart from empty data.")

    missing = [column for column in required_columns if column not in frame.columns]

    if missing:
        raise ValueError(
            f"{chart_name}: Missing required columns: {', '.join(missing)}"
        )

    return frame.copy()


def _numeric_frame(
    frame: pd.DataFrame,
    columns: list[str],
    chart_name: str,
    numeric_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Validate required columns and convert only explicitly specified
    numeric columns. Text and date columns remain unchanged.
    """

    data = _validate_frame(frame, columns, chart_name)

    numeric_columns = numeric_columns if numeric_columns is not None else columns

    invalid_columns = set(numeric_columns) - set(columns)

    if invalid_columns:
        raise ValueError(
            f"{chart_name}: Numeric columns must be included in required "
            f"columns: {', '.join(sorted(invalid_columns))}"
        )

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

        data[column] = data[column].replace(
            [float("inf"), float("-inf")],
            float("nan"),
        )

    data = data.dropna(subset=numeric_columns)

    if data.empty:
        raise ValueError(f"{chart_name}: No valid numeric observations are available.")

    return data


def _scale(max_value: float) -> tuple[float, str]:
    """Choose an appropriate display scale for ridership values."""

    if pd.isna(max_value):
        return 1, "rides"

    max_value = abs(float(max_value))

    if max_value >= 1_000_000_000:
        return 1_000_000_000, "billions"

    if max_value >= 1_000_000:
        return 1_000_000, "millions"

    if max_value >= 10_000:
        return 1_000, "thousands"

    return 1, "rides"


# ============================================================
# SHARED CHART STYLING
# ============================================================


def style(fig: go.Figure, height: int = 380) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=FONT,
            color=INK,
            size=13,
        ),
        title_font=dict(
            family=HEADING_FONT,
            color=INK,
        ),
        margin=dict(l=4, r=8, t=28, b=4),
        hoverlabel=dict(
            bgcolor="#191D28",
            bordercolor="#343B4D",
            font=dict(
                color=INK,
                family=FONT,
                size=12,
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            font=dict(
                size=12,
                color=MUTED,
                family=FONT,
            ),
        ),
        bargap=0.32,
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=GRID,
        tickfont=dict(color=MUTED, size=11, family=FONT),
        title_font=dict(color=MUTED, size=12, family=FONT),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
        tickfont=dict(color=MUTED, size=11, family=FONT),
        title_font=dict(color=MUTED, size=12, family=FONT),
    )

    return fig


# ============================================================
# HOME PAGE CHARTS
# ============================================================


def annual_ridership(yearly: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        yearly,
        ["year", "total_ridership"],
        "Annual ridership",
        numeric_columns=["year", "total_ridership"],
    )

    data["year"] = data["year"].astype(int)
    data = data.sort_values("year")

    divisor, unit = _scale(data["total_ridership"].abs().max())

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=data["total_ridership"] / divisor,
            mode="lines+markers",
            name="Ridership",
            line=dict(color=RED, width=3),
            marker=dict(
                size=9,
                color=RED,
                line=dict(color="#08090D", width=2),
            ),
            fill="tozeroy",
            fillcolor="rgba(255,53,77,0.12)",
            customdata=data["total_ridership"],
            hovertemplate=("Year %{x}<br>Ridership %{customdata:,.0f}<extra></extra>"),
        )
    )

    style(fig, 360)

    fig.update_xaxes(dtick=1, title="Year")
    fig.update_yaxes(title=f"Ridership ({unit})")

    return fig


def borough_share(borough: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        borough,
        ["borough", "total_ridership"],
        "Borough share",
        numeric_columns=["total_ridership"],
    )

    data = data.sort_values("total_ridership", ascending=False)

    fig = go.Figure(
        go.Pie(
            labels=data["borough"],
            values=data["total_ridership"],
            hole=0.64,
            sort=False,
            marker=dict(
                colors=[DASH_BOROUGH_COLORS.get(name, RED) for name in data["borough"]],
                line=dict(color="#08090D", width=3),
            ),
            textinfo="none",
            hovertemplate=(
                "%{label}<br>Ridership %{value:,.0f}<br>Share %{percent}<extra></extra>"
            ),
        )
    )

    style(fig, 360)

    fig.update_layout(
        showlegend=True,
        margin=dict(l=4, r=4, t=28, b=4),
    )

    return fig


def mode_distribution(modes: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        modes,
        ["transit_mode", "total_ridership"],
        "Mode distribution",
        numeric_columns=["total_ridership"],
    )

    data["label"] = data["transit_mode"].map(mode_label)

    data = data.sort_values("total_ridership", ascending=True)

    divisor, unit = _scale(data["total_ridership"].abs().max())

    fig = go.Figure(
        go.Bar(
            x=data["total_ridership"] / divisor,
            y=data["label"],
            orientation="h",
            marker=dict(
                color=[
                    CHART_PALETTE[index % len(CHART_PALETTE)]
                    for index in range(len(data))
                ],
                line=dict(color="#08090D", width=1),
            ),
            customdata=data["total_ridership"],
            hovertemplate=("%{y}<br>Ridership %{customdata:,.0f}<extra></extra>"),
        )
    )

    style(fig, 360)

    fig.update_yaxes(title="", showgrid=False)
    fig.update_xaxes(
        title=f"Ridership ({unit})",
        showgrid=True,
        gridcolor=GRID,
    )

    return fig


def top_stations(
    stations: pd.DataFrame,
    limit: int = 15,
) -> go.Figure:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("Top stations: limit must be a positive integer.")

    data = _numeric_frame(
        stations,
        ["total_ridership", "station_complex", "borough"],
        "Top stations",
        numeric_columns=["total_ridership"],
    )

    data = data.sort_values(
        "total_ridership",
        ascending=False,
    ).head(limit)

    data = data.sort_values("total_ridership", ascending=True)

    data["short_name"] = data["station_complex"].map(short_station_name)

    divisor, unit = _scale(data["total_ridership"].abs().max())

    custom = list(
        zip(
            data["total_ridership"],
            data["borough"],
            data["station_complex"],
            strict=False,
        )
    )

    fig = go.Figure(
        go.Bar(
            x=data["total_ridership"] / divisor,
            y=data["short_name"],
            orientation="h",
            marker=dict(
                color=[DASH_BOROUGH_COLORS.get(name, RED) for name in data["borough"]]
            ),
            customdata=custom,
            hovertemplate=(
                "%{customdata[2]}"
                "<br>Borough %{customdata[1]}"
                "<br>Ridership %{customdata[0]:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    style(fig, 280 + limit * 26)

    fig.update_yaxes(title="", showgrid=False, automargin=True)
    fig.update_xaxes(
        title=f"Ridership ({unit})",
        showgrid=True,
        gridcolor=GRID,
    )

    return fig


# ============================================================
# TEMPORAL ANALYSIS CHARTS
# ============================================================


def monthly_timeline(monthly: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        monthly,
        ["month", "total_ridership"],
        "Monthly timeline",
        numeric_columns=["total_ridership"],
    )

    data["month"] = pd.to_datetime(data["month"], errors="coerce")
    data = data.dropna(subset=["month"]).sort_values("month")

    if data.empty:
        raise ValueError("Monthly timeline: No valid dates are available.")

    divisor, unit = _scale(data["total_ridership"].abs().max())

    fig = go.Figure(
        go.Scatter(
            x=data["month"],
            y=data["total_ridership"] / divisor,
            mode="lines",
            line=dict(color=RED, width=2.8),
            fill="tozeroy",
            fillcolor="rgba(255,53,77,0.09)",
            customdata=data["total_ridership"],
            hovertemplate=("%{x|%b %Y}<br>Ridership %{customdata:,.0f}<extra></extra>"),
        )
    )

    style(fig, 360)

    fig.update_xaxes(title="Month")
    fig.update_yaxes(title=f"Ridership ({unit})")

    return fig


def month_of_year(
    frame: pd.DataFrame,
    value_columns: list[tuple[str, str]],
) -> go.Figure:
    if not value_columns:
        raise ValueError("Month of year: At least one value column is required.")

    required = ["month_name"] + [column for column, _ in value_columns]

    data = _validate_frame(frame, required, "Month of year")

    fig = go.Figure()

    for index, (column, name) in enumerate(value_columns):
        values = pd.to_numeric(data[column], errors="coerce")

        fig.add_trace(
            go.Bar(
                x=data["month_name"],
                y=values / 1_000_000,
                name=name,
                marker_color=CHART_PALETTE[index % len(CHART_PALETTE)],
                hovertemplate=(
                    "%{x}<br>" + name + " %{y:.2f} million" + "<extra></extra>"
                ),
            )
        )

    style(fig, 380)

    fig.update_layout(barmode="group")
    fig.update_yaxes(title="Average ridership (millions)")
    fig.update_xaxes(title="")

    return fig


def hourly_comparison(hourly: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        hourly,
        ["hour", "average_ridership", "day_name"],
        "Hourly comparison",
        numeric_columns=["hour", "average_ridership"],
    )

    data["hour"] = data["hour"].astype(int)
    data = data[data["hour"].between(0, 23)]

    if data.empty:
        raise ValueError("Hourly comparison: No valid hourly observations.")

    fig = go.Figure()

    for day_name in sorted(
        data["day_name"].dropna().unique(),
        key=lambda name: DAY_ORDER.get(str(name), 99),
    ):
        group = data[data["day_name"] == day_name].sort_values("hour")

        fig.add_trace(
            go.Scatter(
                x=group["hour"],
                y=group["average_ridership"],
                mode="lines+markers",
                name=str(day_name),
                line=dict(
                    color=DAY_COLORS.get(str(day_name), PINK),
                    width=2.8,
                ),
                marker=dict(size=6),
                hovertemplate=(
                    str(day_name) + " %{x}:00<br>Average rides %{y:,.0f}<extra></extra>"
                ),
            )
        )

    style(fig, 400)

    fig.update_xaxes(title="Hour of the sampled day", dtick=2)
    fig.update_yaxes(title="Average recorded rides")

    return fig


def peak_share(peak: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        peak,
        [
            "day_name",
            "average_daily_peak_share_percent",
            "average_daily_ridership",
            "average_peak_period_ridership",
            "sampled_dates",
        ],
        "Peak share",
        numeric_columns=[
            "average_daily_peak_share_percent",
            "average_daily_ridership",
            "average_peak_period_ridership",
            "sampled_dates",
        ],
    )

    data = data.sort_values(
        "day_name",
        key=lambda values: values.map(lambda name: DAY_ORDER.get(str(name), 99)),
    )

    fig = go.Figure(
        go.Bar(
            x=data["day_name"],
            y=data["average_daily_peak_share_percent"],
            marker_color=[DAY_COLORS.get(str(name), PINK) for name in data["day_name"]],
            customdata=list(
                zip(
                    data["average_daily_ridership"],
                    data["average_peak_period_ridership"],
                    data["sampled_dates"],
                    strict=False,
                )
            ),
            hovertemplate=(
                "%{x}"
                "<br>Average daily peak share %{y:.2f}%"
                "<br>Average daily ridership %{customdata[0]:,.0f}"
                "<br>Average peak-window ridership %{customdata[1]:,.0f}"
                "<br>Sampled dates %{customdata[2]:.0f}"
                "<extra></extra>"
            ),
        )
    )

    style(fig, 340)

    fig.update_yaxes(
        title="Average daily peak share (%)",
        range=[0, 100],
    )

    fig.update_xaxes(title="")

    return fig


def yoy_change(growth: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        growth,
        ["month", "yoy_growth_percent"],
        "Year-over-year change",
        numeric_columns=["yoy_growth_percent"],
    )

    data["month"] = pd.to_datetime(data["month"], errors="coerce")
    data = data.dropna(subset=["month"]).sort_values("month")

    if data.empty:
        raise ValueError("Year-over-year change: No valid dates are available.")

    values = data["yoy_growth_percent"]
    colors = [RED if value >= 0 else BLUE for value in values]

    fig = go.Figure(
        go.Bar(
            x=data["month"],
            y=values,
            marker_color=colors,
            hovertemplate=("%{x|%b %Y}<br>Year-over-year %{y:.2f}%<extra></extra>"),
        )
    )

    style(fig, 360)

    fig.update_yaxes(title="Year-over-year change (%)")
    fig.update_xaxes(title="")

    return fig


# ============================================================
# BOROUGH ANALYSIS CHARTS
# ============================================================


def borough_bars(
    frame: pd.DataFrame,
    value_column: str,
    unit_title: str,
    hover_precision: str = ",.0f",
) -> go.Figure:
    data = _numeric_frame(
        frame,
        ["borough", value_column],
        "Borough comparison",
        numeric_columns=[value_column],
    )

    data = data.sort_values(value_column, ascending=True)

    maximum = float(data[value_column].abs().max())

    if "percent" in value_column.lower():
        plotted = data[value_column]
        axis = unit_title
    else:
        divisor, unit = _scale(maximum)
        plotted = data[value_column] / divisor
        axis = f"{unit_title} ({unit})"

    fig = go.Figure(
        go.Bar(
            x=plotted,
            y=data["borough"],
            orientation="h",
            marker_color=[
                DASH_BOROUGH_COLORS.get(name, RED) for name in data["borough"]
            ],
            customdata=data[value_column],
            hovertemplate=(
                "%{y}<br>"
                + unit_title
                + " %{customdata:"
                + hover_precision
                + "}"
                + "<extra></extra>"
            ),
        )
    )

    style(fig, 340)

    fig.update_yaxes(title="", showgrid=False, automargin=True)
    fig.update_xaxes(
        title=axis,
        showgrid=True,
        gridcolor=GRID,
    )

    return fig


# ============================================================
# STATION ANALYSIS CHARTS
# ============================================================


def station_compare(stations: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        stations,
        ["total_ridership", "label", "borough"],
        "Station comparison",
        numeric_columns=["total_ridership"],
    )

    data = data.sort_values("total_ridership", ascending=True)

    divisor, unit = _scale(data["total_ridership"].abs().max())

    fig = go.Figure(
        go.Bar(
            x=data["total_ridership"] / divisor,
            y=data["label"],
            orientation="h",
            marker_color=[
                DASH_BOROUGH_COLORS.get(name, RED) for name in data["borough"]
            ],
            customdata=data["total_ridership"],
            hovertemplate=("%{y}<br>Ridership %{customdata:,.0f}<extra></extra>"),
        )
    )

    style(fig, max(280, 70 + 36 * len(data)))

    fig.update_yaxes(title="", showgrid=False, automargin=True)
    fig.update_xaxes(
        title=f"Ridership ({unit})",
        showgrid=True,
        gridcolor=GRID,
    )

    return fig


def station_month_series(monthly: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        monthly,
        ["month", "ridership"],
        "Station monthly series",
        numeric_columns=["ridership"],
    )

    data["month"] = pd.to_datetime(data["month"], errors="coerce")
    data = data.dropna(subset=["month"]).sort_values("month")

    if data.empty:
        raise ValueError("Station monthly series: No valid monthly observations.")

    divisor, unit = _scale(data["ridership"].abs().max())

    fig = go.Figure(
        go.Scatter(
            x=data["month"],
            y=data["ridership"] / divisor,
            mode="lines",
            line=dict(color=RED, width=2.8),
            fill="tozeroy",
            fillcolor="rgba(255,53,77,0.09)",
            customdata=data["ridership"],
            hovertemplate=("%{x|%b %Y}<br>Ridership %{customdata:,.0f}<extra></extra>"),
        )
    )

    style(fig, 340)

    fig.update_yaxes(title=f"Ridership ({unit})")
    fig.update_xaxes(title="")

    return fig


# ============================================================
# GEOSPATIAL SUPPORT CHART
# ============================================================


def centroid_scatter(centroids: pd.DataFrame) -> go.Figure:
    data = _numeric_frame(
        centroids,
        [
            "weighted_longitude",
            "weighted_latitude",
            "total_ridership",
            "borough",
        ],
        "Centroid scatter",
        numeric_columns=[
            "weighted_longitude",
            "weighted_latitude",
            "total_ridership",
        ],
    )

    maximum = float(data["total_ridership"].abs().max())

    if maximum > 0:
        normalized = data["total_ridership"].clip(lower=0) / maximum
    else:
        normalized = pd.Series(0.0, index=data.index)

    marker_sizes = 18 + 28 * normalized

    fig = go.Figure(
        go.Scatter(
            x=data["weighted_longitude"],
            y=data["weighted_latitude"],
            mode="markers+text",
            text=data["borough"],
            textposition="top center",
            marker=dict(
                size=marker_sizes,
                color=[DASH_BOROUGH_COLORS.get(name, RED) for name in data["borough"]],
                line=dict(color="#08090D", width=1),
            ),
            customdata=data["total_ridership"],
            hovertemplate=(
                "%{text}"
                "<br>Weighted latitude %{y:.5f}"
                "<br>Weighted longitude %{x:.5f}"
                "<br>Ridership %{customdata:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    style(fig, 460)

    fig.update_xaxes(
        title="Weighted longitude",
        showgrid=True,
        gridcolor=GRID,
    )

    fig.update_yaxes(
        title="Weighted latitude",
        scaleanchor="x",
        scaleratio=1.15,
    )

    return fig


# ============================================================
# STREAMLIT CHART CONFIGURATION
# ============================================================

CHART_CONFIG = {
    "displayModeBar": "hover",
    "displaylogo": False,
}
