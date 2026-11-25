# ChronoTunnel — Analytical Methodology

## 1. Overview

This document describes the analytical methods used by ChronoTunnel to examine New York City subway ridership patterns from 2020 through 2024.

The methodology covers exploratory data analysis, temporal analysis, statistical comparisons, and geospatial analysis. Calculations are implemented primarily with DuckDB SQL and Python, using Pandas, NumPy, and SciPy where appropriate.

The objective is to transform station-level ridership records into interpretable measures of transit demand, temporal variation, geographic concentration, and potential planning insights.

The analysis is descriptive and exploratory. Statistical tests are used to evaluate selected differences in sampled ridership observations; they do not establish causality.

## 2. Analytical Data Sources

ChronoTunnel uses three processed datasets:

| Dataset | Analytical purpose |
|---|---|
| Hourly ridership | Sampled hourly and daily demand patterns |
| Monthly ridership | Long-term trends, station rankings, borough and transit-mode comparisons, and statistical distributions |
| Station coordinates | Geographic analysis, station ranking, borough summaries, and coordinate quality |

### 2.1 Monthly dataset

The monthly dataset contains station-level ridership observations from January 2020 through December 2024.

- 25,679 records
- 60 months of coverage
- 428 distinct station IDs
- 5-year cumulative ridership of approximately 4.80 billion

Each record represents a station-complex and transit-mode observation for a month.

### 2.2 Hourly dataset

The hourly dataset contains selected dates rather than continuous hourly observations.

- 120 selected dates
- One Wednesday and one Saturday selected per month
- Coverage from January 2020 through December 2024
- 428 distinct station IDs

The hourly dataset is used for sampled Wednesday–Saturday comparisons and hourly demand profiles.

### 2.3 Station-coordinate dataset

The station-coordinate dataset provides geographic attributes and cumulative ridership measures for station-mode records.

Station identity is interpreted using the composite key:

`station_complex_id + transit_mode`

This distinction prevents station records belonging to different transit modes from being treated as the same analytical record solely because they share a station ID.

## 3. Exploratory Data Analysis

Exploratory Data Analysis (EDA) establishes the overall ridership profile and identifies major differences across time, geography, and transit modes.

### 3.1 Overall dataset summary

The overall summary calculates:

- Total ridership
- Total transfers
- Number of distinct station IDs
- Number of boroughs
- Number of transit modes
- Number of observed months
- Average station-month ridership

Ridership and transfers are treated as separate measures. They are not added together.

### 3.2 Yearly ridership analysis

Yearly ridership is calculated by extracting the calendar year from each monthly observation and summing ridership and transfers across all station records within that year.

For year \(y\):

\[
R_y = \sum_{i \in y} r_i
\]

Where:

- \(R_y\) is total ridership in year \(y\).
- \(r_i\) is the ridership recorded in an individual monthly station observation.

This analysis describes changes in annual system-wide demand.

### 3.3 Monthly ridership trends

Monthly system-wide ridership is calculated by grouping monthly station-level observations by calendar month and summing ridership.

The resulting time series is used to examine:

- Month-to-month demand variation
- Longer-term recovery and growth patterns
- Periods of unusually high or low demand

Transfers are aggregated separately.

### 3.4 Borough comparisons

Ridership and transfers are aggregated by borough.

The analysis also counts distinct station IDs within each borough.

Borough ridership share is calculated as:

\[
S_b =
\frac{R_b}{\sum_{j=1}^{B} R_j}
\times 100
\]

Where:

- \(R_b\) is the total ridership of borough \(b\).
- \(B\) is the number of boroughs represented in the dataset.

This identifies the distribution of recorded system-wide demand across boroughs.

### 3.5 Transit-mode comparisons

The same aggregation approach is applied to transit mode.

For each mode, ChronoTunnel calculates total ridership, total transfers, and distinct station IDs.

These comparisons describe how recorded demand is distributed across the represented transit modes.

### 3.6 Top station complexes

Station-level ridership is aggregated across months using station complex ID, station name, and borough.

Station complexes are ranked by cumulative ridership.

The default EDA ranking returns the top 10 station complexes, with a configurable limit.

This ranking identifies locations with the greatest cumulative recorded demand in the monthly dataset.

### 3.7 Hourly day comparison

Hourly observations are grouped by day of week and hour.

The analysis calculates total ridership and the number of distinct sampled dates represented in each group.

This produces an overview of sampled hourly demand patterns across days of the week.

Because the hourly dataset contains selected dates, these results should not be interpreted as continuous five-year hourly coverage.

## 4. Temporal Analysis

Temporal analysis investigates annual growth, recurring monthly patterns, weekday–Saturday differences, and peak-period demand concentration.

### 4.1 Year-over-year growth

Year-over-year growth compares each month's ridership with the same calendar month in the previous year.

Monthly system-wide totals are calculated first. DuckDB's `LAG()` window function with an offset of 12 retrieves the corresponding value from twelve months earlier.

The percentage change is:

\[
G_t =
\frac{R_t - R_{t-12}}{R_{t-12}}
\times 100
\]

Where:

- \(R_t\) is ridership in the current month.
- \(R_{t-12}\) is ridership in the corresponding month of the previous year.
- \(G_t\) is the year-over-year percentage change.

A zero previous-year value is handled using `NULLIF` to avoid division by zero.

The first twelve months do not have a previous-year comparison and therefore do not produce a valid growth percentage.

### 4.2 Monthly seasonality

Monthly seasonality compares ridership for each calendar month across the available years.

For each calendar month, ChronoTunnel calculates:

- Average monthly ridership across 2020–2024
- Average monthly ridership across 2021–2024
- Minimum observed monthly ridership
- Maximum observed monthly ridership
- Number of years represented in each comparison

The 2021–2024 comparison excludes 2020 to provide an additional view that is less influenced by the exceptional disruption associated with the initial pandemic period.

This exclusion is an analytical comparison, not a statistical correction or proof that subsequent years represent normal demand.

### 4.3 Wednesday–Saturday hourly comparison

The hourly dataset is aggregated by sampled date, day of week, and hour.

The comparison includes:

- Wednesday (day-of-week value 3)
- Saturday (day-of-week value 6)

For each day type and hour, average ridership is calculated across the available sampled dates.

\[
\bar{R}_{d,h} =
\frac{1}{n_{d,h}}
\sum_{i=1}^{n_{d,h}} R_{i,d,h}
\]

Where:

- \(d\) represents the day type.
- \(h\) represents the hour.
- \(R_{i,d,h}\) is the total ridership for sampled date \(i\), day type \(d\), and hour \(h\).
- \(n_{d,h}\) is the number of sampled dates represented.

This comparison highlights differences in the hourly demand profile between sampled Wednesdays and Saturdays.

### 4.4 Peak-hour concentration

ChronoTunnel defines two analytical peak periods:

- Morning: 07:00–09:00
- Evening: 16:00–18:00

Both ranges are inclusive.

Hourly ridership is first aggregated into daily totals. Ridership within the two defined periods is then summed to calculate daily peak-period demand.

Two measures are reported.

**Ridership-weighted peak share**

\[
P_w =
\frac{\sum_i P_i}{\sum_i D_i}
\times 100
\]

**Average daily peak share**

\[
P_a =
\frac{1}{n}
\sum_{i=1}^{n}
\left(
\frac{P_i}{D_i}
\times 100
\right)
\]

Where:

- \(P_i\) is peak-period ridership on sampled date \(i\).
- \(D_i\) is total daily ridership on sampled date \(i\).
- \(n\) is the number of sampled dates.

The weighted measure gives greater influence to days with higher total ridership. The average daily measure gives each sampled date equal weight.

These measures are calculated separately for sampled Wednesdays and Saturdays.

The peak windows are project-defined analytical intervals and should not be interpreted as official MTA peak-period definitions.

## 5. Statistical Analysis

Statistical analysis combines descriptive distribution summaries with inferential comparisons of sampled Wednesday and Saturday ridership.

### 5.1 Ridership distribution

Monthly station-level ridership is summarized using:

- Observation count
- Mean
- Median
- Sample standard deviation
- Minimum and maximum
- First and third quartiles
- Skewness

The mean describes the arithmetic average, while the median describes the middle observation.

The interquartile range is:

\[
IQR = Q_3 - Q_1
\]

Skewness is used to assess distribution asymmetry.

A positive skew indicates a longer or heavier right tail, which can occur when a relatively small number of station-month observations have substantially higher ridership than the majority.

These are descriptive measures of the observed monthly station-level distribution, not measures of daily or passenger-level behavior.

### 5.2 Borough-level statistical summaries

Monthly station-level observations are grouped by borough.

For each borough, ChronoTunnel calculates:

- Observation count
- Distinct station ID count
- Mean ridership
- Median ridership
- Sample standard deviation
- Minimum ridership
- Maximum ridership

These measures help compare the distribution of station-level monthly demand across boroughs.

### 5.3 Transit-mode statistical summaries

The same descriptive statistics are calculated after grouping observations by transit mode.

This provides a distribution-level comparison rather than relying only on cumulative ridership totals.

### 5.4 Independent-sample Mann–Whitney U test

ChronoTunnel implements a two-sided Mann–Whitney U test to compare daily ridership observations from sampled Wednesdays and Saturdays.

The test uses the daily totals derived from the hourly dataset.

The samples are treated as independent groups in this implementation.

The test evaluates whether the two groups differ in their underlying distributions. It is not automatically a test of equality of means; interpretation as a difference in medians requires additional distributional assumptions.

The implementation reports:

- Wednesday sample size
- Saturday sample size
- Group means and medians
- Mann–Whitney U statistic
- p-value
- Significance level
- Statistical significance indicator

The selected significance level is:

\[
\alpha = 0.05
\]

The null hypothesis is that the two groups have the same underlying distribution.

A p-value below 0.05 is classified as statistically significant under the selected threshold.

### 5.5 Paired Wilcoxon signed-rank test

ChronoTunnel also implements a paired comparison.

Sampled Wednesday and Saturday daily totals are matched within each calendar month. Only months containing both day types are retained.

The paired difference is:

\[
D_i = W_i - S_i
\]

Where:

- \(W_i\) is sampled Wednesday ridership in month \(i\).
- \(S_i\) is sampled Saturday ridership in month \(i\).
- \(D_i\) is the paired difference.

A two-sided Wilcoxon signed-rank test is applied to the paired differences.

The test evaluates whether the paired differences are centered around zero under its assumptions.

The implementation uses SciPy's automatic method selection for the test calculation.

Months with insufficient paired observations cause the function to raise an error rather than silently produce an invalid comparison.

### 5.6 Paired effect size

The paired comparison also calculates rank-biserial correlation.

After excluding zero differences, the absolute differences are ranked. Positive and negative rank sums are used to calculate:

\[
r_{rb} =
\frac{R_+ - R_-}{R_+ + R_-}
\]

Where:

- \(R_+\) is the sum of ranks for positive differences.
- \(R_-\) is the sum of ranks for negative differences.

The value describes the direction and relative consistency of the paired differences.

A positive value indicates that Wednesday ridership tends to exceed Saturday ridership in the matched observations.

### 5.7 Confidence interval for the mean paired difference

The implementation also calculates a 95% t-based confidence interval for the mean paired difference.

\[
CI =
\bar{D}
\pm
t_{0.975,n-1}
\frac{s_D}{\sqrt{n}}
\]

Where:

- \(\bar{D}\) is the mean paired difference.
- \(s_D\) is the sample standard deviation of paired differences.
- \(n\) is the number of matched months.
- \(t_{0.975,n-1}\) is the two-sided 95% critical value from the t-distribution.

This interval estimates uncertainty around the mean paired difference. It is separate from the Wilcoxon test and does not represent a confidence interval generated by that test.

### 5.8 Interpretation of statistical significance

Statistical significance is assessed using a 0.05 threshold.

A statistically significant result indicates that the observed difference is inconsistent with the relevant null hypothesis under the test's assumptions.

It does not establish:

- A causal relationship
- The size of an operationally meaningful effect
- Generalizability to every day in the five-year period
- The absence of confounding factors or sampling effects

The independent-sample and paired analyses use different statistical designs and should be interpreted separately.

## 6. Geospatial Analysis

Geospatial analysis connects station-level demand with geographic location to identify concentrations of ridership and differences between boroughs.

### 6.1 Borough geospatial summary

The station-coordinate dataset is grouped by borough.

The analysis calculates:

- Station-mode record count
- Distinct station ID count
- Total ridership
- Average station ridership
- Borough share of total ridership

The two station counts represent different concepts. A station ID may be represented by more than one transit-mode record.

### 6.2 Top ridership locations

Station-coordinate records are ranked by cumulative ridership.

The default ranking returns the top 15 records.

The result includes station identity, transit mode, station name, borough, coordinates, cumulative ridership, and coordinate-variant count.

This geographic ranking uses the station-coordinate dataset and should be distinguished from the EDA station-complex ranking derived from monthly records.

### 6.3 Ridership-weighted borough centroids

ChronoTunnel calculates a ridership-weighted geographic center for each borough.

Weighted latitude:

\[
\phi_b =
\frac{\sum_i \phi_i R_i}{\sum_i R_i}
\]

Weighted longitude:

\[
\lambda_b =
\frac{\sum_i \lambda_i R_i}{\sum_i R_i}
\]

Where:

- \(\phi_i\) is the latitude of station record \(i\).
- \(\lambda_i\) is its longitude.
- \(R_i\) is its cumulative ridership.
- \(\phi_b\) and \(\lambda_b\) are the weighted coordinates for borough \(b\).

The resulting coordinates indicate where recorded station ridership is geographically concentrated.

They are not official geographic centroids, population centers, or exact passenger-origin locations.

### 6.4 Coordinate quality assessment

The coordinate quality analysis examines:

- Total coordinate records
- Distinct station IDs
- Distinct station-mode composite keys
- Duplicate composite-key groups
- Invalid latitude values
- Invalid longitude values
- Records with multiple coordinate variants
- Maximum coordinate-variant count

Valid geographic ranges are:

\[
-90 \leq latitude \leq 90
\]

\[
-180 \leq longitude \leq 180
\]

Coordinate variants are retained as a quality indicator rather than automatically treated as separate physical stations.

## 7. Data Interpretation and Analytical Boundaries

The analytical results must be interpreted within the structure and limitations of the underlying datasets.

### 7.1 Sampled hourly observations

The hourly dataset contains 120 selected dates, not continuous hourly observations.

Hourly and daily comparisons therefore describe the selected sample and should not be generalized automatically to every day or hour between 2020 and 2024.

### 7.2 Pandemic-period disruption

The 2020 period includes exceptional changes in public transportation demand.

For this reason, the seasonality analysis reports both a full-period average and a comparison excluding 2020.

Neither comparison removes all possible effects of pandemic-related disruptions.

### 7.3 Station identity

Station IDs alone may not uniquely represent a station-mode record.

The composite key `station_complex_id + transit_mode` is used where station-mode identity matters, particularly for coordinate coverage and duplicate checks.

### 7.4 Geographic representation

Station coordinates are representative geographic positions associated with station records.

They should not be interpreted as exact station entrances, platform locations, passenger origins, or destination points.

Ridership-weighted centroids are analytical summaries rather than official geographic boundaries or centers.

### 7.5 Descriptive versus causal conclusions

ChronoTunnel identifies patterns, associations, and differences in recorded ridership.

The analysis does not establish why a particular pattern occurred. Factors such as service changes, disruptions, weather, population movement, employment patterns, and external events are not independently controlled for in these calculations.

### 7.6 Transfers and ridership

Ridership and transfers are maintained as separate measures throughout the analytical workflow.

They should not be combined into a single passenger-demand total without a separately defined and justified methodology.

## 8. Analytical Implementation

The analytical methods are implemented in the following modules:

| Module | Responsibility |
|---|---|
| `analysis/eda.py` | Overall summaries, yearly and monthly trends, borough and mode comparisons, top stations, hourly day comparisons |
| `analysis/temporal.py` | Year-over-year growth, monthly seasonality, sampled hourly comparisons, peak-period concentration |
| `analysis/statistical.py` | Descriptive distributions, borough and mode statistics, Mann–Whitney U and paired Wilcoxon comparisons |
| `analysis/geospatial.py` | Borough geographic summaries, top locations, weighted centroids, coordinate quality |

DuckDB performs the principal data aggregation and SQL window calculations. Pandas handles returned analytical results, while NumPy and SciPy support the inferential statistical calculations.

The analytical modules return structured results for use by the pipeline, visualization layer, and downstream reporting components.

## 9. Reproducibility and Validation

The analytical workflow uses the processed datasets and shared project configuration paths.

Data validation is performed before the main pipeline analysis. It checks required columns, missing values, negative ridership and transfer values, coordinate ranges, duplicate analytical groups, coordinate coverage, and expected temporal coverage.

The validation report is saved as part of the pipeline outputs.

The pipeline stops when validation reports a `FAIL` status. Checks marked `SKIPPED` are recorded separately and do not independently trigger the current failure gate.

The statistical and analytical functions are implemented as reusable modules rather than being embedded exclusively in dashboard rendering code.

This separation supports reproducibility, testing, and future extension.

## 10. Methodology Summary

ChronoTunnel combines four analytical approaches:

1. **Exploratory analysis** establishes the overall distribution of recorded ridership across time, station complexes, boroughs, and transit modes.
2. **Temporal analysis** examines yearly growth, monthly seasonality, sampled day-type differences, and peak-period concentration.
3. **Statistical analysis** summarizes observed distributions and applies independent-sample and paired non-parametric comparisons.
4. **Geospatial analysis** examines borough-level demand, high-ridership locations, weighted geographic centers, and coordinate quality.

Together, these methods provide a reproducible analytical foundation for understanding historical NYC subway demand and supporting evidence-based mobility planning discussions.

The findings should always be interpreted in the context of the five-year monthly dataset, the selected-date hourly sample, the geographic representation of station records, and the statistical assumptions described in this document.