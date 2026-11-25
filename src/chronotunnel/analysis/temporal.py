import duckdb
import pandas as pd


def get_year_over_year_growth(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate monthly ridership change compared with the same month last year."""

    query = """
        WITH monthly_totals AS (
            SELECT
                CAST(month AS DATE) AS month,
                SUM(ridership) AS total_ridership
            FROM monthly
            GROUP BY month
        )
        SELECT
            month,
            total_ridership,
            LAG(total_ridership, 12) OVER (ORDER BY month)
                AS previous_year_ridership,
            ROUND(
                100.0 * (
                    total_ridership -
                    LAG(total_ridership, 12) OVER (ORDER BY month)
                ) / NULLIF(
                    LAG(total_ridership, 12) OVER (ORDER BY month), 0
                ),
                2
            ) AS yoy_growth_percent
        FROM monthly_totals
        ORDER BY month
    """

    return connection.execute(query).df()


def get_monthly_seasonality(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Compare monthly seasonality across all years and excluding 2020."""

    query = """
        WITH monthly_totals AS (
            SELECT
                month,
                EXTRACT(MONTH FROM month)::INTEGER AS month_number,
                STRFTIME(month, '%B') AS month_name,
                EXTRACT(YEAR FROM month)::INTEGER AS year,
                SUM(ridership) AS monthly_ridership
            FROM monthly
            GROUP BY month
        )
        SELECT
            month_number,
            month_name,

            ROUND(AVG(monthly_ridership), 2)
                AS average_ridership_2020_2024,

            ROUND(
                AVG(
                    CASE WHEN year >= 2021
                    THEN monthly_ridership END
                ), 2
            ) AS average_ridership_2021_2024,

            MIN(monthly_ridership) AS minimum_ridership,
            MAX(monthly_ridership) AS maximum_ridership,
            COUNT(*) AS years_observed,
            COUNT(CASE WHEN year >= 2021 THEN 1 END)
                AS years_excluding_2020

        FROM monthly_totals
        GROUP BY month_number, month_name
        ORDER BY month_number
    """

    return connection.execute(query).df()


def get_weekday_weekend_comparison(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Compare average hourly ridership on sampled Wednesdays and Saturdays."""

    query = """
        WITH hourly_totals AS (
            SELECT
                CAST(transit_timestamp AS DATE) AS sample_date,
                EXTRACT(DOW FROM transit_timestamp)::INTEGER AS day_of_week,
                STRFTIME(transit_timestamp, '%A') AS day_name,
                EXTRACT(HOUR FROM transit_timestamp)::INTEGER AS hour,
                SUM(ridership) AS total_ridership
            FROM hourly
            GROUP BY sample_date, day_of_week, day_name, hour
        )
        SELECT
            day_of_week,
            day_name,
            hour,
            ROUND(AVG(total_ridership), 2) AS average_ridership,
            COUNT(DISTINCT sample_date) AS sampled_dates
        FROM hourly_totals
        WHERE day_of_week IN (3, 6)
        GROUP BY day_of_week, day_name, hour
        ORDER BY day_of_week, hour
    """

    return connection.execute(query).df()


def get_peak_hour_concentration(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate the share of sampled daily ridership occurring in peak periods."""

    query = """
        WITH daily_hourly AS (
            SELECT
                CAST(transit_timestamp AS DATE) AS sample_date,
                EXTRACT(DOW FROM transit_timestamp)::INTEGER AS day_of_week,
                EXTRACT(HOUR FROM transit_timestamp)::INTEGER AS hour,
                SUM(ridership) AS hourly_ridership
            FROM hourly
            GROUP BY sample_date, day_of_week, hour
        ),
        daily_totals AS (
            SELECT
                sample_date,
                day_of_week,
                SUM(hourly_ridership) AS daily_ridership,
                SUM(
                    CASE
                        WHEN hour BETWEEN 7 AND 9
                          OR hour BETWEEN 16 AND 18
                        THEN hourly_ridership
                        ELSE 0
                    END
                ) AS peak_period_ridership
            FROM daily_hourly
            GROUP BY sample_date, day_of_week
        )
        SELECT
            day_of_week,
            CASE
                WHEN day_of_week = 3 THEN 'Wednesday'
                WHEN day_of_week = 6 THEN 'Saturday'
            END AS day_name,
            COUNT(*) AS sampled_dates,
            ROUND(AVG(daily_ridership), 2)
                AS average_daily_ridership,
            ROUND(AVG(peak_period_ridership), 2)
                AS average_peak_period_ridership,
            ROUND(
                100.0 * SUM(peak_period_ridership) /
                NULLIF(SUM(daily_ridership), 0),
                2
            ) AS ridership_weighted_peak_share_percent,
            ROUND(
                AVG(
                    100.0 * peak_period_ridership /
                    NULLIF(daily_ridership, 0)
                ),
                2
            ) AS average_daily_peak_share_percent
        FROM daily_totals
        WHERE day_of_week IN (3, 6)
        GROUP BY day_of_week
        ORDER BY day_of_week
    """

    return connection.execute(query).df()
