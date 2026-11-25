import pandas as pd
import plotly.express as px


def create_borough_ridership_chart(
    borough_data: pd.DataFrame,
    output_path: str,
) -> None:
    """Create a borough-wise ridership comparison chart."""

    fig = px.bar(
        borough_data,
        x="borough",
        y="total_ridership",
        color="borough",
        title="Total Subway Ridership by Borough (2020–2024)",
        labels={
            "borough": "Borough",
            "total_ridership": "Total Ridership",
        },
        text_auto=".3s",
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        yaxis_title="Total Ridership",
        xaxis_title="Borough",
    )

    fig.write_html(
        output_path,
        include_plotlyjs="directory",
    )


def create_top_stations_chart(
    station_data: pd.DataFrame,
    output_path: str,
) -> None:
    """Create a horizontal chart of the highest-ridership stations."""

    data = station_data.sort_values(
        "total_ridership",
        ascending=True,
    )

    fig = px.bar(
        data,
        x="total_ridership",
        y="station_complex",
        color="borough",
        orientation="h",
        title="Top Stations by Total Ridership (2020–2024)",
        labels={
            "station_complex": "Station Complex",
            "total_ridership": "Total Ridership",
            "borough": "Borough",
        },
        text_auto=".3s",
    )

    fig.update_layout(
        template="plotly_white",
        height=max(550, len(data) * 35),
        yaxis_title="",
        xaxis_title="Total Ridership",
    )

    fig.write_html(
        output_path,
        include_plotlyjs="directory",
    )


def create_hourly_ridership_chart(
    hourly_data: pd.DataFrame,
    output_path: str,
) -> None:
    """Compare average hourly ridership on sampled Wednesdays and Saturdays."""

    fig = px.line(
        hourly_data,
        x="hour",
        y="average_ridership",
        color="day_name",
        markers=True,
        title="Average Hourly Ridership: Wednesday vs Saturday",
        labels={
            "hour": "Hour of Day",
            "average_ridership": "Average Ridership",
            "day_name": "Day",
        },
    )

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(
            tickmode="linear",
            dtick=1,
        ),
        yaxis_title="Average Ridership",
        xaxis_title="Hour of Day",
    )

    fig.write_html(
        output_path,
        include_plotlyjs="directory",
    )


def create_monthly_ridership_chart(
    monthly_data: pd.DataFrame,
    output_path: str,
) -> None:
    """Visualize monthly ridership over the five-year study period."""

    data = monthly_data.copy()
    data["month"] = pd.to_datetime(data["month"])

    fig = px.line(
        data,
        x="month",
        y="total_ridership",
        markers=True,
        title="Monthly Subway Ridership (2020–2024)",
        labels={
            "month": "Month",
            "total_ridership": "Total Ridership",
        },
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Total Ridership",
        xaxis_title="Month",
    )

    fig.write_html(
        output_path,
        include_plotlyjs="directory",
    )
