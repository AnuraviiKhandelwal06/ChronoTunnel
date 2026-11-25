import duckdb
import numpy as np
import pandas as pd
from src.chronotunnel.analysis.statistical import (
    compare_paired_weekday_weekend_ridership,
    get_borough_statistics,
    get_ridership_distribution,
    get_transit_mode_statistics,
)


def _format_number(value: float) -> str:
    """Format a finite numeric value with readable thousands separators."""

    number = float(value)

    if not np.isfinite(number):
        raise ValueError("Cannot format a non-finite numeric value.")

    return f"{number:,.0f}"


def _format_p_value(value: float) -> str:
    """Format a valid p-value without displaying it as zero."""

    number = float(value)

    if not np.isfinite(number) or not 0 <= number <= 1:
        raise ValueError("The p-value must be finite and between 0 and 1.")

    if number < 0.0001:
        return f"{number:.2e}"

    return f"{number:.4f}"


def _validate_dataframe(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    dataset_name: str,
) -> None:
    """Validate that an analytical DataFrame contains usable data."""

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(f"{dataset_name} must be a pandas DataFrame.")

    if dataframe.empty:
        raise ValueError(f"{dataset_name} data is unavailable.")

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{', '.join(sorted(missing_columns))}."
        )


def _validate_numeric_values(
    values: dict[str, float],
) -> None:
    """Ensure numerical evidence contains only finite values."""

    for name, value in values.items():
        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Statistical result '{name}' is not numeric.") from error

        if not np.isfinite(number):
            raise ValueError(f"Statistical result '{name}' is not finite.")


def generate_insights_and_recommendations(
    connection: duckdb.DuckDBPyConnection,
) -> dict:
    """
    Generate evidence-based findings and recommendations.

    Returns:
        A dictionary containing:
        - findings
        - recommendations
        - statistical_evidence
        - data_limitations
    """

    if connection is None:
        raise ValueError("A valid DuckDB connection is required.")

    # --------------------------------------------------
    # LOAD STATISTICAL RESULTS
    # --------------------------------------------------

    distribution_df = get_ridership_distribution(connection)
    borough_df = get_borough_statistics(connection)
    mode_df = get_transit_mode_statistics(connection)

    paired_comparison = compare_paired_weekday_weekend_ridership(connection)

    _validate_dataframe(
        distribution_df,
        {
            "mean_ridership",
            "median_ridership",
            "standard_deviation",
            "skewness",
        },
        "Ridership distribution",
    )

    _validate_dataframe(
        borough_df,
        {
            "borough",
            "average_ridership",
            "median_ridership",
            "unique_stations",
        },
        "Borough statistics",
    )

    _validate_dataframe(
        mode_df,
        {
            "transit_mode",
            "average_ridership",
            "median_ridership",
            "unique_stations",
        },
        "Transit mode statistics",
    )

    if not isinstance(paired_comparison, dict):
        raise TypeError("Paired statistical results must be a dictionary.")

    required_evidence = {
        "paired_months",
        "wednesday_mean_ridership",
        "saturday_mean_ridership",
        "mean_paired_difference",
        "median_paired_difference",
        "mean_difference_ci_95_lower",
        "mean_difference_ci_95_upper",
        "wilcoxon_statistic",
        "p_value",
        "rank_biserial_correlation",
        "statistically_significant",
    }

    missing_evidence = required_evidence.difference(paired_comparison)

    if missing_evidence:
        raise ValueError(
            "Paired statistical results are missing required fields: "
            f"{', '.join(sorted(missing_evidence))}."
        )

    distribution = distribution_df.iloc[0]
    leading_borough = borough_df.iloc[0]
    leading_mode = mode_df.iloc[0]

    # --------------------------------------------------
    # VALIDATE ANALYTICAL VALUES
    # --------------------------------------------------

    _validate_numeric_values(
        {
            "mean_ridership": distribution["mean_ridership"],
            "median_ridership": distribution["median_ridership"],
            "standard_deviation": distribution["standard_deviation"],
            "skewness": distribution["skewness"],
            "borough_average": leading_borough["average_ridership"],
            "borough_median": leading_borough["median_ridership"],
            "mode_average": leading_mode["average_ridership"],
            "mode_median": leading_mode["median_ridership"],
        }
    )

    _validate_numeric_values(
        {
            name: paired_comparison[name]
            for name in required_evidence
            if name != "statistically_significant" and name != "paired_months"
        }
    )

    if int(paired_comparison["paired_months"]) < 2:
        raise ValueError("At least two matched monthly observations are required.")

    if not isinstance(
        paired_comparison["statistically_significant"],
        (bool, np.bool_),
    ):
        raise ValueError("The statistical significance indicator must be boolean.")

    if not 0 <= float(paired_comparison["p_value"]) <= 1:
        raise ValueError("The Wilcoxon p-value must be between 0 and 1.")

    if not -1 <= float(paired_comparison["rank_biserial_correlation"]) <= 1:
        raise ValueError("Rank-biserial correlation must be between -1 and 1.")

    if float(paired_comparison["mean_difference_ci_95_lower"]) > float(
        paired_comparison["mean_difference_ci_95_upper"]
    ):
        raise ValueError("The confidence interval bounds are invalid.")

    if (
        not isinstance(leading_borough["borough"], str)
        or not leading_borough["borough"].strip()
    ):
        raise ValueError("The leading borough name is invalid.")

    if (
        not isinstance(leading_mode["transit_mode"], str)
        or not leading_mode["transit_mode"].strip()
    ):
        raise ValueError("The leading transit mode is invalid.")

    # --------------------------------------------------
    # FINDINGS
    # --------------------------------------------------

    findings = []

    mean_ridership = float(distribution["mean_ridership"])
    median_ridership = float(distribution["median_ridership"])
    skewness = float(distribution["skewness"])

    findings.append(
        {
            "category": "Ridership distribution",
            "title": "Station-level ridership varies considerably",
            "observation": (
                f"The average monthly station-level ridership is "
                f"{_format_number(mean_ridership)}, compared with a "
                f"median of {_format_number(median_ridership)}."
            ),
            "evidence": (
                f"Standard deviation: "
                f"{_format_number(distribution['standard_deviation'])}. "
                f"Distribution skewness: {skewness:.2f}."
            ),
            "interpretation": (
                "The difference between the mean and median, together "
                "with the skewness, helps describe how ridership is "
                "distributed across station-month observations."
            ),
        }
    )

    findings.append(
        {
            "category": "Borough comparison",
            "title": (
                f"{leading_borough['borough']} has the highest "
                "average station-level ridership"
            ),
            "observation": (
                f"{leading_borough['borough']} records an average "
                f"monthly station-level ridership of "
                f"{_format_number(leading_borough['average_ridership'])}."
            ),
            "evidence": (
                f"Median: "
                f"{_format_number(leading_borough['median_ridership'])}; "
                f"stations represented: "
                f"{int(leading_borough['unique_stations']):,}."
            ),
            "interpretation": (
                "This identifies a borough with high average demand "
                "per station-month observation. It should not be "
                "interpreted as the borough with the highest total "
                "ridership."
            ),
        }
    )

    findings.append(
        {
            "category": "Transit mode",
            "title": (
                f"{leading_mode['transit_mode']} has the highest "
                "average station-level ridership"
            ),
            "observation": (
                f"The highest average monthly station-level ridership "
                f"among transit modes is "
                f"{_format_number(leading_mode['average_ridership'])} "
                f"for {leading_mode['transit_mode']}."
            ),
            "evidence": (
                f"Median: "
                f"{_format_number(leading_mode['median_ridership'])}; "
                f"stations represented: "
                f"{int(leading_mode['unique_stations']):,}."
            ),
            "interpretation": (
                "Average station-level demand differs across transit "
                "modes. These figures describe monthly station-level "
                "observations, not total network-wide mode demand."
            ),
        }
    )

    weekday_mean = float(paired_comparison["wednesday_mean_ridership"])
    weekend_mean = float(paired_comparison["saturday_mean_ridership"])
    mean_difference = float(paired_comparison["mean_paired_difference"])
    p_value = float(paired_comparison["p_value"])
    statistically_significant = bool(paired_comparison["statistically_significant"])

    findings.append(
        {
            "category": "Weekday versus weekend",
            "title": (
                "Wednesday ridership is higher than Saturday "
                "ridership in the matched monthly sample"
                if mean_difference > 0
                else (
                    "Saturday ridership is higher than Wednesday "
                    "ridership in the matched monthly sample"
                    if mean_difference < 0
                    else "Wednesday and Saturday have equal mean "
                    "ridership in the matched monthly sample"
                )
            ),
            "observation": (
                f"Mean Wednesday daily ridership was "
                f"{_format_number(weekday_mean)}, compared with "
                f"{_format_number(weekend_mean)} on Saturdays."
            ),
            "evidence": (
                f"Mean paired difference: "
                f"{_format_number(mean_difference)}; "
                f"95% confidence interval: "
                f"{_format_number(paired_comparison['mean_difference_ci_95_lower'])} "
                f"to "
                f"{_format_number(paired_comparison['mean_difference_ci_95_upper'])}; "
                f"Wilcoxon p-value: {_format_p_value(p_value)}; "
                f"paired months: {paired_comparison['paired_months']}."
            ),
            "interpretation": (
                "The paired Wilcoxon test indicates a statistically "
                "significant difference in the sampled Wednesday and "
                "Saturday daily ridership observations."
                if statistically_significant
                else "The paired Wilcoxon test does not establish a "
                "statistically significant difference at the 5% level."
            ),
        }
    )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = [
        {
            "priority": "High",
            "title": "Prioritize demand monitoring in high-ridership areas",
            "action": (
                f"Use {leading_borough['borough']} as an initial "
                "priority for detailed station-level demand monitoring."
            ),
            "reason": (
                "It has the highest average monthly station-level "
                "ridership among the boroughs in the analysis."
            ),
            "consideration": (
                "Validate individual station demand and service "
                "conditions before making resource-allocation decisions."
            ),
        },
        {
            "priority": "High",
            "title": "Consider different weekday and weekend service patterns",
            "action": (
                "Evaluate whether service planning and operational "
                "resources should account for differences between "
                "midweek and Saturday demand."
            ),
            "reason": (
                f"The matched sample shows an average daily ridership "
                f"difference of {_format_number(mean_difference)} "
                f"between Wednesday and Saturday."
            ),
            "consideration": (
                "Use additional daily observations and operational "
                "data before changing train frequency or schedules."
            ),
        },
        {
            "priority": "Medium",
            "title": "Use station-level demand for targeted planning",
            "action": (
                "Investigate high-ridership station complexes "
                "individually when evaluating passenger-flow "
                "management and station improvements."
            ),
            "reason": (
                "Network-wide and borough averages can conceal "
                "substantial differences between individual stations."
            ),
            "consideration": (
                "Combine ridership with station capacity, accessibility, "
                "and service-frequency data before prioritizing "
                "infrastructure investments."
            ),
        },
        {
            "priority": "Medium",
            "title": "Maintain mode-specific demand analysis",
            "action": (
                "Monitor subway and Staten Island Railway demand "
                "separately when assessing network performance."
            ),
            "reason": ("Average station-level ridership differs across transit modes."),
            "consideration": (
                "Account for differences in network size and the "
                "number of stations represented in each mode."
            ),
        },
    ]

    # --------------------------------------------------
    # STATISTICAL EVIDENCE
    # --------------------------------------------------

    statistical_evidence = {
        "paired_months": int(paired_comparison["paired_months"]),
        "wednesday_mean_ridership": weekday_mean,
        "saturday_mean_ridership": weekend_mean,
        "mean_paired_difference": mean_difference,
        "median_paired_difference": float(
            paired_comparison["median_paired_difference"]
        ),
        "confidence_interval_lower": float(
            paired_comparison["mean_difference_ci_95_lower"]
        ),
        "confidence_interval_upper": float(
            paired_comparison["mean_difference_ci_95_upper"]
        ),
        "wilcoxon_statistic": float(paired_comparison["wilcoxon_statistic"]),
        "p_value": p_value,
        "rank_biserial_correlation": float(
            paired_comparison["rank_biserial_correlation"]
        ),
        "statistically_significant": statistically_significant,
        "significance_level": 0.05,
    }

    # --------------------------------------------------
    # DATA LIMITATIONS
    # --------------------------------------------------

    data_limitations = [
        (
            "Historical coverage: The study covers MTA ridership "
            "data from January 2020 through December 2024."
        ),
        (
            "Selected hourly sample: Hourly comparisons use one "
            "Wednesday and one Saturday per month, rather than "
            "continuous observations for every day."
        ),
        (
            "Statistical scope: The weekday-weekend test applies "
            "to the matched monthly samples and should not be "
            "generalized automatically to every day of the year."
        ),
        (
            "Ridership interpretation: Ridership records do not "
            "directly measure passenger occupancy, crowding, "
            "station capacity, or train frequency."
        ),
        (
            "Transfers: Transfers are already included in ridership "
            "and should not be added to ridership totals."
        ),
        (
            "Recommendations: Operational recommendations require "
            "additional information about service frequency, "
            "capacity, costs, and station conditions."
        ),
    ]

    return {
        "findings": findings,
        "recommendations": recommendations,
        "statistical_evidence": statistical_evidence,
        "data_limitations": data_limitations,
    }


def generate_recommendations(
    connection: duckdb.DuckDBPyConnection,
) -> list:
    """Return only the actionable recommendations."""

    result = generate_insights_and_recommendations(connection)

    return result["recommendations"]
