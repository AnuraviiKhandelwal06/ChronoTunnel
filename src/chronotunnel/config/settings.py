from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------

# settings.py -> config -> chronotunnel -> src -> ChronoTunnel
PROJECT_ROOT = Path(__file__).resolve().parents[3]


# --------------------------------------------------
# DATA DIRECTORIES
# --------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
METADATA_DIR = DATA_DIR / "metadata"


# --------------------------------------------------
# PROCESSED DATASETS
# --------------------------------------------------

HOURLY_DATA_PATH = (
    PROCESSED_DATA_DIR / "hourly_ridership_sample_station_level_2020_2024.csv"
)

MONTHLY_DATA_PATH = PROCESSED_DATA_DIR / "monthly_ridership_station_level_2020_2024.csv"

STATION_COORDINATES_PATH = PROCESSED_DATA_DIR / "station_coordinates.csv"


# --------------------------------------------------
# OUTPUT DIRECTORIES
# --------------------------------------------------

OUTPUTS_DIR = PROJECT_ROOT / "outputs"

FIGURES_DIR = OUTPUTS_DIR / "figures"
MAPS_DIR = OUTPUTS_DIR / "maps"
METRICS_DIR = OUTPUTS_DIR / "metrics"
REPORTS_DIR = OUTPUTS_DIR / "reports"


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

PROJECT_NAME = "ChronoTunnel"

PROJECT_TAGLINE = "Turning Transit Data into Smarter Mobility Decisions."

DATA_START_DATE = "2020-01-01"
DATA_END_DATE = "2024-12-31"

HOURLY_SAMPLE_DAYS = 120
EXPECTED_STATIONS = 428
