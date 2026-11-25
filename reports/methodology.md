# ChronoTunnel — Project Methodology

**Project:** ChronoTunnel – Urban Mobility Intelligence Platform
**Tagline:** Turning Transit Data into Smarter Mobility Decisions.
**Study Period:** January 2020 – December 2024

---

## 1. Introduction

ChronoTunnel is an urban mobility analytics project designed to examine public transit ridership patterns using historical data from the New York City Metropolitan Transportation Authority (MTA).

The project follows a structured data science workflow that transforms raw transit data into validated analytical datasets, statistical findings, and geographic visualizations.

The methodology combines:

- Data acquisition and preparation
- Data-quality validation
- Exploratory data analysis
- Temporal analysis
- Statistical hypothesis testing
- Geospatial analysis
- Interactive visualization
- Automated pipeline execution

The objective is to produce reproducible and evidence-based insights into transit demand distribution and variation over time.

## 2. Data Sources and Coverage

The project uses MTA subway ridership datasets covering January 2020 through December 2024.

Two primary datasets are used.

### 2.1 Monthly Ridership Dataset

The monthly dataset contains station-level ridership and transfer measurements across 60 months.

It supports:

- Long-term ridership trend analysis
- Annual and monthly comparisons
- Borough-level demand analysis
- Transit-mode comparisons
- Station-level aggregation

### 2.2 Hourly Ridership Dataset

The hourly dataset contains station-level hourly observations for 120 selected dates.

The sampling design includes:

- One Wednesday per month
- One Saturday per month
- 60 sampled Wednesdays
- 60 sampled Saturdays

The selected dates fall between the 10th and 20th of each month.

This dataset supports comparisons of hourly demand patterns, weekday-versus-weekend differences, and peak-period concentration.

It is important to distinguish this selected sample from a continuous hourly time series.

### 2.3 Station Coordinate Dataset

A station coordinate reference dataset provides geographic information used to associate station-level ridership with locations.

It contains 429 station-mode coordinate records representing 428 unique station IDs.

The composite key of `station_complex_id` and `transit_mode` is retained when matching station coordinates to ridership records.

This avoids incorrectly merging distinct transit-mode records that share a station ID.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical operations |
| DuckDB | Analytical SQL queries |
| SciPy | Statistical hypothesis testing |
| Statsmodels | Statistical analysis support |
| Matplotlib | Data visualization support |
| Seaborn | Statistical visualization support |
| Plotly | Interactive charts |
| Folium | Interactive geographic maps |
| GeoPandas | Geospatial data processing support |
| Streamlit | Planned interactive application layer |
| Pytest | Testing support |

The analytical pipeline primarily uses Python, Pandas, DuckDB, SciPy, Plotly, and Folium.

## 4. Project Architecture

The project follows a modular structure that separates data processing, analysis, visualization, and reporting.

```text
ChronoTunnel/
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ raw/
â”‚   â”œâ”€â”€ interim/
â”‚   â”œâ”€â”€ processed/
â”‚   â”œâ”€â”€ external/
â”‚   â””â”€â”€ metadata/
â”‚
â”œâ”€â”€ notebooks/
â”‚
â”œâ”€â”€ src/
â”‚   â””â”€â”€ chronotunnel/
â”‚       â”œâ”€â”€ config/
â”‚       â”œâ”€â”€ data/
â”‚       â”œâ”€â”€ features/
â”‚       â”œâ”€â”€ analysis/
â”‚       â”œâ”€â”€ visualization/
â”‚       â”œâ”€â”€ recommendations/
â”‚       â”œâ”€â”€ pipeline/
â”‚       â””â”€â”€ utils/
â”‚
â”œâ”€â”€ scripts/
â”‚
â”œâ”€â”€ app/
â”‚
â”œâ”€â”€ outputs/
â”‚   â”œâ”€â”€ figures/
â”‚   â”œâ”€â”€ maps/
â”‚   â”œâ”€â”€ metrics/
â”‚   â””â”€â”€ reports/
â”‚
â”œâ”€â”€ reports/
â”‚   â”œâ”€â”€ findings.md
â”‚   â”œâ”€â”€ methodology.md
â”‚   â””â”€â”€ final_report.md
â”‚
â”œâ”€â”€ tests/
â”œâ”€â”€ requirements.txt
â””â”€â”€ run_pipeline.py
```

Each module has a specific responsibility:

- `config/`: Centralized project paths and settings.
- `data/`: Dataset loading, validation, and preprocessing.
- `features/`: Feature engineering.
- `analysis/`: Exploratory, temporal, statistical, and geospatial analysis.
- `visualization/`: Charts and geographic maps.
- `pipeline/`: Integration and execution of analytical stages.
- `outputs/`: Generated analytical results and visualizations.
- `reports/`: Documentation of findings and methodology.

## 5. Data Loading

DuckDB is used as the analytical query engine.

The loading module:

1. Establishes an in-memory DuckDB connection.
2. Checks whether the required processed datasets exist.
3. Registers the hourly, monthly, and station coordinate datasets as queryable views.
4. Provides functions to retrieve monthly data, coordinate data, and filtered hourly records.

The datasets are accessed through SQL queries, allowing analytical operations to be performed without repeatedly loading entire files into memory.

The project preserves station identifiers as strings to avoid unintended changes to identifier values.

## 6. Data Preprocessing

Preprocessing is performed using Pandas.

### 6.1 Hourly Data Preparation

The hourly preprocessing function:

- Converts transit timestamps into datetime values.
- Extracts calendar dates.
- Extracts the hour of the day.
- Derives day of the week and day name.
- Extracts month number and month name.
- Extracts year.
- Creates a weekend indicator.
- Sorts records by timestamp, station ID, and transit mode.

The day-of-week encoding follows Pandas conventions:

| Value | Day |
|---:|---|
| 0 | Monday |
| 1 | Tuesday |
| 2 | Wednesday |
| 3 | Thursday |
| 4 | Friday |
| 5 | Saturday |
| 6 | Sunday |

### 6.2 Monthly Data Preparation

The monthly preprocessing function:

- Converts the monthly date field into datetime format.
- Extracts year.
- Extracts month number.
- Extracts month name.
- Sorts records chronologically and by station and transit mode.

### 6.3 Data Preservation

Preprocessing operates on copies of the input DataFrames.

The raw source datasets are not modified by the analytical workflow.

Missing hourly station records are not automatically replaced with zero because the absence of a record does not establish that ridership was zero.

## 7. Data Quality and Validation

Before analysis, ChronoTunnel executes a dedicated validation module.

The validation process checks:

- Required columns
- Missing values
- Negative ridership values
- Negative transfer values
- Invalid latitude values
- Invalid longitude values
- Duplicate analytical records
- Missing station-coordinate matches
- Number of sampled hourly dates
- Number of monthly observations

Station-coordinate matching uses the composite station ID and transit mode key.

The completed pipeline reported:

**18 validation checks passed out of 18.**

No validation failures were reported.

The validation results are exported to:

`outputs/metrics/data_validation.csv`

## 8. Exploratory Data Analysis

Exploratory analysis is conducted using DuckDB SQL aggregations.

The EDA module examines:

### 8.1 Overall Ridership

Calculates:

- Total ridership
- Total transfers
- Unique station IDs
- Number of boroughs
- Number of transit modes
- Number of months

### 8.2 Annual Ridership

Groups monthly ridership by year to examine changes in annual totals.

### 8.3 Monthly Ridership Trends

Aggregates ridership by month to identify changes over the study period.

### 8.4 Borough-Level Analysis

Groups records by borough to compare total ridership, transfers, and station counts.

### 8.5 Transit-Mode Analysis

Compares recorded ridership across subway, tram, and Staten Island Railway.

### 8.6 Highest-Ridership Stations

Aggregates ridership by station complex and identifies the highest-ridership locations.

### 8.7 Hourly Day Comparison

Compares average hourly ridership between sampled Wednesdays and Saturdays.

The results are exported as CSV files in `outputs/metrics/`.

## 9. Temporal Analysis

The temporal module examines how recorded ridership varies over time.

### 9.1 Year-over-Year Growth

Monthly year-over-year growth is calculated using:

\[
Growth(\%) =
\frac{R_t-R_{t-12}}{R_{t-12}}\times100
\]

Where:

- \(R_t\) is ridership in the current month.
- \(R_{t-12}\) is ridership in the same month of the previous year.

The first 12 months do not have a previous-year comparison.

### 9.2 Monthly Seasonality

Average monthly ridership is calculated across the study period.

The analysis also examines monthly averages excluding 2020 to reduce the influence of the unusually low ridership observations during that year.

These averages are descriptive and remain influenced by changes in annual ridership levels.

They are not treated as isolated seasonal effects.

### 9.3 Weekday and Weekend Comparison

Hourly observations are grouped by day of the week and hour.

For each hour, ridership is normalized by the number of sampled dates for the corresponding day.

This ensures that the Wednesday and Saturday hourly profiles are compared using their respective 60 sampled dates.

### 9.4 Peak-Period Concentration

Two analytical time windows are defined:

- Morning peak: 07:00–09:00
- Evening peak: 16:00–18:00

Peak-period ridership is calculated by aggregating observations within these windows.

Two measures are considered:

**Ridership-weighted peak share**

\[
\frac{\text{Total peak-period ridership}}
{\text{Total daily ridership}}\times100
\]

**Average daily peak share**

First, the peak share is calculated separately for each sampled date. The resulting daily percentages are then averaged.

These measures describe the concentration of recorded ridership within the selected time windows.

The selected windows are analytical definitions rather than verified official MTA peak-period definitions.

## 10. Statistical Analysis

Statistical analysis is used to evaluate differences and distributions in the ridership data.

### 10.1 Ridership Distribution

Descriptive distribution statistics are calculated to understand the spread and characteristics of station-level ridership observations.

### 10.2 Borough Statistics

Ridership statistics are calculated for individual boroughs to compare their distribution and average station-level demand.

### 10.3 Transit-Mode Statistics

Descriptive statistics are calculated separately for each transit mode.

### 10.4 Paired Wednesday–Saturday Comparison

The hourly sample contains one Wednesday and one Saturday observation date per month.

Since both observations belong to the same month, they are treated as matched monthly observations.

The paired comparison follows these steps:

1. Aggregate hourly ridership across stations for each sampled date.
2. Group observations by month and day of the week.
3. Match Wednesday and Saturday totals within each month.
4. Retain months containing both sampled days.
5. Calculate paired differences.
6. Apply the Wilcoxon signed-rank test.

The Wilcoxon signed-rank test is selected because it evaluates paired observations without requiring the paired differences to follow a normal distribution.

The analysis also calculates:

- Mean paired difference
- Median paired difference
- 95% confidence interval for the mean paired difference
- Wilcoxon test statistic
- p-value
- Rank-biserial correlation

The confidence interval is calculated using a paired t-based approximation. It is reported separately from the nonparametric Wilcoxon hypothesis test.

A significance threshold of 0.05 is used.

The results apply to the 60 matched sampled months and are not automatically generalizable to every Wednesday and Saturday in the study period.

## 11. Geospatial Analysis

Geospatial analysis associates station-level ridership with geographic coordinates.

The process includes:

1. Matching station ridership records with station coordinate records.
2. Retaining transit mode in the matching key.
3. Aggregating ridership by geographic location.
4. Identifying high-ridership station locations.
5. Calculating borough-level ridership summaries.
6. Calculating ridership-weighted borough centroids.
7. Evaluating coordinate quality.

### 11.1 Ridership-Weighted Centroids

Borough centroids are calculated using station coordinates weighted by recorded ridership.

The weighted coordinates represent analytical centers of recorded station ridership.

They are not equivalent to population-weighted geographic centers or actual passenger origins.

### 11.2 Geographic Visualization

Folium is used to generate:

- Station ridership map
- Ridership heatmap

Station markers are scaled according to recorded ridership.

The maps use representative station coordinates, not exact station entrance locations.

## 12. Visualization

ChronoTunnel generates interactive visualizations to make the analytical results easier to explore.

### Plotly Charts

The chart module generates:

- Borough ridership chart
- Top-station ridership chart
- Hourly ridership comparison
- Monthly ridership trend

### Folium Maps

The map module generates:

- Station ridership map
- Ridership heatmap

The generated HTML files can be opened in a web browser.

## 13. Automated Pipeline

The analytical workflow is integrated into a single pipeline.

The entry point is:

`run_pipeline.py`

Execution command:

```powershell
cd D:\ChronoTunnel
python run_pipeline.py
```

The pipeline performs six main stages:

1. Initialize directories and establish the analytical database connection.
2. Validate the input datasets.
3. Execute exploratory data analysis.
4. Execute temporal analysis.
5. Execute statistical and geospatial analysis.
6. Export metrics and generate charts and maps.

If validation detects a failure, the pipeline stops rather than proceeding with potentially invalid data.

The database connection is closed after execution.

### Generated Outputs

| Output Directory | Contents |
|---|---|
| `outputs/metrics/` | Analytical CSV and JSON results |
| `outputs/figures/` | Interactive Plotly charts |
| `outputs/maps/` | Interactive Folium maps |

The pipeline was executed successfully, with all 18 validation checks passing.

## 14. Reproducibility

To reproduce the analytical workflow:

1. Use Python with the project dependencies installed.
2. Place the required processed datasets in `data/processed/`.
3. Verify that the configured dataset paths exist.
4. Run the pipeline from the project root directory.

```powershell
cd D:\ChronoTunnel
python run_pipeline.py
```

The dependencies are listed in `requirements.txt`.

The pipeline generates analytical outputs in the configured output directories.

For consistent reproduction, the source datasets, Python environment, and project code should be maintained together.

## 15. Methodological Limitations

The methodology has several limitations:

- The hourly dataset is based on selected dates rather than continuous daily coverage.
- Only Wednesday and Saturday are included in the hourly comparison.
- The analysis does not contain complete passenger journey information.
- Train frequency, capacity, occupancy, and service disruption information are not included.
- Missing station-hour records are not assumed to represent zero ridership.
- Historical trends do not establish causal explanations.
- Coordinate records represent analytical station locations rather than exact passenger locations.
- Monthly seasonal averages may be influenced by changes in annual ridership levels.

These limitations define the scope of conclusions that can reasonably be drawn from the current datasets.

## 16. Conclusion

ChronoTunnel uses a modular and reproducible analytical workflow to transform public transit ridership datasets into structured mobility insights.

By integrating SQL-based data processing, statistical analysis, temporal comparisons, and geospatial visualization, the project demonstrates a practical application of data science to urban mobility.

The methodology establishes a foundation for future extensions involving predictive modeling, demand forecasting, and integration of additional transit operations data.

---

**ChronoTunnel — Turning Transit Data into Smarter Mobility Decisions.**
