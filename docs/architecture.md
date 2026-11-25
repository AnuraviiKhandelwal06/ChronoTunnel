# ChronoTunnel — System Architecture

## 1. Overview

ChronoTunnel is an urban mobility intelligence platform designed to analyze New York City subway ridership patterns using public transportation data covering 2020–2024.

The platform combines a Python-based analytical backend, a DuckDB-powered data access layer, an orchestrated analytics pipeline, and a Streamlit application.

Its architecture separates data management, analytical processing, visualization, and application presentation into distinct modules to support maintainability, reproducibility, and future extensibility.

## 2. Architectural Design

ChronoTunnel follows a modular, layered architecture.

The major architectural layers are:

1. Data storage layer
2. Data access and validation layer
3. Analytical processing layer
4. Pipeline orchestration layer
5. Visualization and output layer
6. Streamlit presentation layer

### High-Level Architecture

```text
                         CHRONOTUNNEL
                              |
              +---------------+---------------+
              |                               |
         DATA STORAGE                    STREAMLIT APP
              |                               |
         Processed CSVs                  Landing Page
              |                               |
              v                          Dashboard Pages
         DATA ACCESS                          |
              |                          UI Components
         DuckDB Views                         |
              |                               |
              v                               |
        DATA VALIDATION                       |
              |                               |
              v                               |
      ANALYTICAL PROCESSING                   |
              |                               |
       +------+------+------+                 |
       |      |      |      |                 |
      EDA  Temporal Statistical Geospatial   |
       |      |      |      |                 |
       +------+------+------+                 |
              |                               |
              v                               |
      PIPELINE ORCHESTRATION                  |
              |                               |
              v                               |
      METRICS AND VISUALIZATIONS --------------+
              |
              v
           OUTPUTS
```

The diagram represents the major logical components. It does not imply that every dashboard page directly reads every pipeline output.

## 3. Repository Architecture

The primary application code is organized into two directories.

### 3.1 Analytical Backend — `src/chronotunnel/`

The backend contains reusable data-engineering and analytical modules.

| Module | Responsibility | Implementation Status |
|---|---|---|
| `config/` | Centralized project settings, dataset paths, and output directories. | Implemented |
| `data/` | Dataset loading, preprocessing, and data validation. | Implemented |
| `analysis/` | Exploratory, temporal, statistical, and geospatial analysis. | Implemented |
| `pipeline/` | Orchestration of the end-to-end analytical workflow. | Implemented |
| `visualization/` | Interactive charts and geospatial maps. | Implemented |
| `features/` | Reserved for future feature-engineering functionality. | Scaffolded; implementation pending |
| `recommendations/` | Recommendation-generation logic. | Implemented |
| `utils/` | Reserved for shared utility functions. | Scaffolded; implementation pending |

The primary analytical modules are:

- `analysis/eda.py`
- `analysis/temporal.py`
- `analysis/statistical.py`
- `analysis/geospatial.py`

The pipeline entry point is:

`src/chronotunnel/pipeline/run.py`

The feature-engineering and shared utility directories are currently structural extension points and are not part of the active analytical execution workflow.

### 3.2 Application Frontend — `app/`

The frontend is implemented using Streamlit.

| Component | Responsibility |
|---|---|
| `Landing.py` | Application entry point and landing experience. |
| `pages/00_Home.py` | Home dashboard. |
| `pages/01_Overview.py` | Ridership overview. |
| `pages/02_Temporal_Analysis.py` | Temporal ridership analysis. |
| `pages/03_Station_Analysis.py` | Station-level analysis. |
| `pages/04_Borough_Analysis.py` | Borough-level analysis. |
| `pages/05_Geospatial_Analysis.py` | Geographic analysis. |
| `pages/06_Insights_Recommendations.py` | Analytical insights and recommendations. |
| `components/` | Reusable interface components, metrics, charts, filters, rendering, navigation, and styling. |
| `config.py` | Application configuration. |

The component directory supports a reusable presentation structure rather than requiring every page to implement its own interface elements.

## 4. Data Architecture

ChronoTunnel organizes its datasets into separate storage stages:

- `data/raw/` — Raw source datasets.
- `data/interim/` — Intermediate datasets generated during processing.
- `data/processed/` — Analytical datasets prepared for downstream consumption.
- `data/external/` — Additional externally sourced datasets.
- `data/metadata/` — Dataset-related metadata.

The principal processed datasets are:

| Dataset | Description |
|---|---|
| `hourly_ridership_sample_station_level_2020_2024.csv` | Sampled hourly station-level ridership observations. |
| `monthly_ridership_station_level_2020_2024.csv` | Monthly station-level ridership observations. |
| `station_coordinates.csv` | Station-complex geographic reference information. |

The hourly dataset contains 120 selected dates, comprising one Wednesday and one Saturday per month. The monthly dataset covers January 2020 through December 2024.

## 5. Data Access Architecture

DuckDB provides the analytical data-access layer.

The module `src/chronotunnel/data/load.py` implements database connection creation and dataset registration.

The connection uses an in-memory DuckDB database.

During initialization, the following datasets are registered as views:

- `hourly`
- `monthly`
- `station_coordinates`

This allows analytical modules to query the processed CSV datasets using SQL without requiring a persistent database server.

The data-access module also provides:

- Monthly dataset loading.
- Station-coordinate loading.
- Filtered hourly data queries.
- Optional timestamp, station, and transit-mode filtering.
- Parameterized SQL query execution.

Hourly queries support optional row limits to control the amount of data returned to pandas.

## 6. Pipeline Architecture

The pipeline is orchestrated through:

`src/chronotunnel/pipeline/run.py`

The `run_pipeline()` function executes six sequential stages.

### Stage 1 — Data Validation

- Executes the centralized data-validation workflow.
- Saves validation results to `outputs/metrics/data_validation.csv`.
- Stops execution if a validation failure is detected.

### Stage 2 — Exploratory Data Analysis

Calculates:

- Yearly ridership.
- Monthly ridership trends.
- Borough-level ridership.
- Transit-mode ridership.
- Top station complexes.

### Stage 3 — Temporal Analysis

Calculates:

- Year-over-year growth.
- Monthly seasonality.
- Weekday and weekend comparisons.
- Peak-hour concentration.

### Stage 4 — Statistical Analysis

Calculates:

- Ridership distribution statistics.
- Borough statistics.
- Transit-mode statistics.
- Paired Wednesday–Saturday ridership comparison.

### Stage 5 — Geospatial Analysis

Calculates:

- Borough geospatial summaries.
- Top ridership locations.
- Ridership-weighted borough centroids.
- Coordinate-quality summaries.

### Stage 6 — Visualization Generation

Generates:

- Borough ridership chart.
- Top station chart.
- Hourly ridership comparison chart.
- Monthly ridership trend chart.
- Station ridership map.
- Ridership heatmap.

The pipeline saves analytical results and visualizations to the project's output directories.

## 7. Output Architecture

Pipeline outputs are organized into three primary directories.

| Directory | Contents |
|---|---|
| `outputs/metrics/` | CSV analytical results and JSON statistical comparison results. |
| `outputs/figures/` | Interactive HTML charts. |
| `outputs/maps/` | Interactive HTML geographic maps. |

Output directories are created automatically when the pipeline executes.

The pipeline uses a `try/finally` structure to ensure the DuckDB connection is closed after execution, including when an exception occurs.

## 8. Configuration Management

Project-wide configuration is maintained in:

`src/chronotunnel/config/settings.py`

The module defines:

- Project root directory.
- Data directory paths.
- Processed dataset locations.
- Output directory paths.
- Project metadata.
- Data coverage dates.
- Hourly sampling metadata.
- Expected station count.

Centralized configuration reduces the need to duplicate project paths across backend modules.

## 9. Architectural Principles

ChronoTunnel follows these design principles:

1. **Modularity:** Separate data, analysis, visualization, and presentation responsibilities.
2. **Reusability:** Keep reusable analytical logic in independent Python modules.
3. **Reproducibility:** Use documented datasets, assumptions, and repeatable pipeline execution.
4. **Data quality:** Validate datasets before downstream analytical processing.
5. **Separation of concerns:** Keep application presentation separate from core analytical calculations.
6. **Resource management:** Close database connections after pipeline execution.
7. **Extensibility:** Maintain independent analytical modules that can accommodate future capabilities.

## 10. Current Architecture Boundaries

The current implementation is a local analytical application built around processed CSV datasets, in-memory DuckDB, Python analytical modules, and Streamlit.

The architecture does not currently establish a production cloud deployment, distributed processing infrastructure, persistent database service, or automated real-time data ingestion system.

These capabilities should be treated as potential future extensions rather than existing platform functionality.

---

**Project:** ChronoTunnel
**Architecture:** Modular, layered analytical architecture
**Backend:** Python, Pandas, DuckDB
**Frontend:** Streamlit
**Data Coverage:** 2020–2024