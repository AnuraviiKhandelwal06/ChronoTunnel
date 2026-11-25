# ChronoTunnel — Data Dictionary

## 1. Overview

This document defines the structure, fields, data types, and analytical meaning of the processed datasets used by ChronoTunnel.

ChronoTunnel uses three principal datasets to analyze New York City subway ridership patterns from 2020 through 2024:

1. Hourly station-level ridership dataset.
2. Monthly station-level ridership dataset.
3. Station-coordinate reference dataset.

The datasets support temporal analysis, station and borough comparisons, statistical investigations, and geospatial visualization.

## 2. Dataset Summary

| Dataset | File | Records | Columns | Analytical Grain |
|---|---|---:|---:|---|
| Hourly Ridership | `hourly_ridership_sample_station_level_2020_2024.csv` | 1,172,916 | 10 | Timestamp × station complex × transit mode |
| Monthly Ridership | `monthly_ridership_station_level_2020_2024.csv` | 25,679 | 10 | Month × station complex × transit mode |
| Station Coordinates | `station_coordinates.csv` | 429 | 8 | Station complex × transit mode |

The hourly dataset contains 120 selected dates, consisting of one Wednesday and one Saturday per month.

The monthly dataset covers January 2020 through December 2024.

The station-coordinate dataset provides geographic reference information for station complexes represented in the processed ridership data.

## 3. Data Type Conventions

The following data types are used in the processed CSV datasets:

| Data Type | Meaning |
|---|---|
| `str` | Text or string representation of a value. |
| `int64` | 64-bit integer value. |
| `float64` | 64-bit floating-point numeric value. |

Date and time fields are currently stored as strings in the processed CSV files. They must be parsed into appropriate datetime representations when performing time-based calculations.

Latitude and longitude values are represented as floating-point numbers in decimal degrees.

## 4. Hourly Ridership Dataset

**File:** `hourly_ridership_sample_station_level_2020_2024.csv`

**Purpose:** Stores sampled hourly ridership and transfer observations for individual station complexes and transit modes.

**Analytical grain:** One record per transit timestamp, station complex, and transit mode.

### 4.1 Column Definitions

| Column | Data Type | Description |
|---|---|---|
| `transit_timestamp` | `str` | Timestamp representing the hourly observation period. |
| `transit_mode` | `str` | Transit service mode associated with the observation. |
| `station_complex_id` | `int64` | Numeric identifier assigned to the station complex. |
| `station_complex` | `str` | Name of the station complex. |
| `borough` | `str` | New York City borough associated with the station complex. |
| `latitude` | `float64` | Latitude coordinate associated with the station observation. |
| `longitude` | `float64` | Longitude coordinate associated with the station observation. |
| `ridership` | `int64` | Recorded passenger ridership for the observation period. |
| `transfers` | `int64` | Recorded transfer count for the observation period. |
| `source_coordinate_variants` | `int64` | Count of coordinate variants represented in the contributing source records. |

### 4.2 Analytical Interpretation

The hourly dataset supports:

- Hour-of-day ridership analysis.
- Weekday and weekend comparisons.
- Peak-period demand analysis.
- Station-level demand comparisons.
- Transit-mode comparisons.
- Temporal heatmaps and hourly visualizations.

The dataset is sampled rather than a complete hourly record of every day in the five-year period.

Its 120 selected dates consist of one Wednesday and one Saturday per month. Results derived from this dataset should therefore be interpreted in the context of this sampling design.

## 5. Monthly Ridership Dataset

**File:** `monthly_ridership_station_level_2020_2024.csv`

**Purpose:** Stores monthly aggregated ridership and transfer observations for individual station complexes and transit modes.

**Analytical grain:** One record per month, station complex, and transit mode.

### 5.1 Column Definitions

| Column | Data Type | Description |
|---|---|---|
| `month` | `str` | Month represented by the aggregated observation. |
| `transit_mode` | `str` | Transit service mode associated with the observation. |
| `station_complex_id` | `int64` | Numeric identifier assigned to the station complex. |
| `station_complex` | `str` | Name of the station complex. |
| `borough` | `str` | New York City borough associated with the station complex. |
| `latitude` | `float64` | Latitude coordinate associated with the station complex. |
| `longitude` | `float64` | Longitude coordinate associated with the station complex. |
| `ridership` | `int64` | Aggregated passenger ridership for the month. |
| `transfers` | `int64` | Aggregated transfer count for the month. |
| `source_rows` | `int64` | Number of source records contributing to the aggregated observation. |

### 5.2 Analytical Interpretation

The monthly dataset supports:

- Monthly and yearly ridership trends.
- Year-over-year growth analysis.
- Borough-level ridership comparisons.
- Station-level demand rankings.
- Transit-mode comparisons.
- Monthly seasonality analysis.

Unlike the sampled hourly dataset, this dataset provides monthly coverage across the full January 2020–December 2024 period.

## 6. Station Coordinates Dataset

**File:** `station_coordinates.csv`

**Purpose:** Provides geographic reference information for station complexes and transit modes represented in ChronoTunnel.

**Analytical grain:** One record per station complex and transit mode.

### 6.1 Column Definitions

| Column | Data Type | Description |
|---|---|---|
| `station_complex_id` | `int64` | Numeric identifier assigned to the station complex. |
| `transit_mode` | `str` | Transit service mode associated with the station record. |
| `station_complex` | `str` | Name of the station complex. |
| `borough` | `str` | New York City borough associated with the station complex. |
| `latitude` | `float64` | Representative latitude coordinate for the station record. |
| `longitude` | `float64` | Representative longitude coordinate for the station record. |
| `total_ridership` | `int64` | Aggregated ridership value associated with the station record, used in geographic processing. |
| `coordinate_variants` | `int64` | Count of coordinate variants associated with the station record. |

### 6.2 Analytical Interpretation

The coordinate dataset supports:

- Station-level geographic visualization.
- Ridership-weighted geographic analysis.
- Borough-level geographic summaries.
- Station location comparisons.
- Geographic quality checks.

The coordinates represent station-complex reference positions and should not be interpreted as exact station entrances or individual platform locations.

## 7. Identifiers and Record Relationships

### 7.1 Station Identity

The combination of `station_complex_id` and `transit_mode` should be used when identifying station records across the datasets.

A station complex identifier alone may not uniquely distinguish records associated with different transit modes.

### 7.2 Dataset Relationships

The datasets are related through their station identifiers and transit-mode fields.

| Dataset | Relevant Fields |
|---|---|
| Hourly Ridership | `station_complex_id`, `transit_mode` |
| Monthly Ridership | `station_complex_id`, `transit_mode` |
| Station Coordinates | `station_complex_id`, `transit_mode` |

Temporal fields provide the additional dimensions needed to distinguish observations within the hourly and monthly datasets.

## 8. Measures and Units

| Measure | Field | Interpretation |
|---|---|---|
| Ridership | `ridership` | Passenger ridership count for the relevant observation period. |
| Transfers | `transfers` | Recorded transfer count for the relevant observation period. |
| Total Ridership | `total_ridership` | Aggregated ridership value used in geographic reference processing. |
| Latitude | `latitude` | Geographic latitude in decimal degrees. |
| Longitude | `longitude` | Geographic longitude in decimal degrees. |

**Important analytical distinction:** Ridership and transfers are separate measures. They must not be added together or treated as interchangeable indicators of passenger demand.

## 9. Data Quality and Interpretation

The processed datasets are subject to validation before downstream analytical processing.

Important considerations include:

1. **Missing values:** Required fields should be checked for missing observations.
2. **Numeric validity:** Ridership, transfer, and identifier fields should contain valid numeric values.
3. **Coordinate validity:** Geographic coordinates should fall within valid latitude and longitude ranges.
4. **Record uniqueness:** Analytical records should be unique at their intended dataset grain.
5. **Station consistency:** Station identifiers and transit modes should be considered together when matching records.
6. **Temporal interpretation:** Hourly observations represent selected dates, while monthly observations cover the complete monthly period.
7. **Geographic interpretation:** Station coordinates represent station-complex locations rather than precise passenger entry points.

## 10. Known Dataset Limitations

The following limitations should be considered when interpreting analytical results:

- Hourly observations are sampled from 120 selected dates rather than representing every hour of the entire five-year period.
- The hourly sample includes one Wednesday and one Saturday per month and should not be treated as a complete representation of all weekdays and weekends.
- Monthly and hourly datasets have different temporal granularities and coverage structures.
- Coordinate values are representative station-complex positions and may not correspond to exact physical entrances.
- Station names and geographic attributes should not be used as the sole basis for record matching when station identifiers and transit modes are available.
- Statistical conclusions should account for the sampling design and assumptions of the underlying analysis.

## 11. Dataset Usage Across ChronoTunnel

| Analytical Component | Primary Dataset |
|---|---|
| Hourly and peak-period analysis | Hourly Ridership |
| Weekday and weekend comparisons | Hourly Ridership |
| Monthly and yearly trends | Monthly Ridership |
| Borough-level ridership analysis | Monthly Ridership |
| Station demand rankings | Monthly Ridership |
| Station geographic visualization | Station Coordinates |
| Ridership-weighted geographic analysis | Station Coordinates and Monthly Ridership |

The datasets are accessed through the ChronoTunnel data-access layer and used by the analytical modules and application components.

---

**Project:** ChronoTunnel
**Data Domain:** NYC Subway Ridership
**Coverage Period:** January 2020 – December 2024
**Primary Data Formats:** CSV
**Analytical Data Access:** DuckDB and Pandas