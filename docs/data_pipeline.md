# ChronoTunnel — Data Pipeline

## 1. Overview

ChronoTunnel uses a structured data pipeline to load, validate, query, analyze, and visualize NYC subway ridership data from 2020 to 2024.

The pipeline is designed to keep data access separate from analytical logic and visualization. DuckDB provides the query layer, Pandas supports data preparation and analysis, and the pipeline orchestrator coordinates the execution of analytical modules.

The pipeline produces reusable analytical datasets, statistical results, interactive charts, and geospatial visualizations.

## 2. Pipeline Architecture

The current pipeline follows six major stages:

1. Data loading and connection initialization
2. Data validation
3. Exploratory data analysis
4. Temporal and statistical analysis
5. Geospatial analysis
6. Visualization generation and output storage

### High-Level Workflow

```text
Processed CSV Datasets
        |
        v
DuckDB In-Memory Connection
        |
        v
Dataset Registration
        |
        v
Data Validation
        |
        v
Exploratory Data Analysis
        |
        v
Temporal and Statistical Analysis
        |
        v
Geospatial Analysis
        |
        v
Charts, Maps, Metrics and Reports
        |
        v
Outputs Directory
```

## 3. Project Configuration and Paths

All major project paths and dataset settings are centralized in:

`src/chronotunnel/config/settings.py`

The project root is resolved dynamically using the location of the settings module:

```python
PROJECT_ROOT = Path(__file__).resolve().parents[3]
```

This avoids relying on a hardcoded machine-specific project directory.

### Data Directories

| Constant | Purpose |
|---|---|
| `DATA_DIR` | Root data directory |
| `RAW_DATA_DIR` | Raw source data |
| `INTERIM_DATA_DIR` | Intermediate data |
| `PROCESSED_DATA_DIR` | Processed analytical datasets |
| `EXTERNAL_DATA_DIR` | External supporting data |
| `METADATA_DIR` | Dataset metadata |

### Processed Dataset Paths

| Constant | Dataset |
|---|---|
| `HOURLY_DATA_PATH` | `hourly_ridership_sample_station_level_2020_2024.csv` |
| `MONTHLY_DATA_PATH` | `monthly_ridership_station_level_2020_2024.csv` |
| `STATION_COORDINATES_PATH` | `station_coordinates.csv` |

The current analytical pipeline reads these three processed CSV datasets.

The raw, interim, external, and metadata directory constants provide centralized project paths; their presence does not imply that every directory is actively used by the current pipeline execution.

### Output Directories

| Constant | Purpose |
|---|---|
| `OUTPUTS_DIR` | Root directory for generated outputs |
| `FIGURES_DIR` | Interactive charts and figures |
| `MAPS_DIR` | Geospatial maps |
| `METRICS_DIR` | Analytical metrics and tabular results |
| `REPORTS_DIR` | Reserved path for reports |

The current pipeline explicitly creates the figures, maps, and metrics directories when it runs.

## 4. Data Loading and Query Layer

**Module:** `src/chronotunnel/data/load.py`

ChronoTunnel uses DuckDB to provide a lightweight analytical query layer over the processed CSV files.

### 4.1 Connection Initialization

The `create_connection()` function creates an in-memory DuckDB connection and registers the processed datasets.

```python
connection = duckdb.connect(database=":memory:")
```

The connection is initialized for the current pipeline execution rather than relying on a persistent database server.

### 4.2 Dataset Registration

The `register_datasets()` function registers the processed CSV files as DuckDB views:

| View Name | Source |
|---|---|
| `hourly` | Hourly ridership dataset |
| `monthly` | Monthly ridership dataset |
| `station_coordinates` | Station coordinates dataset |

Before registration, the function checks whether each configured dataset file exists. A missing file raises `FileNotFoundError`.

DuckDB reads the CSV files and exposes them through queryable views.

### 4.3 Data Access Functions

The loading module provides separate functions for different access patterns.

| Function | Responsibility |
|---|---|
| `create_connection()` | Creates the DuckDB connection and registers datasets |
| `register_datasets()` | Registers the processed CSV files as views |
| `load_monthly_data()` | Loads monthly records into a Pandas DataFrame |
| `load_station_coordinates()` | Loads station coordinate records into a Pandas DataFrame |
| `query_hourly_data()` | Retrieves filtered hourly records |

The hourly query function supports optional filters:

- Start timestamp
- End timestamp
- Station complex ID
- Transit mode
- Row limit

SQL parameters are used for filter values rather than directly inserting user-provided values into the SQL query.

The function also rejects non-positive row limits.

This query-based approach avoids requiring the entire hourly dataset to be loaded into Pandas for every analytical operation.

## 5. Data Preparation

**Module:** `src/chronotunnel/data/preprocess.py`

The preprocessing module provides separate preparation functions for hourly and monthly data.

### 5.1 Hourly Data Preparation

Function: `prepare_hourly_data(df)`

The function:

1. Checks that the required columns are present.
2. Rejects empty input data.
3. Converts `transit_timestamp` into a datetime value.
4. Raises an error if timestamp parsing fails or produces missing datetime values.
5. Derives additional temporal attributes.
6. Sorts the records by timestamp, station complex ID, and transit mode.
7. Resets the DataFrame index.

The derived attributes include:

| Attribute | Description |
|---|---|
| `date` | Calendar date |
| `hour` | Hour of the day |
| `day_of_week` | Numeric day-of-week representation |
| `day_name` | Day name |
| `month` | Month identifier |
| `month_name` | Month name |
| `year` | Calendar year |
| `is_weekend` | Indicates Saturday or Sunday |

The original dataset columns are preserved.

### 5.2 Monthly Data Preparation

Function: `prepare_monthly_data(df)`

The function:

1. Checks the required columns.
2. Rejects empty input data.
3. Converts `month` into a datetime value.
4. Raises an error if month parsing fails or produces missing datetime values.
5. Derives year and month attributes.
6. Sorts records by month, station complex ID, and transit mode.
7. Resets the DataFrame index.

The derived attributes are:

- `year`
- `month_number`
- `month_name`

The original monthly dataset columns are preserved.

## 6. Data Validation

**Module:** `src/chronotunnel/data/validate.py`

ChronoTunnel performs data quality checks before starting the analytical stages.

Function: `run_data_validation(connection)`

The validation process uses DuckDB SQL queries and returns a Pandas DataFrame containing the check name, status, actual result, and expected result.

### 6.1 Validation Categories

| Category | Validation |
|---|---|
| Required columns | Checks required columns in all three datasets |
| Missing values | Checks required fields for null values |
| Negative values | Checks hourly and monthly ridership and transfer values |
| Coordinate ranges | Checks latitude and longitude against valid geographic ranges |
| Duplicate records | Checks duplicate analytical groups |
| Coordinate coverage | Checks that hourly and monthly station-mode combinations exist in the coordinate dataset |
| Temporal coverage | Checks the expected number of hourly dates and monthly periods |

### 6.2 Analytical Uniqueness

The validation process checks uniqueness at the appropriate analytical grain.

| Dataset | Analytical Key |
|---|---|
| Hourly | `transit_timestamp`, `transit_mode`, `station_complex_id` |
| Monthly | `month`, `transit_mode`, `station_complex_id` |
| Station coordinates | `station_complex_id`, `transit_mode` |

Station identity is represented by the combination of `station_complex_id` and `transit_mode`, rather than station ID alone.

### 6.3 Expected Temporal Coverage

The current configuration defines:

- 120 sampled hourly dates
- 60 monthly periods
- 428 expected stations

The validation module checks hourly date coverage and monthly period coverage against the expected values.

### 6.4 Validation Statuses

Each validation check receives one of three statuses:

| Status | Meaning |
|---|---|
| `PASS` | The validation condition is satisfied |
| `FAIL` | The validation condition is not satisfied |
| `SKIPPED` | The check cannot be performed because a dependency, such as a required column, is missing |

The validation report is saved as:

`outputs/metrics/data_validation.csv`

The pipeline stops when the validation report contains a `FAIL` status. Checks marked `SKIPPED` are recorded in the report but do not independently trigger the pipeline failure condition.

## 7. Pipeline Orchestration

**Module:** `src/chronotunnel/pipeline/run.py`

The `run_pipeline()` function coordinates the complete analytical workflow.

### Stage 1 — Data Validation

- Initializes the DuckDB connection.
- Executes the validation module.
- Saves the validation report.
- Prints the validation results.
- Stops execution if any check has a `FAIL` status.

### Stage 2 — Exploratory Data Analysis

**Module:** `src/chronotunnel/analysis/eda.py`

The exploratory analysis generates:

- Yearly ridership
- Monthly ridership trends
- Borough-level ridership
- Transit-mode ridership
- Top 15 stations

### Stage 3 — Temporal Analysis

**Module:** `src/chronotunnel/analysis/temporal.py`

The temporal analysis investigates:

- Year-over-year growth
- Monthly seasonality
- Weekday versus weekend patterns
- Peak-hour ridership concentration

### Stage 4 — Statistical Analysis

**Module:** `src/chronotunnel/analysis/statistical.py`

The statistical analysis includes:

- Ridership distribution analysis
- Borough-level statistical summaries
- Transit-mode statistical summaries
- Paired Wednesday-versus-Saturday comparison

The paired comparison evaluates differences between the selected Wednesday and Saturday observations using a Wilcoxon signed-rank test.

### Stage 5 — Geospatial Analysis

**Module:** `src/chronotunnel/analysis/geospatial.py`

The geospatial analysis generates:

- Borough-level geographic summaries
- Top 15 station locations
- Ridership-weighted geographic centroids
- Coordinate quality results

### Stage 6 — Visualization Generation

**Modules:**
- `src/chronotunnel/visualization/charts.py`
- `src/chronotunnel/visualization/maps.py`

The visualization stage generates interactive Plotly charts and geospatial HTML maps.

The current chart outputs include:

- Borough ridership
- Top 15 stations
- Hourly ridership comparison
- Monthly ridership trend

The geospatial outputs include a station map and a heatmap.

The pipeline closes the DuckDB connection in a `finally` block after execution, including when an error occurs after connection initialization.

## 8. Generated Outputs

The pipeline stores generated artifacts under the `outputs/` directory.

### 8.1 Metrics

The metrics directory contains analytical CSV and JSON outputs.

| Output | Description |
|---|---|
| `data_validation.csv` | Data quality validation results |
| `yearly_ridership.csv` | Yearly ridership totals |
| `monthly_ridership.csv` | Monthly ridership results |
| `borough_ridership.csv` | Borough-level ridership |
| `transit_mode_ridership.csv` | Transit-mode ridership |
| `top_stations.csv` | Top station results |
| `year_over_year_growth.csv` | Year-over-year growth |
| `monthly_seasonality.csv` | Monthly seasonal patterns |
| `weekday_weekend_comparison.csv` | Weekday and weekend comparison |
| `peak_hour_concentration.csv` | Peak-hour concentration |
| `ridership_distribution.csv` | Ridership distribution statistics |
| `borough_statistics.csv` | Borough-level statistical results |
| `transit_mode_statistics.csv` | Transit-mode statistical results |
| `top_locations.csv` | Top geographic locations |
| `borough_summary.csv` | Geospatial borough summary |
| `weighted_centroids.csv` | Ridership-weighted geographic centroids |
| `coordinate_quality.csv` | Coordinate quality results |
| `paired_weekday_weekend_comparison.json` | Paired statistical comparison results |

### 8.2 Figures

The figures directory contains four interactive Plotly HTML charts and the shared Plotly JavaScript dependency used by the generated HTML files.

### 8.3 Maps

The maps directory contains the generated station map and geographic heatmap as HTML files.

The map basemaps use OpenStreetMap tiles and therefore require an internet connection to display the underlying map tiles.

## 9. Running the Pipeline

Run the pipeline from the project root using the activated project virtual environment:

```powershell
python run_pipeline.py
```

The root-level script invokes the pipeline orchestrator.

A successful execution performs validation, analytical processing, and visualization generation, then reports the locations of the generated outputs.

## 10. Engineering Design Considerations

The current pipeline follows several important design principles:

- **Centralized configuration:** Dataset and output paths are defined in one settings module.
- **Separation of concerns:** Loading, preprocessing, validation, analysis, visualization, and orchestration are maintained in separate modules.
- **Query-based data access:** DuckDB supports filtered hourly queries without requiring the full hourly dataset to be loaded into Pandas.
- **Parameterized filtering:** Hourly query filters use SQL parameters.
- **Explicit validation:** Data quality checks run before analytical processing.
- **Reproducible outputs:** Analytical results are written to structured output directories.
- **Resource management:** The DuckDB connection is closed after pipeline execution.
- **Failure visibility:** Invalid data and pipeline failures are surfaced through exceptions and validation results.

## 11. Current Pipeline Scope

The current implementation is a local, batch-oriented analytical pipeline operating on processed CSV datasets.

It does not currently implement:

- Automated scheduled ingestion
- Continuous or real-time ridership processing
- A persistent analytical database
- Distributed data processing
- Automated cloud deployment
- A production orchestration service

These capabilities are potential future extensions rather than features of the current implementation.

The pipeline provides the data engineering foundation for ChronoTunnel's exploratory analysis, statistical investigations, geospatial analysis, and interactive application.