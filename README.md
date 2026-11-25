# ChronoTunnel

### Turning Transit Data into Smarter Mobility Decisions

ChronoTunnel is an urban mobility intelligence platform that analyzes New York City subway ridership data to uncover temporal trends, station-level demand patterns, borough-level differences, and geographic concentrations.

Built with Python, Pandas, DuckDB, and Streamlit, the platform combines reproducible data processing, statistical analysis, geospatial intelligence, and interactive visualizations to support data-informed transportation planning.

---

## Project Overview

ChronoTunnel uses historical NYC MTA subway ridership data covering January 2020 through December 2024.

The platform explores how ridership varies across time, stations, boroughs, and transit modes, transforming raw transportation data into structured analytical outputs and decision-support insights.

## Key Capabilities

- **Data Engineering:** Structured data loading, preprocessing, validation, and analytical querying.
- **Ridership Analytics:** Station, borough, transit-mode, and yearly ridership analysis.
- **Temporal Intelligence:** Monthly trends, seasonal patterns, weekday comparisons, and peak-hour concentration.
- **Statistical Analysis:** Distribution analysis, hypothesis testing, effect-size measurement, and confidence intervals.
- **Geospatial Intelligence:** Station-level mapping, borough summaries, and ridership-weighted geographic analysis.
- **Interactive Exploration:** Streamlit application for exploring analytical results.
- **Decision Support:** Evidence-based insights and recommendations derived from historical demand patterns.

## Dataset

The project uses the NYC MTA Subway Hourly Ridership dataset.

| Attribute | Description |
|---|---|
| Source | NYC MTA / NYC Open Data |
| Dataset ID | `wujg-7c2s` |
| Historical period | January 2020 – December 2024 |
| Monthly records | 25,679 |
| Hourly sample records | 1,172,916 |
| Selected hourly dates | 120 |
| Station identifiers | 428 |

**Official dataset:** [MTA Subway Hourly Ridership – NYC Open Data](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/wujg-7c2s)

### Dataset Organization

The repository contains:

- **Raw data:** 120 selected-day hourly CSV files.
- **Processed data:** Hourly and monthly station-level ridership datasets and station coordinates.
- **Metadata:** Dataset information and extraction records.

The large processed hourly dataset is stored using Git Large File Storage (Git LFS).

**Important data consideration:** The hourly dataset is a sample containing one Wednesday and one Saturday per month. It is not a continuous five-year hourly record. Monthly data provides broader temporal coverage. Refer to the limitations documentation before interpreting results.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Analytical Querying | DuckDB |
| Statistical Analysis | SciPy, Statsmodels |
| Visualization | Plotly, Matplotlib, Seaborn |
| Geospatial Analysis | GeoPandas, Folium |
| Application | Streamlit |
| Testing | Pytest, pytest-cov |
| Code Quality | Ruff |
| Notebooks | Jupyter, IPython |

## Repository Structure

```text
ChronoTunnel/
├── app/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   └── Landing.py
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── external/
│   └── metadata/
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── data_pipeline.md
│   ├── methodology.md
│   ├── technical_documentation.md
│   ├── limitations.md
│   └── README.md
├── logs/
├── notebooks/
├── outputs/
│   ├── figures/
│   ├── maps/
│   ├── metrics/
│   └── reports/
├── reports/
├── scripts/
├── src/
│   └── chronotunnel/
│       ├── analysis/
│       ├── config/
│       ├── data/
│       ├── features/
│       ├── pipeline/
│       ├── recommendations/
│       ├── utils/
│       └── visualization/
├── tests/
├── .gitattributes
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── run_pipeline.py
```

`data/interim/` is reserved for reproducible intermediate artifacts and is excluded from version control.

## Getting Started

### 1. Prerequisites

- Python 3.11 or later
- Git
- Git LFS
- A Windows, macOS, or Linux development environment

### 2. Clone the Repository

```bash
git clone https://github.com/AnuraviiKhandelwal06/ChronoTunnel.git
cd ChronoTunnel
```

### 3. Retrieve Large Dataset Files

ChronoTunnel uses Git LFS for the large processed hourly dataset.

Install Git LFS if it is not already installed:

```bash
git lfs install
```

Retrieve the LFS-managed dataset:

```bash
git lfs pull
```

Verify that the hourly CSV has been downloaded rather than remaining an LFS pointer file.

### 4. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 5. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project with development dependencies:

```bash
pip install -e ".[dev]"
```

Alternatively, install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 6. Verify Dataset Availability

Ensure that the following files exist in `data/processed/`:

```text
hourly_ridership_sample_station_level_2020_2024.csv
monthly_ridership_station_level_2020_2024.csv
station_coordinates.csv
```

The project uses centralized dataset paths defined in:

`src/chronotunnel/config/settings.py`

The pipeline checks dataset availability before registration and raises an error if a required file is missing.

## Running ChronoTunnel

### Execute the Data Pipeline

From the project root:

```bash
python run_pipeline.py
```

The pipeline performs:

1. Data loading and validation
2. Exploratory data analysis
3. Temporal analysis
4. Statistical analysis
5. Geospatial analysis
6. Visualization generation

Generated analytical artifacts are stored in the configured output directories.

### Launch the Streamlit Application

```bash
streamlit run app/Landing.py
```

Open the local URL displayed in the terminal to explore the application.

### Run Automated Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run a specific test module:

```bash
python -m pytest tests/test_preprocessing.py -v
```

Generate a coverage report:

```bash
python -m pytest --cov=src.chronotunnel --cov-report=term-missing
```

## Generated Outputs

The analytical pipeline generates:

- CSV metrics covering ridership trends, borough summaries, station rankings, temporal patterns, statistical results, and geographic summaries.
- Interactive Plotly HTML visualizations.
- Interactive Folium station maps and geographic heatmaps.
- Data validation reports.
- A JSON report containing paired weekday–weekend statistical comparison results.

Generated artifacts are stored under:

- `outputs/metrics/`
- `outputs/figures/`
- `outputs/maps/`

## Documentation

Detailed project documentation is available in the [`docs/`](docs/) directory.

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | System architecture and component responsibilities |
| [Data Dictionary](docs/data_dictionary.md) | Dataset schemas, fields, and definitions |
| [Data Pipeline](docs/data_pipeline.md) | Data processing and pipeline execution |
| [Methodology](docs/methodology.md) | Analytical and statistical methodology |
| [Technical Documentation](docs/technical_documentation.md) | Environment, dependencies, execution, and testing |
| [Limitations](docs/limitations.md) | Data, analytical, and technical limitations |

## Analytical Scope and Limitations

ChronoTunnel is currently a historical analytics and decision-support platform.

Its findings are based on the available 2020–2024 datasets and the documented analytical methodology. The hourly dataset uses selected dates rather than continuous hourly coverage.

The platform does not currently provide real-time ridership monitoring, passenger origin-destination tracking, or validated causal estimates of transportation interventions.

Recommendations should be interpreted as analytical guidance rather than guaranteed operational outcomes.

See [Limitations and Future Improvements](docs/limitations.md) for further details.

## Project Objective

ChronoTunnel demonstrates how data engineering, statistical analysis, geospatial methods, and interactive analytics can be combined to transform public transportation data into actionable mobility intelligence.

---

**Project:** ChronoTunnel
**Domain:** Urban Mobility Intelligence
**Data Coverage:** 2020–2024
**Platform:** Python · DuckDB · Streamlit
**Focus:** Data Engineering · Data Science · Geospatial Analytics