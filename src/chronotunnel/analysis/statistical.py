import duckdb
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, t, wilcoxon


def get_ridership_distribution(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Calculate descriptive statistics for monthly station-level ridership."""

    query = """
        SELECT
            COUNT(*) AS observations,
            ROUND(AVG(ridership), 2) AS mean_ridership,
            MEDIAN(ridership) AS median_ridership,
            ROUND(STDDEV_SAMP(ridership), 2) AS standard_deviation,
            MIN(ridership) AS minimum_ridership,
            QUANTILE_CONT(ridership, 0.25) AS first_quartile,
            QUANTILE_CONT(ridership, 0.75) AS third_quartile,
            MAX(ridership) AS maximum_ridership,
            ROUND(SKEWNESS(ridership), 4) AS skewness
        FROM monthly
    """

    return connection.execute(query).df()


def get_borough_statistics(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Compare monthly station-level ridership distributions by borough."""

    query = """
        SELECT
            borough,
            COUNT(*) AS observations,
            COUNT(DISTINCT station_complex_id) AS unique_stations,
            ROUND(AVG(ridership), 2) AS average_ridership,
            MEDIAN(ridership) AS median_ridership,
            ROUND(STDDEV_SAMP(ridership), 2) AS standard_deviation,
            MIN(ridership) AS minimum_ridership,
            MAX(ridership) AS maximum_ridership
        FROM monthly
        GROUP BY borough
        ORDER BY average_ridership DESC
    """

    return connection.execute(query).df()


def get_transit_mode_statistics(
    connection: duckdb.DuckDBPyConnection,
) -> pd.DataFrame:
    """Compare monthly station-level ridership distributions by transit mode."""

    query = """
        SELECT
            transit_mode,
            COUNT(*) AS observations,
            COUNT(DISTINCT station_complex_id) AS unique_stations,
            ROUND(AVG(ridership), 2) AS average_ridership,
            MEDIAN(ridership) AS median_ridership,
            ROUND(STDDEV_SAMP(ridership), 2) AS standard_deviation,
            MIN(ridership) AS minimum_ridership,
            MAX(ridership) AS maximum_ridership
        FROM monthly
        GROUP BY transit_mode
        ORDER BY average_ridership DESC
    """

    return connection.execute(query).df()


def compare_weekday_weekend_ridership(
    connection: duckdb.DuckDBPyConnection,
) -> dict:
    """Compare sampled Wednesday and Saturday daily ridership using Mann-Whitney U."""

    query = """
        SELECT
            CAST(transit_timestamp AS DATE) AS sample_date,
            EXTRACT(DOW FROM transit_timestamp)::INTEGER AS day_of_week,
            SUM(ridership) AS daily_ridership
        FROM hourly
        WHERE EXTRACT(DOW FROM transit_timestamp)::INTEGER IN (3, 6)
        GROUP BY sample_date, day_of_week
        ORDER BY sample_date
    """

    daily_data = connection.execute(query).df()

    if daily_data.empty:
        raise ValueError("No Wednesday or Saturday observations are available.")

    wednesday = daily_data.loc[
        daily_data["day_of_week"] == 3,
        "daily_ridership",
    ].to_numpy(dtype=float)

    saturday = daily_data.loc[
        daily_data["day_of_week"] == 6,
        "daily_ridership",
    ].to_numpy(dtype=float)

    if len(wednesday) < 2 or len(saturday) < 2:
        raise ValueError(
            "At least two Wednesday and two Saturday observations "
            "are required for the independent-sample comparison."
        )

    if not np.isfinite(wednesday).all() or not np.isfinite(saturday).all():
        raise ValueError("Daily ridership contains non-finite values.")

    if (wednesday < 0).any() or (saturday < 0).any():
        raise ValueError("Daily ridership cannot contain negative values.")

    result = mannwhitneyu(
        wednesday,
        saturday,
        alternative="two-sided",
    )

    return {
        "wednesday_sample_size": len(wednesday),
        "saturday_sample_size": len(saturday),
        "wednesday_mean_ridership": round(float(wednesday.mean()), 2),
        "saturday_mean_ridership": round(float(saturday.mean()), 2),
        "wednesday_median_ridership": round(float(np.median(wednesday)), 2),
        "saturday_median_ridership": round(float(np.median(saturday)), 2),
        "mann_whitney_u_statistic": round(float(result.statistic), 2),
        "p_value": float(result.pvalue),
        "significance_level": 0.05,
        "statistically_significant": bool(result.pvalue < 0.05),
    }


def compare_paired_weekday_weekend_ridership(
    connection: duckdb.DuckDBPyConnection,
) -> dict:
    """
    Compare Wednesday and Saturday ridership using one matched pair per month.

    Each month must contain exactly one sampled Wednesday and one sampled
    Saturday. Ambiguous monthly pairs are rejected rather than silently
    selecting one observation.
    """

    query = """
        WITH daily_totals AS (
            SELECT
                DATE_TRUNC(
                    'month', CAST(transit_timestamp AS DATE)
                ) AS sample_month,
                EXTRACT(DOW FROM transit_timestamp)::INTEGER AS day_of_week,
                CAST(transit_timestamp AS DATE) AS sample_date,
                SUM(ridership) AS daily_ridership
            FROM hourly
            WHERE EXTRACT(DOW FROM transit_timestamp)::INTEGER IN (3, 6)
            GROUP BY sample_month, day_of_week, sample_date
        ),
        monthly_counts AS (
            SELECT
                sample_month,
                COUNT(
                    DISTINCT CASE
                        WHEN day_of_week = 3 THEN sample_date
                    END
                ) AS wednesday_dates,
                COUNT(
                    DISTINCT CASE
                        WHEN day_of_week = 6 THEN sample_date
                    END
                ) AS saturday_dates
            FROM daily_totals
            GROUP BY sample_month
        )
        SELECT
            d.sample_month,
            MAX(
                CASE WHEN d.day_of_week = 3
                THEN d.daily_ridership END
            ) AS wednesday_ridership,
            MAX(
                CASE WHEN d.day_of_week = 6
                THEN d.daily_ridership END
            ) AS saturday_ridership,
            c.wednesday_dates,
            c.saturday_dates
        FROM daily_totals AS d
        INNER JOIN monthly_counts AS c
            ON d.sample_month = c.sample_month
        GROUP BY
            d.sample_month,
            c.wednesday_dates,
            c.saturday_dates
        ORDER BY d.sample_month
    """

    monthly_data = connection.execute(query).df()

    if monthly_data.empty:
        raise ValueError("No matched weekday-weekend observations are available.")

    invalid_months = monthly_data.loc[
        (monthly_data["wednesday_dates"] != 1) | (monthly_data["saturday_dates"] != 1),
        "sample_month",
    ]

    if not invalid_months.empty:
        invalid_labels = [
            pd.Timestamp(month).strftime("%Y-%m") for month in invalid_months
        ]

        raise ValueError(
            "Each included month must contain exactly one sampled "
            "Wednesday and one sampled Saturday. Invalid months: "
            f"{', '.join(invalid_labels)}."
        )

    wednesday = monthly_data["wednesday_ridership"].to_numpy(dtype=float)
    saturday = monthly_data["saturday_ridership"].to_numpy(dtype=float)

    if len(wednesday) < 2:
        raise ValueError("At least two matched monthly observations are required.")

    if not np.isfinite(wednesday).all() or not np.isfinite(saturday).all():
        raise ValueError("Paired daily ridership contains non-finite values.")

    if (wednesday < 0).any() or (saturday < 0).any():
        raise ValueError("Paired daily ridership cannot contain negative values.")

    differences = wednesday - saturday
    n = len(differences)

    mean_difference = float(np.mean(differences))
    median_difference = float(np.median(differences))
    std_difference = float(np.std(differences, ddof=1))

    standard_error = std_difference / np.sqrt(n)
    critical_value = float(t.ppf(0.975, df=n - 1))

    ci_lower = mean_difference - critical_value * standard_error
    ci_upper = mean_difference + critical_value * standard_error

    nonzero = differences[differences != 0]

    if len(nonzero) == 0:
        # All paired differences are zero: there is no evidence of a
        # systematic directional difference.
        wilcoxon_statistic = 0.0
        p_value = 1.0
        rank_biserial = 0.0

    else:
        test_result = wilcoxon(
            differences,
            alternative="two-sided",
            zero_method="wilcox",
            method="auto",
        )

        wilcoxon_statistic = float(test_result.statistic)
        p_value = float(test_result.pvalue)

        ranks = pd.Series(np.abs(nonzero)).rank(method="average").to_numpy()

        positive_rank_sum = float(ranks[nonzero > 0].sum())
        negative_rank_sum = float(ranks[nonzero < 0].sum())
        total_rank_sum = positive_rank_sum + negative_rank_sum

        rank_biserial = (
            (positive_rank_sum - negative_rank_sum) / total_rank_sum
            if total_rank_sum > 0
            else 0.0
        )

    if not np.isfinite(
        [mean_difference, median_difference, ci_lower, ci_upper, p_value]
    ).all():
        raise ValueError("Statistical calculations produced non-finite results.")

    return {
        "paired_months": n,
        "wednesday_mean_ridership": round(float(wednesday.mean()), 2),
        "saturday_mean_ridership": round(float(saturday.mean()), 2),
        "mean_paired_difference": round(mean_difference, 2),
        "median_paired_difference": round(median_difference, 2),
        "mean_difference_ci_95_lower": round(float(ci_lower), 2),
        "mean_difference_ci_95_upper": round(float(ci_upper), 2),
        "wilcoxon_statistic": round(wilcoxon_statistic, 2),
        "p_value": p_value,
        "rank_biserial_correlation": round(float(rank_biserial), 4),
        "statistically_significant": bool(p_value < 0.05),
    }
