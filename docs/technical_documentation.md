# ChronoTunnel — Technical Documentation

## 1. Overview

ChronoTunnel is an urban mobility intelligence platform for analyzing New York City subway ridership data from 2020 through 2024.

The project combines a Python-based data processing and analytical backend with an interactive Streamlit application. DuckDB provides the analytical query layer, while Pandas, NumPy, and SciPy support data preparation and statistical analysis. Plotly and Folium are used to generate interactive visualizations.

This document describes the technical environment, project organization, dependencies, setup procedure, execution commands, testing approach, and generated artifacts.

## 2. Technology Stack

### 2.1 Programming Language

- Python 3.11 or newer, as specified in `pyproject.toml`.
- Current development environment: Python 3.14.5.

### 2.2 Core Libraries

| Technology | Purpose |
|---|---|
| Pandas | Data manipulation and analytical result handling |
| NumPy | Numerical operations and statistical calculations |
| DuckDB | In-memory analytical database and SQL execution |
| SciPy | Statistical hypothesis testing |
| Plotly | Interactive charts |
| Folium | Interactive geographic maps |
| Streamlit | Interactive application and dashboard |

### 2.3 Exploratory Analysis and Geospatial Libraries

| Technology | Purpose |
|---|---|
| Matplotlib | Static data visualization |
| Seaborn | Statistical visualization |
| GeoPandas | Geospatial data workflows |
| Statsmodels | Statistical analysis and supporting analytical workflows |
| Jupyter | Interactive analytical notebooks |
| IPykernel | Python kernel support for notebooks |

### 2.4 Development and Quality Tools

| Technology | Purpose |
|---|---|
| Pytest | Automated testing |
| Pytest-cov | Test coverage reporting |
| Ruff | Python linting and formatting |
| Setuptools | Python package build configuration |
| Wheel | Python distribution packaging |

## 3. Repository Organization

The repository separates application code, analytical modules, datasets, documentation, notebooks, tests, and generated outputs.

### 3.1 Important Root-Level Files

| File | Responsibility |
|---|---|
| `pyproject.toml` | Package metadata, dependencies, build configuration, Pytest and Ruff settings |
| `requirements.txt` | Complete development environment dependencies |
| `run_pipeline.py` | Root-level data pipeline entry point |
| `README.md` | Project introduction and repository documentation |
| `.gitignore` | Excludes generated files, local environments, and non-versioned data |
| `.env.example` | Example environment configuration placeholder |

### 3.2 Source Code Organization

The main Python package is located under `src/chronotunnel/`.

| Module | Responsibility |
|---|---|
| `config/` | Central project paths and configuration |
| `data/` | Dataset loading, preprocessing, and validation |
| `analysis/` | EDA, temporal, statistical, and geospatial calculations |
| `pipeline/` | Pipeline orchestration |
| `visualization/` | Chart and map generation |
| `recommendations/` | Analytical recommendations |
| `features/` | Reserved structure for future feature engineering |
| `utils/` | Shared utility extension points |

The `features/` and `utils/` directories are extension points; they should not be interpreted as fully implemented components of the current analytical workflow.

### 3.3 Streamlit Application

The interactive application is located in `app/`.

It includes:

- `Landing.py` for the application entry point.
- `config.py` for application configuration.
- `components/` for reusable interface components.
- `pages/` for individual analytical pages.
- `assets/` for application assets.

The pages cover home, overview, temporal analysis, station analysis, borough analysis, geospatial analysis, and insights and recommendations.

### 3.4 Other Important Directories

| Directory | Responsibility |
|---|---|
| `data/raw/` | Original source datasets |
| `data/interim/` | Intermediate processing artifacts |
| `data/processed/` | Prepared analytical datasets |
| `data/external/` | Supporting external data |
| `data/metadata/` | Dataset metadata |
| `notebooks/` | Exploratory and experimental analysis |
| `tests/` | Automated tests |
| `docs/` | Technical and analytical documentation |
| `outputs/metrics/` | Tabular analytical results |
| `outputs/figures/` | Interactive charts |
| `outputs/maps/` | Geographic visualizations |
| `outputs/reports/` | Report output directory |
| `logs/` | Application and pipeline log directory |

## 4. Python Environment Setup

### 4.1 Verify Python

Open PowerShell in the project root and verify the Python installation:

```powershell
python --version
```

The project requires Python 3.11 or newer.

### 4.2 Create a Virtual Environment

Create a project-specific environment:

```powershell
python -m venv .venv
```

### 4.3 Activate the Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, use an appropriate execution-policy configuration for the current user or activate the environment using another supported terminal.

### 4.4 Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 4.5 Install Dependencies

Install the complete project development environment:

```powershell
pip install -r requirements.txt
```

The requirements file includes application dependencies, exploratory-analysis libraries, notebook support, and development tools.

### 4.6 Install the Project in Editable Mode

For development, install the project and its declared development dependencies:

```powershell
pip install -e ".[dev]"
```

This uses the package configuration in `pyproject.toml`.

The editable installation allows changes to the source package to be used without rebuilding the package after each code modification.

## 5. Dependency Configuration

ChronoTunnel maintains two dependency configuration files.

### 5.1 `pyproject.toml`

The project configuration defines:

- Package name: `chronotunnel`
- Version: `1.0.0`
- Minimum Python version: `3.11`
- Package build backend: Setuptools
- Core runtime dependencies
- Optional development dependencies
- Pytest configuration
- Ruff linting and formatting configuration

Core dependencies include Pandas, NumPy, DuckDB, Plotly, Folium, Streamlit, and SciPy.

The optional `dev` dependency group includes Pytest, Pytest-cov, Ruff, Jupyter, and IPykernel.

### 5.2 `requirements.txt`

The requirements file provides a broader installation specification.

It includes:

- Core application and data-pipeline libraries
- Exploratory analysis and notebook libraries
- Geospatial and statistical libraries
- Testing and development tools

The two files serve related but different purposes. `requirements.txt` supports full environment setup, while `pyproject.toml` defines package metadata and declared core and optional dependencies.

## 6. Data Configuration

Project-level paths and metadata are centralized in:

`src/chronotunnel/config/settings.py`

The configuration defines:

- Project root
- Data directory hierarchy
- Processed dataset paths
- Output directory paths
- Project name and tagline
- Dataset date boundaries
- Expected hourly sample size
- Expected station count

The processed analytical datasets are:

```text
data/processed/
    hourly_ridership_sample_station_level_2020_2024.csv
    monthly_ridership_station_level_2020_2024.csv
    station_coordinates.csv
```

The project uses configuration-based paths rather than scattering dataset locations throughout the analytical modules.

The current pipeline expects these processed datasets to be available at the configured paths.

## 7. Running the Data Pipeline

### 7.1 Pipeline Entry Point

The root-level execution file is:

`run_pipeline.py`

Its responsibility is to import and execute the pipeline function:

```python
from src.chronotunnel.pipeline.run import run_pipeline


if __name__ == "__main__":
    run_pipeline()
```

### 7.2 Execute the Pipeline

From the project root, with the project environment activated:

```powershell
python run_pipeline.py
```

The pipeline performs the following stages:

1. Data validation
2. Exploratory data analysis
3. Temporal analysis
4. Statistical analysis
5. Geospatial analysis
6. Visualization generation

The validation stage runs before the main analytical stages. A validation report containing a `FAIL` status stops pipeline execution.

### 7.3 Pipeline Outputs

Generated artifacts are written to the configured output directories:

```text
outputs/
    figures/
    maps/
    metrics/
    reports/
```

The metrics directory contains CSV analytical results and a JSON statistical comparison result.

The figures directory contains interactive Plotly HTML visualizations and the shared Plotly JavaScript asset.

The maps directory contains interactive geographic HTML visualizations.

Generated outputs are separate from the processed input datasets.

## 8. Running the Streamlit Application

### 8.1 Application Entry Point

The application entry point is:

`app/Landing.py`

### 8.2 Start the Application

From the project root:

```powershell
streamlit run app/Landing.py
```

Streamlit starts the local development server and provides the application URL in the terminal.

Open the displayed local URL in a browser.

### 8.3 Application Pages

The current application includes:

| Page | Purpose |
|---|---|
| Home | Main application landing and overview |
| Overview | High-level ridership indicators |
| Temporal Analysis | Time-based ridership patterns |
| Station Analysis | Station-level demand analysis |
| Borough Analysis | Borough-level comparisons |
| Geospatial Analysis | Geographic demand visualization |
| Insights & Recommendations | Interpretation and planning recommendations |

The application consumes the analytical datasets and generated results through its application and data-access components.

The pipeline and Streamlit application are separate execution entry points.

## 9. Automated Testing

ChronoTunnel uses Pytest for automated testing.

Tests are located in:

`tests/`

### 9.1 Run the Complete Test Suite

```powershell
python -m pytest -v
```

The command executes the configured test suite and displays individual test results.

### 9.2 Run a Specific Test Module

For example:

```powershell
python -m pytest tests/test_preprocessing.py -v
```

Other test modules cover data validation, pipeline behavior, and visualization functionality.

### 9.3 Generate Coverage Reports

To run tests with coverage reporting:

```powershell
python -m pytest --cov=src.chronotunnel --cov-report=term-missing
```

Coverage results help identify source-code areas not exercised by the current tests.

Passing tests demonstrate that the tested behavior satisfies the implemented test cases; they do not guarantee the absence of every possible defect.

## 10. Code Quality and Formatting

Ruff is configured in `pyproject.toml`.

The current configuration includes:

- Line length: 88 characters
- Target Python version: Python 3.11
- Error checks
- Pyflakes checks
- Import sorting
- Python upgrade checks
- Common bug-pattern checks

### 10.1 Run Linting

```powershell
ruff check .
```

### 10.2 Apply Automatic Lint Fixes

```powershell
ruff check . --fix
```

Review changes before accepting automatic fixes.

### 10.3 Check Formatting

```powershell
ruff format --check .
```

### 10.4 Apply Formatting

```powershell
ruff format .
```

Formatting should be performed and reviewed before committing source-code changes.

## 11. Jupyter Notebook Environment

The `notebooks/` directory contains exploratory analysis, statistical investigations, and validation workflows.

To start Jupyter:

```powershell
jupyter lab
```

Alternatively:

```powershell
jupyter notebook
```

The project includes Jupyter and IPykernel dependencies for notebook execution.

Notebook experiments support analytical investigation, while reusable production-oriented calculations are maintained in the `src/chronotunnel/` package.

## 12. Generated Artifact Management

ChronoTunnel distinguishes between source artifacts and generated artifacts.

### 12.1 Source Artifacts

Examples include:

- Python source files
- Application code
- Tests
- Documentation
- Configuration files
- Analytical notebooks

These are maintained as project source material.

### 12.2 Generated Artifacts

Examples include:

- Analytical CSV outputs
- Statistical JSON results
- Plotly HTML charts
- Folium HTML maps
- Shared visualization assets
- Temporary execution files

Generated outputs are written to the configured output directories.

Large datasets and generated artifacts are managed separately from ordinary source-code versioning through the repository's ignore configuration.

The exact version-control policy should be checked against `.gitignore` before preparing a release.

## 13. Execution Workflow

A typical local development workflow is:

1. Activate the project virtual environment.
2. Verify that the processed datasets are available.
3. Run the data pipeline.
4. Review the validation report and analytical outputs.
5. Start the Streamlit application.
6. Inspect the analytical pages and visualizations.
7. Run the automated test suite after code changes.
8. Run Ruff linting and formatting checks.
9. Review repository changes before committing.

The pipeline should be run successfully before relying on newly generated outputs in the application.

## 14. Current Technical Scope

The current technical implementation provides:

- A modular Python analytical package
- Configuration-driven dataset paths
- DuckDB-based analytical queries
- Data preparation and validation
- Reusable EDA, temporal, statistical, and geospatial modules
- A staged analytical pipeline
- Interactive chart and map generation
- A multi-page Streamlit interface
- Automated tests
- Notebook-based exploratory workflows

The project currently focuses on historical ridership analysis using the processed 2020–2024 datasets.

The documentation does not imply that the platform currently provides real-time transit ingestion, a continuously scheduled production pipeline, cloud deployment, or a live operational database.

## 15. Technical Documentation Summary

ChronoTunnel is organized as a modular Python application with a separate Streamlit interface and a reproducible analytical pipeline.

The configuration, data, analysis, pipeline, visualization, and recommendation modules have distinct responsibilities.

The dependency configuration supports both core application execution and the broader development environment. Pytest and Ruff provide the primary automated testing and code-quality workflows.

This structure provides a foundation for maintaining, testing, extending, and presenting ChronoTunnel as an analytical software project.