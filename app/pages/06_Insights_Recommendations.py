import html
import math
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from src.chronotunnel.data.load import create_connection
from src.chronotunnel.recommendations.generate import (
    generate_insights_and_recommendations,
)

from components.sidebar import mount_dashboard

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Insights & Recommendations | ChronoTunnel",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------
# THEME
# ---------------------------------------------------------

COLORS = {
    "background": "#08090D",
    "surface": "#12151E",
    "surface_alt": "#171B26",
    "border": "rgba(255,255,255,0.09)",
    "text": "#F5F6FA",
    "muted": "#A7B0C2",
    "red": "#FF354D",
    "blue": "#7BA7FF",
    "pink": "#FF6B9A",
    "purple": "#A78BFA",
    "orange": "#FFAD70",
    "green": "#65C99A",
}

FONT = "DM Sans, sans-serif"
DISPLAY_FONT = "Space Grotesk, sans-serif"

# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------


def inject_page_styles():
    """Inject page-specific styling."""

    st.markdown(
        f"""
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap'
        );

        /* -----------------------------------------
           PAGE HEADER
        ----------------------------------------- */

        .insights-header {{
            margin-bottom: 2rem;
        }}

        .insights-eyebrow {{
            color: {COLORS["red"]};
            font-family: {FONT};
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.17em;
            text-transform: uppercase;
            margin-bottom: 0.65rem;
        }}

        .insights-title {{
            color: {COLORS["text"]};
            font-family: {DISPLAY_FONT};
            font-size: 2.45rem;
            font-weight: 600;
            line-height: 1.15;
            margin-bottom: 0.7rem;
        }}

        .insights-subtitle {{
            color: {COLORS["muted"]};
            font-family: {FONT};
            font-size: 0.95rem;
            line-height: 1.75;
            max-width: 850px;
        }}

        /* -----------------------------------------
           SECTION HEADINGS
        ----------------------------------------- */

        .section-heading {{
            color: {COLORS["text"]};
            font-family: {DISPLAY_FONT};
            font-size: 1.55rem;
            font-weight: 600;
            margin-top: 1.8rem;
            margin-bottom: 0.35rem;
        }}

        .section-description {{
            color: {COLORS["muted"]};
            font-family: {FONT};
            font-size: 0.85rem;
            line-height: 1.65;
            margin-bottom: 1.2rem;
        }}

        /* -----------------------------------------
           INSIGHT CARDS
        ----------------------------------------- */

        .insight-card {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            padding: 1.3rem 1.4rem;
            min-height: 245px;
            margin-bottom: 0.9rem;
            transition: border-color 0.2s ease;
        }}

        .insight-card:hover {{
            border-color: rgba(255,53,77,0.35);
        }}

        .insight-category {{
            color: {COLORS["red"]};
            font-family: {FONT};
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }}

        .insight-card h3 {{
            color: {COLORS["text"]};
            font-family: {DISPLAY_FONT};
            font-size: 1.1rem;
            font-weight: 600;
            line-height: 1.45;
            margin: 0 0 0.8rem 0;
        }}

        .insight-card p {{
            color: {COLORS["muted"]};
            font-family: {FONT};
            font-size: 0.85rem;
            line-height: 1.7;
            margin-bottom: 0.7rem;
        }}

        .insight-evidence {{
            background: rgba(123,167,255,0.07);
            border-left: 3px solid {COLORS["blue"]};
            border-radius: 5px;
            padding: 0.75rem 0.9rem;
            color: #C4D5F5;
            font-family: {FONT};
            font-size: 0.8rem;
            line-height: 1.65;
            margin-top: 0.9rem;
        }}

        .insight-evidence strong {{
            color: {COLORS["blue"]};
        }}

        /* -----------------------------------------
           RECOMMENDATION CARDS
        ----------------------------------------- */

        .recommendation-card {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            padding: 1.35rem 1.45rem;
            margin-bottom: 0.95rem;
            transition: border-color 0.2s ease;
        }}

        .recommendation-card:hover {{
            border-color: rgba(255,107,154,0.35);
        }}

        .recommendation-title {{
            color: {COLORS["text"]};
            font-family: {DISPLAY_FONT};
            font-size: 1.08rem;
            font-weight: 600;
            line-height: 1.45;
            margin: 0.8rem 0 1rem 0;
        }}

        .recommendation-label {{
            color: {COLORS["pink"]};
            font-family: {FONT};
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-top: 0.85rem;
            margin-bottom: 0.3rem;
        }}

        .recommendation-card p {{
            color: {COLORS["muted"]};
            font-family: {FONT};
            font-size: 0.85rem;
            line-height: 1.7;
            margin-bottom: 0.55rem;
        }}

        /* -----------------------------------------
           PRIORITY LABELS
        ----------------------------------------- */

        .priority-high {{
            display: inline-block;
            color: #FF9AA5;
            background: rgba(255,53,77,0.13);
            border: 1px solid rgba(255,53,77,0.25);
            border-radius: 20px;
            padding: 0.25rem 0.7rem;
            font-family: {FONT};
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .priority-medium {{
            display: inline-block;
            color: #FFD18F;
            background: rgba(255,173,112,0.11);
            border: 1px solid rgba(255,173,112,0.23);
            border-radius: 20px;
            padding: 0.25rem 0.7rem;
            font-family: {FONT};
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .priority-low {{
            display: inline-block;
            color: #9FC5FF;
            background: rgba(123,167,255,0.11);
            border: 1px solid rgba(123,167,255,0.23);
            border-radius: 20px;
            padding: 0.25rem 0.7rem;
            font-family: {FONT};
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        /* -----------------------------------------
           STATISTICAL EVIDENCE PANEL
        ----------------------------------------- */

        .evidence-panel {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            padding: 1.3rem 1.4rem;
            margin-top: 0.3rem;
        }}

        .evidence-panel strong {{
            color: {COLORS["text"]};
            font-weight: 600;
        }}

        .evidence-panel p {{
            color: {COLORS["muted"]};
            font-family: {FONT};
            font-size: 0.84rem;
            line-height: 1.7;
            margin: 0.45rem 0;
        }}

        .evidence-main-value {{
            color: {COLORS["blue"]};
            font-family: {DISPLAY_FONT};
            font-size: 2rem;
            font-weight: 700;
            margin: 0.25rem 0 1rem 0;
        }}

        /* -----------------------------------------
           METHODOLOGY AND FOOTER
        ----------------------------------------- */

        .method-note {{
            color: #8993A6;
            font-family: {FONT};
            font-size: 0.77rem;
            line-height: 1.7;
        }}

        .insights-footer {{
            color: #8993A6;
            font-family: {FONT};
            font-size: 0.72rem;
            letter-spacing: 0.1em;
            text-align: center;
            padding: 0.5rem 0;
        }}

        /* -----------------------------------------
           METRICS
        ----------------------------------------- */

        div[data-testid="stMetric"] {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 1rem 1.1rem;
        }}

        div[data-testid="stMetricLabel"] {{
            color: {COLORS["muted"]} !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: {COLORS["text"]} !important;
            font-family: {DISPLAY_FONT};
        }}

        div[data-testid="stMetricDelta"] {{
            color: {COLORS["green"]} !important;
        }}

        /* -----------------------------------------
           EXPANDERS
        ----------------------------------------- */

        div[data-testid="stExpander"] {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
        }}

        div[data-testid="stExpander"] summary {{
            color: {COLORS["text"]};
        }}

        /* -----------------------------------------
           DIVIDER
        ----------------------------------------- */

        hr {{
            border-color: {COLORS["border"]} !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# VALIDATION AND FORMATTING HELPERS
# ---------------------------------------------------------


def safe_text(value):
    """Escape text before inserting it into HTML."""

    return html.escape(str(value))


def validate_numeric_value(value, field_name):
    """Return a finite float or raise a descriptive validation error."""

    if isinstance(value, bool):
        raise ValueError(f"'{field_name}' must be numeric, not boolean.")

    try:
        numeric_value = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(
            f"'{field_name}' must contain a valid numeric value."
        ) from error

    if not math.isfinite(numeric_value):
        raise ValueError(f"'{field_name}' must contain a finite value.")

    return numeric_value


def format_number(value):
    """Format finite numeric values with thousands separators."""

    numeric_value = validate_numeric_value(value, "Displayed number")

    return f"{numeric_value:,.0f}"


def format_p_value(value):
    """Format a valid p-value without displaying small values as zero."""

    numeric_value = validate_numeric_value(value, "p-value")

    if not 0 <= numeric_value <= 1:
        raise ValueError("The p-value must be between 0 and 1.")

    if numeric_value < 0.0001:
        return f"{numeric_value:.2e}"

    return f"{numeric_value:.4f}"


def validate_text_fields(record, required_fields, record_name):
    """Validate required text fields in a generated record."""

    if not isinstance(record, dict):
        raise ValueError(f"Each {record_name} must be a dictionary.")

    for field in required_fields:
        value = record.get(field)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Each {record_name} must contain a non-empty '{field}' field."
            )


def validate_results(results):
    """Validate the complete output contract from the insight generator."""

    if not isinstance(results, dict):
        raise ValueError("The insight generator must return a dictionary.")

    required_result_fields = {
        "findings",
        "recommendations",
        "statistical_evidence",
        "data_limitations",
    }

    missing_fields = required_result_fields.difference(results)

    if missing_fields:
        raise ValueError(
            "Insight results are missing required fields: "
            + ", ".join(sorted(missing_fields))
        )

    findings = results["findings"]
    recommendations = results["recommendations"]
    evidence = results["statistical_evidence"]
    limitations = results["data_limitations"]

    if not isinstance(findings, list):
        raise ValueError("'findings' must be a list.")

    if not isinstance(recommendations, list):
        raise ValueError("'recommendations' must be a list.")

    if not isinstance(evidence, dict):
        raise ValueError("'statistical_evidence' must be a dictionary.")

    if not isinstance(limitations, list):
        raise ValueError("'data_limitations' must be a list.")

    finding_fields = (
        "category",
        "title",
        "observation",
        "evidence",
        "interpretation",
    )

    recommendation_fields = (
        "priority",
        "title",
        "action",
        "reason",
        "consideration",
    )

    for finding in findings:
        validate_text_fields(
            finding,
            finding_fields,
            "finding",
        )

    for recommendation in recommendations:
        validate_text_fields(
            recommendation,
            recommendation_fields,
            "recommendation",
        )

    if any(
        not isinstance(limitation, str) or not limitation.strip()
        for limitation in limitations
    ):
        raise ValueError("Every data limitation must be a non-empty string.")

    required_evidence_fields = (
        "paired_months",
        "wednesday_mean_ridership",
        "saturday_mean_ridership",
        "mean_paired_difference",
        "median_paired_difference",
        "confidence_interval_lower",
        "confidence_interval_upper",
        "wilcoxon_statistic",
        "p_value",
        "rank_biserial_correlation",
        "statistically_significant",
        "significance_level",
    )

    missing_evidence = set(required_evidence_fields).difference(evidence)

    if missing_evidence:
        raise ValueError(
            "Statistical evidence is missing required fields: "
            + ", ".join(sorted(missing_evidence))
        )

    paired_months = evidence["paired_months"]

    if isinstance(paired_months, bool) or not isinstance(paired_months, int):
        raise ValueError("'paired_months' must be an integer.")

    if paired_months < 2:
        raise ValueError(
            "At least two matched months are required for the "
            "paired statistical comparison."
        )

    numeric_fields = (
        "wednesday_mean_ridership",
        "saturday_mean_ridership",
        "mean_paired_difference",
        "median_paired_difference",
        "confidence_interval_lower",
        "confidence_interval_upper",
        "wilcoxon_statistic",
        "p_value",
        "rank_biserial_correlation",
        "significance_level",
    )

    for field in numeric_fields:
        evidence[field] = validate_numeric_value(
            evidence[field],
            field,
        )

    if evidence["wednesday_mean_ridership"] < 0:
        raise ValueError("Wednesday mean ridership cannot be negative.")

    if evidence["saturday_mean_ridership"] < 0:
        raise ValueError("Saturday mean ridership cannot be negative.")

    if evidence["wilcoxon_statistic"] < 0:
        raise ValueError("The Wilcoxon statistic cannot be negative.")

    if not 0 <= evidence["p_value"] <= 1:
        raise ValueError("The p-value must be between 0 and 1.")

    if not -1 <= evidence["rank_biserial_correlation"] <= 1:
        raise ValueError("Rank-biserial correlation must be between -1 and 1.")

    if not 0 < evidence["significance_level"] < 1:
        raise ValueError("The significance level must be between 0 and 1.")

    if evidence["confidence_interval_lower"] > evidence["confidence_interval_upper"]:
        raise ValueError(
            "The confidence interval lower bound cannot exceed its upper bound."
        )

    if not isinstance(evidence["statistically_significant"], bool):
        raise ValueError("'statistically_significant' must be a boolean.")

    expected_significance = evidence["p_value"] < evidence["significance_level"]

    if evidence["statistically_significant"] != expected_significance:
        raise ValueError(
            "The statistical significance flag does not agree "
            "with the p-value and significance level."
        )

    return results


# ---------------------------------------------------------
# RENDERING HELPERS
# ---------------------------------------------------------


def render_section_heading(title, description):
    """Render a section heading and description."""

    st.html(
        f"""
        <div class="section-heading">{safe_text(title)}</div>
        <div class="section-description">
            {safe_text(description)}
        </div>
        """
    )


def render_finding(finding):
    """Render an individual analytical finding."""

    category = safe_text(finding["category"])
    title = safe_text(finding["title"])
    observation = safe_text(finding["observation"])
    evidence = safe_text(finding["evidence"])
    interpretation = safe_text(finding["interpretation"])

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-category">
                {category}
            </div>

            <h3>{title}</h3>

            <p>{observation}</p>

            <div class="insight-evidence">
                <strong>Evidence</strong><br>
                {evidence}
            </div>

            <p style="margin-top: 0.85rem; margin-bottom: 0;">
                <strong>Interpretation:</strong> {interpretation}
            </p>

        </div>
        """
    )


def render_recommendation(recommendation):
    """Render an actionable recommendation."""

    priority = recommendation["priority"]

    priority_classes = {
        "High": "priority-high",
        "Medium": "priority-medium",
        "Low": "priority-low",
    }

    priority_class = priority_classes.get(
        priority,
        "priority-medium",
    )

    title = safe_text(recommendation["title"])
    action = safe_text(recommendation["action"])
    reason = safe_text(recommendation["reason"])
    consideration = safe_text(recommendation["consideration"])

    st.html(
        f"""
        <div class="recommendation-card">

            <span class="{priority_class}">
                {safe_text(priority)} Priority
            </span>

            <div class="recommendation-title">
                {title}
            </div>

            <div class="recommendation-label">
                Suggested action
            </div>
            <p>{action}</p>

            <div class="recommendation-label">
                Why it matters
            </div>
            <p>{reason}</p>

            <div class="recommendation-label">
                Planning consideration
            </div>
            <p style="margin-bottom: 0;">
                {consideration}
            </p>

        </div>
        """
    )


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------


@st.cache_data(show_spinner="Generating analytical insights...")
def get_recommendation_results():
    """Load the database and generate validated analytical insights."""

    connection = create_connection()

    try:
        results = generate_insights_and_recommendations(connection)

        return validate_results(results)

    finally:
        connection.close()


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

mount_dashboard()
inject_page_styles()

# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.html(
    """
    <div class="insights-header">

        <div class="insights-eyebrow">
            Decision Intelligence · 2020–2024
        </div>

        <div class="insights-title">
            Insights & Recommendations
        </div>

        <div class="insights-subtitle">
            Translate ridership patterns into evidence-based findings
            and practical planning recommendations for New York City's
            public transit network.
        </div>

    </div>
    """
)

# ---------------------------------------------------------
# GENERATE RESULTS
# ---------------------------------------------------------

try:
    results = get_recommendation_results()

except Exception as error:
    st.error(
        "Unable to generate insights and recommendations. "
        "Please verify that the analytical data and database "
        "connection are available."
    )

    with st.expander("Technical details"):
        st.exception(error)

    st.stop()

findings = results["findings"]
recommendations = results["recommendations"]
evidence = results["statistical_evidence"]
limitations = results["data_limitations"]

# ---------------------------------------------------------
# KEY METRICS
# ---------------------------------------------------------

render_section_heading(
    "Research at a glance",
    "A summary of the analytical outputs generated from the study.",
)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.metric("Key findings", len(findings))

with metric_2:
    st.metric("Recommendations", len(recommendations))

with metric_3:
    st.metric("Matched months", evidence["paired_months"])

with metric_4:
    significance_label = (
        "Significant" if evidence["statistically_significant"] else "Not significant"
    )

    st.metric(
        "Statistical significance",
        significance_label,
    )

# ---------------------------------------------------------
# ANALYTICAL FINDINGS
# ---------------------------------------------------------

render_section_heading(
    "Evidence-based findings",
    "Key observations derived from station-level and daily ridership analysis.",
)

for index in range(0, len(findings), 2):
    columns = st.columns(2)

    with columns[0]:
        render_finding(findings[index])

    if index + 1 < len(findings):
        with columns[1]:
            render_finding(findings[index + 1])

# ---------------------------------------------------------
# WEEKDAY VS WEEKEND STATISTICAL COMPARISON
# ---------------------------------------------------------

render_section_heading(
    "Weekday vs weekend evidence",
    "A paired monthly comparison of sampled Wednesday and Saturday daily ridership.",
)

weekday_mean = evidence["wednesday_mean_ridership"]
weekend_mean = evidence["saturday_mean_ridership"]
mean_difference = evidence["mean_paired_difference"]

chart_col, evidence_col = st.columns([1.4, 1])

with chart_col:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Wednesday", "Saturday"],
            y=[weekday_mean, weekend_mean],
            marker_color=[
                COLORS["red"],
                COLORS["blue"],
            ],
            text=[
                format_number(weekday_mean),
                format_number(weekend_mean),
            ],
            textposition="outside",
            textfont=dict(
                color=COLORS["text"],
                size=12,
            ),
            hovertemplate=("%{x}<br>Daily ridership: %{y:,.0f}<extra></extra>"),
        )
    )

    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=35, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=COLORS["muted"],
            family=FONT,
        ),
        yaxis=dict(
            title="Mean daily ridership",
            title_font=dict(color=COLORS["muted"]),
            tickfont=dict(color=COLORS["muted"]),
            showgrid=True,
            gridcolor=COLORS["border"],
            zeroline=False,
        ),
        xaxis=dict(
            title="",
            tickfont=dict(color=COLORS["text"]),
            showgrid=False,
        ),
        showlegend=False,
        bargap=0.48,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

with evidence_col:
    st.html(
        f"""
        <div class="evidence-panel">

            <div class="insight-category">
                Paired comparison
            </div>

            <p>
                <strong>Mean paired difference</strong>
            </p>

            <div class="evidence-main-value">
                {format_number(mean_difference)}
            </div>

            <p>
                <strong>95% confidence interval</strong><br>
                {format_number(evidence["confidence_interval_lower"])}
                to
                {format_number(evidence["confidence_interval_upper"])}
            </p>

            <p>
                <strong>Wilcoxon p-value</strong><br>
                {format_p_value(evidence["p_value"])}
            </p>

            <p>
                <strong>Rank-biserial correlation</strong><br>
                {evidence["rank_biserial_correlation"]:.4f}
            </p>

            <p>
                <strong>Matched observations</strong><br>
                {evidence["paired_months"]} months
            </p>

        </div>
        """
    )

# ---------------------------------------------------------
# STATISTICAL INTERPRETATION
# ---------------------------------------------------------

if evidence["statistically_significant"]:
    st.success(
        "The paired Wilcoxon signed-rank test identifies a statistically "
        "significant difference between the sampled Wednesday and Saturday "
        "ridership observations at the "
        f"{evidence['significance_level']:.0%} significance level."
    )

else:
    st.info(
        "The paired Wilcoxon signed-rank test does not establish a "
        "statistically significant difference at the "
        f"{evidence['significance_level']:.0%} significance level."
    )

st.html(
    """
    <p class="method-note">
        Statistical note: The comparison uses matched monthly observations.
        The confidence interval is calculated using the paired differences
        and a t-based interval. Statistical significance does not establish
        the cause of the observed difference.
    </p>
    """
)

# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

render_section_heading(
    "Planning recommendations",
    "Potential actions informed by the observed ridership patterns. "
    "These are planning suggestions, not automatic operational decisions.",
)

for recommendation in recommendations:
    render_recommendation(recommendation)

# ---------------------------------------------------------
# DATA LIMITATIONS
# ---------------------------------------------------------

render_section_heading(
    "Study limitations",
    "Important context for interpreting the findings and recommendations.",
)

with st.expander(
    "View data limitations and interpretation notes",
    expanded=False,
):
    for limitation in limitations:
        st.markdown(f"- {safe_text(limitation)}")

# ---------------------------------------------------------
# METHODOLOGY
# ---------------------------------------------------------

with st.expander(
    "Statistical methodology",
    expanded=False,
):
    st.markdown(
        """
        **Ridership distribution**

        Descriptive statistics are used to examine the distribution of
        monthly station-level ridership, including the mean, median,
        standard deviation and skewness.

        **Borough and transit-mode comparison**

        Average and median station-level ridership are calculated
        separately for each borough and transit mode.

        **Weekday and weekend comparison**

        Wednesday and Saturday daily ridership observations are matched
        by month. A two-sided Wilcoxon signed-rank test is used to assess
        whether the paired differences are statistically significant.

        **Effect size**

        Rank-biserial correlation is reported to describe the direction
        and magnitude of the paired differences.

        **Confidence interval**

        A 95% t-based confidence interval is calculated for the mean
        paired difference.
        """
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.html(
    """
    <div class="insights-footer">
        ChronoTunnel · URBAN MOBILITY INTELLIGENCE · MTA RIDERSHIP STUDY · 2020–2024
    </div>
    """
)
