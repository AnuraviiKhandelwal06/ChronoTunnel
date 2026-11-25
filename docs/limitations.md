# ChronoTunnel — Limitations and Future Improvements

## 1. Overview

ChronoTunnel analyzes historical New York City subway ridership data to identify temporal, geographic, and station-level demand patterns. Its findings are based on the available datasets, sampling design, analytical assumptions, and current implementation.

This document records the limitations that should be considered when interpreting analytical results or using the platform to support transportation planning decisions.

The limitations are grouped into data coverage, analytical methodology, geospatial interpretation, recommendations, and technical implementation.

## 2. Dataset Coverage and Temporal Limitations

### 2.1 Historical Data Period

The current analytical datasets cover January 2020 through December 2024.

Consequently:

- The platform does not represent current or real-time subway conditions.
- Trends beyond December 2024 are not included.
- Historical patterns should not automatically be treated as forecasts of future demand.
- Changes in ridership after the covered period require updated source data and pipeline execution.

### 2.2 Limited Hourly Sampling

The hourly analytical dataset is a representative sample rather than a continuous record of every hour.

It contains 120 selected dates across the five-year period, consisting of one Wednesday and one Saturday per month.

This sampling design supports selected weekday-versus-weekend and hourly pattern comparisons, but it introduces important constraints:

- It does not capture every weekday or weekend day.
- It cannot establish complete hourly demand patterns for every date.
- Unusual events, holidays, service disruptions, and exceptional demand days may not be represented.
- Hourly results should be interpreted as patterns within the selected sample, not as complete historical hourly totals.

The monthly dataset provides broader monthly coverage, but it does not remove the hourly dataset's sampling limitations.

### 2.3 Pandemic-Era Effects

The dataset includes 2020, a period affected by the COVID-19 pandemic and substantial changes in travel behavior.

The resulting ridership patterns may reflect exceptional circumstances rather than ordinary transportation demand.

Although some seasonal comparisons exclude 2020, this does not eliminate all pandemic-related effects from the remaining period. Changes in commuting behavior and recovery patterns may continue to influence later observations.

## 3. Data Quality and Representation Limitations

### 3.1 Station Identity

Station records are identified using the combination of `station_complex_id` and `transit_mode`.

A station complex may therefore have multiple records associated with different transit modes. Analyses that count station records without considering this composite identity may produce misleading station counts.

Station names, borough metadata, and source classifications should also be interpreted in the context of the source dataset.

### 3.2 Geographic Coordinates

The station coordinate dataset provides representative geographic positions for station complexes.

These coordinates should not be interpreted as:

- Exact station entrances or exits.
- Individual platform locations.
- Passenger origins or destinations.
- Precise pedestrian access points.

Some station complexes may have multiple coordinate variants in the source data. The processed coordinate dataset uses representative positions for geographic analysis.

Maps and spatial summaries therefore communicate approximate station-level geography rather than detailed passenger movement.

### 3.3 Ridership and Transfers

Ridership and transfers are separate measures in the source data.

They are retained as distinct analytical variables and should not be combined into a single passenger-demand measure without a clearly defined methodology.

The interpretation of either measure depends on the source dataset's definitions and reporting conventions.

### 3.4 Aggregation Effects

Aggregation at monthly, borough, station-complex, or transit-mode level can conceal variation within individual stations, dates, and hours.

For example, borough-level totals may be dominated by a small number of high-demand station complexes. Aggregate results should therefore be considered alongside station-level and temporal analysis where appropriate.

## 4. Statistical and Analytical Limitations

### 4.1 Descriptive Analysis

Most ChronoTunnel findings describe observed ridership patterns.

They identify distributions, trends, differences, concentrations, and associations within the available data. They do not establish that one factor caused a change in ridership.

### 4.2 Weekday and Weekend Comparisons

The weekday-versus-weekend analysis focuses on selected Wednesdays and Saturdays.

The statistical workflow uses:

- Mann–Whitney U testing for independent daily observations.
- Paired Wilcoxon signed-rank testing for matched monthly Wednesday–Saturday comparisons.

These tests answer different statistical questions and should not be treated as interchangeable.

The results remain subject to the sampling design and assumptions of the selected tests. They do not represent every weekday and weekend observation across the full historical period.

### 4.3 Statistical Significance and Effect Size

A small p-value does not independently establish practical importance.

Statistical findings should be interpreted alongside effect-size measures, observed differences, sample size, and the analytical context.

The confidence interval calculated for the paired mean difference uses a t-based approach. It is not a confidence interval directly produced by the Wilcoxon signed-rank test.

### 4.4 Limited External Variables

The current analysis primarily uses ridership, transfers, timestamps, station metadata, borough classifications, transit modes, and geographic coordinates.

It does not comprehensively control for external factors such as:

- Subway service frequency and service disruptions.
- Weather conditions.
- Public events and holidays.
- Changes in population and employment.
- Fare policy changes.
- Construction and station closures.
- Broader economic and behavioral changes.

These factors may influence ridership and should be considered before drawing broader conclusions.

## 5. Geospatial Analysis Limitations

The current geographic analysis uses representative station coordinates and aggregates ridership by station or borough.

It does not model:

- Passenger origin-destination flows.
- Actual passenger routes.
- Walking distance or accessibility.
- Travel time between stations.
- Network connectivity or transfer paths.
- Population-weighted accessibility.
- Detailed catchment areas.

Geographic concentration on a map should therefore be interpreted as the spatial distribution of recorded station-level demand, not as a complete representation of passenger movement or transport accessibility.

Interactive map basemaps also depend on access to external OpenStreetMap tile services.

## 6. Recommendation and Decision-Support Limitations

ChronoTunnel produces analytical insights and recommendations based on observed historical patterns.

These recommendations are intended to support investigation and planning discussions. They are not independently validated operational interventions.

The current system does not establish the expected impact of a proposed service change, estimate intervention costs, or optimize schedules against operational constraints.

Before implementation, recommendations should be evaluated using additional operational data, domain expertise, stakeholder input, and appropriate impact-assessment methods.

## 7. Technical and Deployment Limitations

### 7.1 Local Execution

The current platform is designed for local execution using Python, Streamlit, Pandas, and DuckDB.

It is not currently a fully deployed, cloud-hosted production service.

### 7.2 Data Processing and Storage

The analytical pipeline reads configured processed datasets and uses an in-memory DuckDB connection for querying.

The current implementation does not provide a persistent analytical database, distributed processing infrastructure, or a streaming ingestion architecture.

### 7.3 Automation and Monitoring

The current implementation is manually executable through the pipeline entry point.

It does not include a production scheduler, automated source-data ingestion, continuous monitoring, or alerting infrastructure.

### 7.4 Application and API Infrastructure

The current user interface is built with Streamlit.

The platform does not currently expose a separately deployed backend API, multi-user authentication system, role-based access control, or production-grade service-level monitoring.

These capabilities would require additional architecture and operational work.

## 8. Future Improvements

The following improvements could extend the analytical depth and technical capabilities of ChronoTunnel.

### 8.1 Data Engineering

- Automate ingestion of updated MTA datasets.
- Introduce explicit data versioning and historical snapshots.
- Add incremental processing and reproducible pipeline runs.
- Evaluate persistent analytical storage for larger datasets.
- Expand data-quality monitoring and pipeline observability.

### 8.2 Advanced Analytics

- Incorporate a more comprehensive hourly dataset.
- Extend analysis to holidays, special events, and service disruptions.
- Develop demand forecasting models with temporal validation.
- Evaluate station-level anomaly detection.
- Introduce network-aware and origin-destination analysis where suitable data is available.
- Incorporate external explanatory variables to improve interpretation.

### 8.3 Geospatial Intelligence

- Integrate subway network and route connectivity data.
- Evaluate station accessibility and catchment areas.
- Incorporate population and employment distributions.
- Develop spatial clustering and network-based demand analysis.

### 8.4 Platform Engineering

- Introduce automated data-pipeline scheduling.
- Add persistent analytical storage where justified.
- Implement structured logging and monitoring.
- Add API services if independent application integrations become necessary.
- Evaluate deployment, authentication, and access-control requirements.

These are potential development directions, not capabilities currently claimed by the platform.

## 9. Responsible Interpretation

ChronoTunnel should be treated as a historical analytical and decision-support platform.

Users should:

1. Consider the coverage and sampling design before interpreting results.
2. Distinguish descriptive findings from causal conclusions.
3. Review statistical significance alongside effect size and sample limitations.
4. Interpret geographic results as representative station-level patterns.
5. Validate recommendations against operational and external evidence.
6. Avoid treating historical demand as a guarantee of future conditions.

## 10. Limitations Summary

ChronoTunnel provides a reproducible foundation for examining NYC subway ridership patterns across temporal, geographic, station, and borough dimensions.

Its current limitations primarily arise from the historical observation period, sampled hourly dataset, representative geographic coordinates, limited external variables, and local execution architecture.

Making these boundaries explicit helps ensure that the platform's findings are interpreted responsibly while providing a clear foundation for future improvements in data engineering, advanced analytics, geospatial intelligence, and platform deployment.