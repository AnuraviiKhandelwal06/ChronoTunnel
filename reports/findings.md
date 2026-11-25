# ChronoTunnel — Analytical Findings Report

**Project:** ChronoTunnel – Urban Mobility Intelligence Platform
**Tagline:** Turning Transit Data into Smarter Mobility Decisions.
**Study Period:** January 2020 – December 2024
**Data Source:** MTA Subway Hourly Ridership and Monthly Ridership Data

---

## 1. Executive Summary

ChronoTunnel analyzes New York City's public transit ridership patterns between 2020 and 2024 to identify changes in demand, geographic concentration, temporal travel patterns, and station-level activity.

The analysis reveals that:

- Total annual ridership increased by approximately 88.2% between 2020 and 2024.
- Manhattan accounts for approximately 53.65% of recorded ridership.
- Times Sq–42 St is the highest-ridership station complex in the dataset.
- Sampled Wednesdays demonstrate higher average daily ridership than sampled Saturdays.
- Peak-period ridership represents a larger share of Wednesday demand than Saturday demand.
- Paired statistical testing identifies a significant difference between Wednesday and Saturday ridership across the 60 matched months.

These findings provide an evidence-based overview of transit demand distribution and temporal variation.

## 2. Dataset Overview

The analysis uses two MTA datasets covering January 2020 through December 2024.

| Dataset | Records | Coverage |
|---|---:|---|
| Monthly ridership | 25,679 | 60 months |
| Hourly ridership sample | 1,172,916 | 120 selected dates |
| Station coordinates | 429 | 428 unique station IDs |

The monthly dataset provides coverage across all 60 months.

The hourly dataset is a selected sample containing one Wednesday and one Saturday from each month, giving 60 sampled dates for each day of the week.

The analysis covers 428 unique station IDs and three transit modes.

**Important:** The hourly dataset is a sample, not a continuous hourly record covering every day of the five-year period.

## 3. Overall Ridership Trends

Total recorded ridership during the study period was approximately **4.803 billion**.

### Annual ridership

| Year | Total Ridership | Annual Growth |
|---|---:|---:|
| 2020 | 643.31 million | — |
| 2021 | 763.91 million | 18.7% |
| 2022 | 1.021 billion | 33.6% |
| 2023 | 1.163 billion | 14.0% |
| 2024 | 1.212 billion | 4.1% |

Between 2020 and 2024, annual ridership increased by approximately **88.2%**.

The strongest year-over-year increase occurred in 2022, followed by slower growth in 2023 and 2024.

This indicates that the rate of annual ridership growth moderated toward the end of the study period.

These figures describe changes in recorded ridership and do not independently establish the reasons behind those changes.

### Monthly year-over-year observations

Monthly comparisons reveal substantial variation:

- April 2021 recorded approximately 343.94% year-over-year growth, partly reflecting the unusually low April 2020 comparison base.
- Most months in 2022 recorded positive year-over-year growth.
- Growth moderated considerably during 2023.
- In 2024, monthly growth ranged from approximately -0.88% to 8.89%.

The comparison demonstrates why monthly year-over-year growth should be interpreted alongside the underlying monthly ridership totals.

## 4. Borough-Level Ridership Distribution

Ridership is unevenly distributed across New York City's five boroughs.

| Borough | Total Ridership | Ridership Share |
|---|---:|---:|
| Manhattan | 2,576,696,612 | 53.65% |
| Brooklyn | 1,098,172,665 | 22.87% |
| Queens | 734,785,978 | 15.30% |
| Bronx | 384,162,750 | 8.00% |
| Staten Island | 8,846,915 | 0.18% |

### Key observations

**Manhattan dominates recorded ridership.**

More than half of all recorded ridership is associated with Manhattan stations.

**Brooklyn represents the second-largest share.**

Brooklyn contributes approximately 22.87% of total ridership.

**Queens has a substantial recorded transfer volume.**

Queens records approximately 69.48 million transfers, the highest absolute transfer total among the boroughs.

**Staten Island contributes a relatively small share.**

Its recorded ridership represents approximately 0.18% of the systemwide total.

These results describe the distribution of recorded station ridership. They should not be interpreted as direct measurements of borough population, passenger origins, or complete passenger journeys.

## 5. Transit Mode Analysis

The dataset contains three transit modes.

| Transit Mode | Total Ridership |
|---|---:|
| Subway | 4,783,143,149 |
| Tram | 10,674,858 |
| Staten Island Railway | 8,846,913 |

The subway accounts for approximately 99.6% of total recorded ridership.

This indicates that the analyzed ridership volume is overwhelmingly concentrated in the subway mode.

The relatively small volumes for tram and Staten Island Railway should be considered when comparing their results with the subway.

## 6. Highest-Ridership Station Complexes

The ten highest-ridership station complexes are:

| Rank | Station Complex | Borough | Total Ridership |
|---:|---|---|---:|
| 1 | Times Sq–42 St | Manhattan | 168,202,157 |
| 2 | Grand Central–42 St | Manhattan | 115,353,629 |
| 3 | 34 St–Herald Sq | Manhattan | 97,401,047 |
| 4 | 14 St–Union Sq | Manhattan | 86,561,174 |
| 5 | Fulton St | Manhattan | 70,686,291 |
| 6 | 34 St–Penn Station (A,C,E) | Manhattan | 68,310,948 |
| 7 | 59 St–Columbus Circle | Manhattan | 63,617,661 |
| 8 | 34 St–Penn Station (1,2,3) | Manhattan | 62,794,521 |
| 9 | 74-Broadway/Jackson Hts–Roosevelt Av | Queens | 58,200,078 |
| 10 | Flushing–Main St | Queens | 57,024,065 |

### Key observations

- Eight of the ten highest-ridership station records are in Manhattan.
- Times Sq–42 St ranks first, with approximately 168.2 million recorded rides.
- Grand Central–42 St ranks second.
- Queens also has two station complexes among the top ten.

The results highlight the concentration of recorded demand around a small number of high-ridership station complexes.

## 7. Temporal Ridership Patterns

The hourly dataset provides a comparison of sampled Wednesdays and Saturdays.

### Wednesday pattern

The highest hourly ridership observations occur at:

- 08:00 — approximately 306,798 rides.
- 17:00 — approximately 318,900 rides.

The hourly profile shows pronounced morning and evening peaks.

### Saturday pattern

Saturday ridership follows a more gradual daytime pattern.

- Ridership increases through the morning.
- The highest hourly observation occurs at 16:00, with approximately 158,475 rides.
- The afternoon and early evening contain much of the observed daytime demand.

These patterns indicate differences in the hourly distribution of sampled ridership between the two days.

They do not independently establish the purpose of individual journeys.

## 8. Peak-Period Concentration

For this analysis, peak periods were defined as:

- Morning: 07:00–09:00
- Evening: 16:00–18:00

These are analytical time windows selected for comparison, not a claim that they represent an official MTA peak-period definition.

| Metric | Wednesday | Saturday |
|---|---:|---:|
| Sampled dates | 60 | 60 |
| Average daily ridership | 3,208,250.73 | 2,003,929.13 |
| Average peak-period ridership | 1,579,610.35 | 673,256.30 |
| Average daily peak share | 48.31% | 33.83% |
| Ridership-weighted peak share | 49.24% | 33.60% |

### Key finding

The average daily peak-period share is approximately **14.48 percentage points higher on Wednesday** than on Saturday.

This indicates that sampled Wednesday ridership is more concentrated in the selected morning and evening windows.

Saturday demand is comparatively more distributed across the day.

## 9. Statistical Comparison: Wednesday vs Saturday

Because the hourly dataset contains one Wednesday and one Saturday sample in each month, the analysis uses paired monthly comparisons.

A Wilcoxon signed-rank test was applied to the 60 matched monthly observations.

### Statistical results

| Metric | Result |
|---|---:|
| Matched months | 60 |
| Mean Wednesday ridership | 3,208,250.73 |
| Mean Saturday ridership | 2,003,929.13 |
| Mean paired difference | 1,204,321.60 |
| Median paired difference | 1,220,108.50 |
| 95% confidence interval for mean difference | 1,059,597.40–1,349,045.80 |
| Wilcoxon statistic | 0.0 |
| p-value | 1.63 × 10⁻¹¹ |
| Rank-biserial correlation | 1.00 |

### Interpretation

The p-value is substantially below the conventional 0.05 significance threshold.

All 60 matched monthly differences were positive, meaning sampled Wednesday ridership exceeded sampled Saturday ridership in every matched month.

The result provides strong statistical evidence of a difference between the sampled Wednesday and Saturday observations.

**Scope limitation:** This result applies to the selected dates and sampling design. It should not be generalized automatically to every Wednesday and Saturday throughout the five-year period.

The confidence interval is based on a paired t approximation, while the hypothesis test itself is nonparametric.

## 10. Geospatial Findings and Coordinate Quality

The geographic analysis associates station ridership with representative station coordinates.

Coordinate validation produced the following results:

| Quality Check | Result |
|---|---:|
| Coordinate records | 429 |
| Unique station IDs | 428 |
| Unique station-mode combinations | 429 |
| Duplicate station-mode groups | 0 |
| Invalid latitude records | 0 |
| Invalid longitude records | 0 |
| Records with multiple coordinate variants | 27 |
| Maximum coordinate variants | 8 |

### Key observations

- No invalid latitude or longitude values were identified.
- No duplicate station-mode coordinate groups were found.
- Some station IDs have multiple coordinate variants.
- The coordinate analysis retains transit mode as part of the station matching key.

The generated maps use representative coordinates for visualization. These should not be treated as exact station entrances or precise passenger locations.

Borough-weighted centroids are analytical centers of recorded station ridership, not necessarily geographic or population centers.

## 11. Key Insights and Opportunities

The combined findings suggest several areas for further investigation.

### 1. High-demand station monitoring

Times Sq–42 St, Grand Central–42 St, and other leading station complexes represent important locations for deeper demand analysis.

Future work could examine their hourly, monthly, and borough-level patterns.

### 2. Borough-level demand analysis

Manhattan's large share of recorded ridership suggests that borough-level comparisons should be an important part of transit planning analysis.

Future analysis could examine how demand varies across individual station complexes within each borough.

### 3. Time-specific demand analysis

The difference in peak-period concentration between sampled Wednesdays and Saturdays suggests that temporal demand profiles should be considered when evaluating service requirements.

### 4. Better operational data integration

Combining ridership with train frequency, service disruptions, passenger capacity, and station-level operational data would support more detailed operational analysis.

### 5. Expanded temporal analysis

A continuous hourly dataset would enable stronger analysis of daily, weekly, seasonal, and long-term hourly patterns.

These are opportunities for further research, not conclusions about existing service inadequacy.

## 12. Limitations of the Analysis

The following limitations should be considered when interpreting the findings:

1. **Hourly sampling:** Hourly observations cover 120 selected dates, not every day from 2020 to 2024.

2. **Selected weekdays:** The hourly comparison uses one Wednesday and one Saturday per month, selected between the 10th and 20th.

3. **No complete journey information:** Ridership counts do not identify complete passenger journeys, origins, destinations, or unique passengers.

4. **No capacity measurements:** The dataset does not directly measure train capacity, station occupancy, crowding, or passenger density.

5. **Transfer interpretation:** Transfers are already included in the recorded ridership measure. They must not be added to ridership as a separate passenger count.

6. **Missing hourly observations:** An absent station-hour record should not automatically be interpreted as zero ridership.

7. **No causal inference:** Observed trends do not independently establish the reasons behind ridership changes.

8. **Coordinate precision:** Representative station coordinates are suitable for analytical mapping but are not exact entrance locations.

9. **Peak-period definition:** The selected peak windows are analytical definitions and should not be presented as verified official MTA definitions.

## 13. Conclusion

ChronoTunnel demonstrates how public transit datasets can be transformed into an integrated analytical workflow covering data validation, exploratory analysis, temporal comparisons, statistical testing, and geospatial visualization.

The analysis identifies substantial changes in annual ridership, uneven borough-level demand distribution, high-ridership station complexes, and distinct sampled weekday and weekend patterns.

By combining descriptive statistics, paired hypothesis testing, and geographic analysis, ChronoTunnel moves beyond basic ridership reporting toward a more structured understanding of urban mobility patterns.

The findings provide a foundation for future predictive modeling, demand forecasting, and evidence-based transit planning research.

---

**ChronoTunnel — Turning Transit Data into Smarter Mobility Decisions.**