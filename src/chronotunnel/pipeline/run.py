import json

from src.chronotunnel.analysis.eda import (
    get_borough_ridership,
    get_monthly_ridership_trend,
    get_top_stations,
    get_transit_mode_ridership,
    get_yearly_ridership,
)
from src.chronotunnel.analysis.geospatial import (
    get_borough_geospatial_summary,
    get_borough_weighted_centroids,
    get_coordinate_quality_summary,
    get_top_ridership_locations,
)
from src.chronotunnel.analysis.statistical import (
    compare_paired_weekday_weekend_ridership,
    get_borough_statistics,
    get_ridership_distribution,
    get_transit_mode_statistics,
)
from src.chronotunnel.analysis.temporal import (
    get_monthly_seasonality,
    get_peak_hour_concentration,
    get_weekday_weekend_comparison,
    get_year_over_year_growth,
)
from src.chronotunnel.config.settings import (
    FIGURES_DIR,
    MAPS_DIR,
    METRICS_DIR,
)
from src.chronotunnel.data.load import create_connection
from src.chronotunnel.data.validate import run_data_validation
from src.chronotunnel.visualization.charts import (
    create_borough_ridership_chart,
    create_hourly_ridership_chart,
    create_monthly_ridership_chart,
    create_top_stations_chart,
)
from src.chronotunnel.visualization.maps import (
    create_ridership_heatmap,
    create_station_ridership_map,
)


def run_pipeline():
    """Execute the complete ChronoTunnel analytical workflow."""

    for directory in [FIGURES_DIR, MAPS_DIR, METRICS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    connection = create_connection()

    try:
        print("\n" + "=" * 60)
        print("CHRONOTUNNEL - URBAN MOBILITY INTELLIGENCE PLATFORM")
        print("=" * 60)

        # 1. Data validation
        print("\n[1/6] Running data validation...")

        validation = run_data_validation(connection)
        validation.to_csv(
            METRICS_DIR / "data_validation.csv",
            index=False,
        )

        print(validation.to_string(index=False))

        if (
            validation.astype(str)
            .apply(lambda column: column.str.upper().eq("FAIL"))
            .any()
            .any()
        ):
            raise RuntimeError("Data validation failed. Pipeline stopped.")

        print("Data validation completed.")

        # 2. Exploratory data analysis
        print("\n[2/6] Running exploratory data analysis...")

        eda_results = {
            "yearly_ridership": get_yearly_ridership(connection),
            "monthly_ridership": get_monthly_ridership_trend(connection),
            "borough_ridership": get_borough_ridership(connection),
            "transit_mode_ridership": get_transit_mode_ridership(connection),
            "top_stations": get_top_stations(connection, limit=15),
        }

        # 3. Temporal analysis
        print("\n[3/6] Running temporal analysis...")

        temporal_results = {
            "year_over_year_growth": get_year_over_year_growth(connection),
            "monthly_seasonality": get_monthly_seasonality(connection),
            "weekday_weekend_comparison": get_weekday_weekend_comparison(connection),
            "peak_hour_concentration": get_peak_hour_concentration(connection),
        }

        # 4. Statistical analysis
        print("\n[4/6] Running statistical analysis...")

        statistical_results = {
            "ridership_distribution": get_ridership_distribution(connection),
            "borough_statistics": get_borough_statistics(connection),
            "transit_mode_statistics": get_transit_mode_statistics(connection),
        }

        paired_comparison = compare_paired_weekday_weekend_ridership(connection)

        # 5. Geospatial analysis
        print("\n[5/6] Running geospatial analysis...")

        geospatial_results = {
            "borough_summary": get_borough_geospatial_summary(connection),
            "top_locations": get_top_ridership_locations(connection, 15),
            "weighted_centroids": get_borough_weighted_centroids(connection),
            "coordinate_quality": get_coordinate_quality_summary(connection),
        }

        # Save all tabular results
        all_results = {
            **eda_results,
            **temporal_results,
            **statistical_results,
            **geospatial_results,
        }

        for name, result in all_results.items():
            result.to_csv(
                METRICS_DIR / f"{name}.csv",
                index=False,
            )

        # Save paired statistical comparison
        with open(
            METRICS_DIR / "paired_weekday_weekend_comparison.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(paired_comparison, file, indent=4)

        # 6. Generate visualizations
        print("\n[6/6] Generating visualizations...")

        station_coordinates = connection.execute(
            "SELECT * FROM station_coordinates"
        ).df()

        create_station_ridership_map(
            station_coordinates,
            str(MAPS_DIR / "station_ridership_map.html"),
        )

        create_ridership_heatmap(
            station_coordinates,
            str(MAPS_DIR / "ridership_heatmap.html"),
        )

        create_borough_ridership_chart(
            eda_results["borough_ridership"],
            str(FIGURES_DIR / "borough_ridership.html"),
        )

        create_top_stations_chart(
            eda_results["top_stations"],
            str(FIGURES_DIR / "top_15_stations.html"),
        )

        create_hourly_ridership_chart(
            temporal_results["weekday_weekend_comparison"],
            str(FIGURES_DIR / "hourly_ridership_comparison.html"),
        )

        create_monthly_ridership_chart(
            eda_results["monthly_ridership"],
            str(FIGURES_DIR / "monthly_ridership_trend.html"),
        )

        print("\n" + "=" * 60)
        print("CHRONOTUNNEL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print(f"\nMetrics saved to: {METRICS_DIR}")
        print(f"Charts saved to:  {FIGURES_DIR}")
        print(f"Maps saved to:    {MAPS_DIR}")

        print("\nPaired Wednesday-Saturday comparison:")
        print(json.dumps(paired_comparison, indent=4))

    finally:
        connection.close()


if __name__ == "__main__":
    run_pipeline()
