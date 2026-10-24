# Business Questions & KPI Catalog

## RD Economic & Financial Intelligence Platform

> **Business-driven analytical framework connecting economic questions, KPIs, data requirements, future Gold datasets, and dashboard outputs for the Dominican Republic.**

---

## Document Information

| Attribute | Details |
|---|---|
| **Project Name** | RD Economic & Financial Intelligence Platform |
| **Document Type** | Business Questions & KPI Catalog |
| **Document Version** | 1.0 |
| **Status** | Draft / Source Validation Pending |
| **Project Type** | Data Engineering & Business Intelligence Case Study |
| **Primary Platform** | Databricks |
| **Architecture Approach** | Lakehouse / Medallion Architecture |
| **Geographic Scope** | Dominican Republic |
| **Project Owner** | Stanly Fernandez |
| **Repository** | `rd-economic-financial-intelligence` |
| **Detailed Working File** | `03_Business_Questions_KPI_Catalog.xlsx` |

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Relationship with the Excel Workbook](#2-relationship-with-the-excel-workbook)
3. [Business-to-Data Traceability](#3-business-to-data-traceability)
4. [Analytical Domains](#4-analytical-domains)
5. [Business Questions Register](#5-business-questions-register)
6. [KPI Catalog](#6-kpi-catalog)
7. [Inflation & CPI KPIs](#7-inflation--cpi-kpis)
8. [Foreign Exchange KPIs](#8-foreign-exchange-kpis)
9. [Monetary Policy KPIs](#9-monetary-policy-kpis)
10. [Fuel Market KPIs](#10-fuel-market-kpis)
11. [International Oil KPIs](#11-international-oil-kpis)
12. [Economic Relationship KPIs](#12-economic-relationship-kpis)
13. [Consumer & Basic Basket KPIs](#13-consumer--basic-basket-kpis)
14. [Agricultural Price KPIs](#14-agricultural-price-kpis)
15. [Energy & Electricity KPIs](#15-energy--electricity-kpis)
16. [Housing & Rental KPIs](#16-housing--rental-kpis)
17. [Cross-Domain Analytical Framework](#17-cross-domain-analytical-framework)
18. [Candidate Gold Analytical Layer](#18-candidate-gold-analytical-layer)
19. [Dashboard Mapping](#19-dashboard-mapping)
20. [KPI Governance](#20-kpi-governance)
21. [Validation Status](#21-validation-status)
22. [Calculation Principles](#22-calculation-principles)
23. [Data Granularity & Dimensions](#23-data-granularity--dimensions)
24. [Source Validation Requirements](#24-source-validation-requirements)
25. [Definition of Done](#25-definition-of-done)
26. [Next Steps](#26-next-steps)

---

# 1. Purpose

The purpose of the **Business Questions & KPI Catalog** is to translate the business requirements of the **RD Economic & Financial Intelligence Platform** into measurable analytical indicators.

This document establishes the connection between:

- Business problems
- Business questions
- Key Performance Indicators (KPIs)
- Required data
- Calculation logic
- Analytical dimensions
- Expected data sources
- Future Gold datasets
- Dashboard pages
- Business insights

The catalog is intended to prevent the project from becoming a collection of disconnected datasets and dashboards.

Every major technical component should ultimately support a defined business or analytical requirement.

The project therefore follows a **business-driven data engineering approach**:

```text
Business Problem
       ↓
Business Requirement
       ↓
Business Question
       ↓
KPI
       ↓
Required Data
       ↓
Source System
       ↓
Bronze
       ↓
Silver
       ↓
Gold
       ↓
Dashboard
       ↓
Business Insight
```

---

# 2. Relationship with the Excel Workbook

The detailed working version of the KPI Catalog is maintained in:

```text
03_Business_Questions_KPI_Catalog.xlsx
```

The workbook contains four worksheets:

```text
03_Business_Questions_KPI_Catalog.xlsx
│
├── KPI_Catalog
├── Business_Questions
├── Domain_Summary
└── Definitions
```

### `KPI_Catalog`

Contains the detailed KPI-level specification, including:

- KPI ID
- Domain
- Business Question
- KPI Name
- Business Definition
- Calculation Logic
- Unit
- Granularity
- Dimensions
- Required Data
- Expected Source
- Candidate Gold Dataset
- Dashboard Page
- Priority
- Validation Status
- Notes

### `Business_Questions`

Contains the centralized register of analytical questions the platform is expected to answer.

### `Domain_Summary`

Provides a high-level view of KPI coverage across analytical domains.

### `Definitions`

Defines the governance and interpretation of the fields used throughout the catalog.

> **Important:** The Excel workbook is the detailed working catalog. This Markdown document provides a repository-friendly representation of the analytical framework and the most important KPI definitions.

---

# 3. Business-to-Data Traceability

A core design principle of this project is **traceability**.

A dataset should not be incorporated simply because it is available.

Instead, data should support a defined analytical requirement.

For example:

```text
Business Question
"How is inflation evolving in the Dominican Republic?"

                    ↓

KPIs
Monthly Inflation %
YoY Inflation %
YTD Inflation %
Core Inflation %

                    ↓

Required Data
Historical CPI observations

                    ↓

Source
Validated official/public source

                    ↓

Data Engineering
Bronze → Silver → Gold

                    ↓

Analytical Dataset
gold.inflation_metrics

                    ↓

Dashboard
Inflation & CPI

                    ↓

Business Insight
Inflation trend and category-level price pressure
```

This traceability model will be maintained throughout the project.

---

# 4. Analytical Domains

The initial analytical scope contains the following domains:

| Domain | Scope | Initial Priority |
|---|---|---|
| **Inflation & CPI** | CPI and inflation analysis | MVP |
| **Foreign Exchange** | USD/DOP and FX trends | MVP |
| **Monetary Policy** | Policy rate and inflation relationships | MVP |
| **Fuel Market** | Dominican fuel prices | MVP |
| **International Oil** | WTI and Brent | MVP |
| **Economic Relationships** | Cross-domain correlations and lag analysis | MVP / Phase 2 |
| **Consumer / Basic Basket** | Consumer-product prices | MVP |
| **Agricultural Prices** | Agricultural product prices | MVP |
| **Energy / Electricity** | Electricity tariffs and energy costs | Phase 2 / Source-dependent |
| **Housing / Rentals** | Rental and housing indicators | Phase 2 / Source-dependent |

The final scope may change following the **Data Source Assessment**.

---

# 5. Business Questions Register

## 5.1 Inflation & CPI

### BQ-001

**How is inflation evolving in the Dominican Republic?**

Related KPIs:

- CPI Index
- Monthly Inflation
- YoY Inflation
- YTD Inflation
- Core Inflation

### BQ-002

**Which expenditure groups are experiencing the greatest price changes?**

Related KPI:

- Inflation by Expenditure Group

---

## 5.2 Foreign Exchange

### BQ-003

**How is the Dominican peso performing against the U.S. dollar?**

Related KPIs:

- USD/DOP Buy Rate
- USD/DOP Sell Rate
- Daily FX Change
- MoM FX Change
- YoY FX Change
- YTD FX Change
- 30-Day Moving Average
- 52-Week High
- 52-Week Low

---

## 5.3 Monetary Policy

### BQ-004

**How has monetary policy evolved relative to inflation?**

Related KPIs:

- Monetary Policy Rate
- Policy Rate Change
- Policy Rate YTD Change
- Inflation–Policy Rate Spread
- Real Policy Rate Proxy

---

## 5.4 Fuel Market

### BQ-005

**How are fuel prices evolving in the Dominican Republic?**

Related KPIs:

- Current Fuel Price
- Previous Week Price
- Weekly Price Change
- Weekly Price Change %
- Monthly Price Change %
- YoY Price Change %
- YTD Price Change %
- 4-Week Moving Average
- 12-Week Moving Average
- 52-Week High
- 52-Week Low
- Fuel Price Volatility

---

## 5.5 International Oil

### BQ-006

**How are international oil prices evolving?**

Related KPIs:

- WTI Price
- Brent Price
- WTI WoW %
- Brent WoW %
- WTI MoM %
- Brent MoM %
- WTI 30-Day Moving Average
- Brent 30-Day Moving Average

---

## 5.6 Oil & Fuel Relationships

### BQ-007

**How do international oil prices relate to Dominican fuel prices?**

Potential analytical metrics:

- Oil/Fuel Correlation
- Oil/Fuel Lag Correlation T+1
- Oil/Fuel Lag Correlation T+2
- Oil/Fuel Lag Correlation T+4

These metrics are intended for exploratory analysis and should **not be interpreted as evidence of causality**.

---

## 5.7 Consumer & Basic Basket

### BQ-008

**Which products are contributing most to changes in household purchasing costs?**

Related KPIs:

- Average Product Price
- Median Product Price
- Minimum Product Price
- Maximum Product Price
- Product MoM %
- Product YoY %
- Product YTD %
- Product Price Volatility
- Regional Price Difference %
- Category Price Index

---

## 5.8 Agricultural Prices

### BQ-009

**Which agricultural products have experienced the greatest price changes, volatility, or seasonality?**

Related KPIs:

- Average Agricultural Price
- MoM Price Change %
- YoY Price Change %
- YTD Price Change %
- Price Volatility
- Seasonal Price Index
- Regional Price Difference %

---

## 5.9 Energy & Electricity

### BQ-010

**How are electricity and energy costs evolving?**

Related KPIs:

- Electricity Tariff
- MoM Tariff Change %
- YoY Tariff Change %
- YTD Tariff Change %
- Average Cost per kWh

> **Status:** Pending Source Validation.

---

## 5.10 Housing & Rentals

### BQ-011

**How are rental prices and housing costs evolving?**

Initial KPI:

- Median Rental Asking Price

> **Status:** Phase 2 / Pending Source Validation.

Only legally and technically appropriate data sources should be used.

---

## 5.11 Cross-Domain Analysis

### BQ-012

**How do FX movements compare with domestic inflation and selected local prices?**

Potential analysis:

- FX vs Inflation
- FX vs Fuel
- FX vs Consumer Prices
- FX vs Agricultural Prices

### BQ-013

**How is the overall cost-of-living environment changing?**

Potential inputs include:

- Inflation
- Food prices
- Fuel prices
- Electricity
- Exchange rates
- Housing
- Agricultural prices

This question represents a broader analytical objective and may be developed progressively as the required datasets become available.

---

# 6. KPI Catalog

The KPI catalog uses unique identifiers based on analytical domain.

| Prefix | Domain |
|---|---|
| `INF` | Inflation & CPI |
| `FX` | Foreign Exchange |
| `MON` | Monetary Policy |
| `FUEL` | Fuel Market |
| `OIL` | International Oil |
| `REL` | Economic Relationships |
| `CON` | Consumer / Basic Basket |
| `AGR` | Agricultural Prices |
| `ENE` | Energy / Electricity |
| `HOU` | Housing / Rentals |

Example:

```text
INF-001
│   │
│   └── Sequential KPI number
│
└────── Inflation domain
```

This naming convention provides stable identifiers that can be referenced across documentation, code, tests, dashboards, and data-quality rules.

---

# 7. Inflation & CPI KPIs

**Validation status:** Validated (2026-10-23) against the official BCRD CPI workbooks (base October 2019 – September 2020 = 100). Calculated values are stored in `gold.inflation_metrics` and reconcile with the variations BCRD publishes: monthly 5,550/5,550, 12-month 808/808, year-to-date 808/808.

| KPI ID | KPI Name | Unit | Granularity | Priority | Status |
|---|---|---|---|---|---|
| **INF-001** | CPI Index | Index | Monthly | MVP | Validated |
| **INF-002** | Monthly Inflation | % | Monthly | MVP | Validated |
| **INF-003** | YoY Inflation | % | Monthly | MVP | Validated |
| **INF-004** | YTD Inflation | % | Monthly | MVP | Validated |
| **INF-005** | Core Inflation | % | Monthly | MVP | Validated |
| **INF-006** | Inflation by Expenditure Group | % | Monthly | MVP | Validated |

Validated coverage: headline CPI from 1984, expenditure groups (12) from 1999, core CPI from 2000, and regional CPI (Ozama, Norte o Cibao, Este, Sur) from 2011. Regional CPI is available in the same model as `series_type = region`. Windows without enough history return NULL with an `is_full_window_*` flag, the same rule as FX decision D4.

---

## INF-001 — CPI Index

**Business Definition**

Official Consumer Price Index level for the reference period.

**Required Data**

- Observation date
- CPI index
- Expenditure group where applicable

**Expected Source**

Official Dominican economic source — to be validated during Data Source Assessment.

**Candidate Gold Dataset**

```text
gold.inflation_metrics
```

---

## INF-002 — Monthly Inflation

Measures the percentage change in CPI compared with the previous month.

### Calculation

```text
Monthly Inflation % =
(CPI_t / CPI_t-1 - 1) × 100
```

---

## INF-003 — YoY Inflation

Measures the percentage change in CPI compared with the same month of the previous year.

### Calculation

```text
YoY Inflation % =
(CPI_t / CPI_t-12 - 1) × 100
```

---

## INF-004 — YTD Inflation

Measures cumulative inflation from the end of the previous calendar year.

### Calculation

```text
YTD Inflation % =
(CPI_t / CPI_December_Previous_Year - 1) × 100
```

---

## INF-005 — Core Inflation

Represents the official underlying inflation measure according to the methodology of the validated source.

The project should **not independently redefine core inflation**.

Where available, the official published methodology and value should be preserved.

---

## INF-006 — Inflation by Expenditure Group

Measures price changes across CPI expenditure groups or categories.

Potential dimensions:

```text
Date
Expenditure Group
Category
```

This KPI will help identify which categories are experiencing the strongest price pressure.

---

# 7b. Cost of Living KPIs (BCRD Family Basket)

Added on 2026-10-23 to answer **BQ-013: How is the overall cost-of-living environment changing?** at macro level. Product-level prices remain the scope of the Consumer & Basic Basket KPIs (CON-001 to CON-010, Pro Consumidor).

**Validation status:** Validated against the BCRD "Costo de la Canasta Familiar" workbooks (by income quintile and national from 2018; by region from October 2020). Stored in `gold.cost_of_living_metrics` (grain: month × segment).

| KPI ID | KPI Name | Unit | Granularity | Priority | Status |
|---|---|---|---|---|---|
| **COL-001** | Family Basket Cost | DOP/month | Monthly | MVP | Validated |
| **COL-002** | Basket Cost YoY % | % | Monthly | MVP | Validated |
| **COL-003** | Quintile 5 vs Quintile 1 Gap | DOP; ratio | Monthly | MVP | Validated |

```text
COL-001  Basket cost (published BCRD value, DOP)
COL-002  (Cost_t / Cost_t-12 - 1) × 100
COL-003  Q5 - Q1 (DOP)   and   Q5 / Q1 (ratio), same month
```

Methodology notes:

- The basket is the ENGIH-2018 household basket **indexed by CPI**. Its national and regional year-over-year change therefore equals headline and regional CPI inflation. COL KPIs add what CPI cannot show: the cost **level in DOP** and the **income-quintile** view.
- Quintile and national values before October 2020 are a BCRD **retropolation**. They are flagged `is_retropolated`, and year-over-year values that use them are flagged `uses_retropolated_value`.
- COL-003 is a month-level value stored on the national row of each month.

---

# 8. Foreign Exchange KPIs

**Validation status:** Validated (2026-10-23) against the official BCRD daily exchange-rate file (1,253 business-day observations, 2021-09-20 to 2026-09-18). Rates are expressed in DOP per 1 USD.

| KPI ID | KPI Name | Unit | Granularity | Priority | Status |
|---|---|---|---|---|---|
| **FX-001** | USD/DOP Buy Rate | DOP/USD | Daily (business days) | MVP | Validated |
| **FX-002** | USD/DOP Sell Rate | DOP/USD | Daily (business days) | MVP | Validated |
| **FX-003** | Daily FX Change | % | Daily (business days) | MVP | Validated |
| **FX-004** | MoM FX Change | % | Monthly | MVP | Validated |
| **FX-005** | YoY FX Change | % | Monthly | MVP | Validated |
| **FX-006** | YTD FX Change | % | Daily / Monthly | MVP | Validated |
| **FX-007** | 30-Day Moving Average | DOP/USD | Daily (business days) | MVP | Validated |
| **FX-008** | 52-Week High | DOP/USD | Daily (business days) | MVP | Validated |
| **FX-009** | 52-Week Low | DOP/USD | Daily (business days) | MVP | Validated |

## FX Calculation Decisions

The original catalog left four definitions open. They were resolved before building the Silver layer because each one changes dashboard values.

| ID | Decision | Applies to | Rationale |
|---|---|---|---|
| **D1** | Use the **conventional** percentage change `(Rate_t / Rate_ref - 1) × 100` as the primary KPI. Keep the BCRD official appreciation/depreciation values as separate reference columns. | FX-003 to FX-006 | BCRD calculates appreciation/depreciation with the reciprocal (1/rate), so its sign is the opposite of a conventional change. Mixing both would mislead users. Dashboards must state: **"Rate up = peso depreciation."** |
| **D2** | The monthly reference value is the rate on the **last available business day of the month**. | FX-004, FX-005 | Financial-market standard. A monthly average can be added later for comparisons with monthly CPI. |
| **D3** | "30-day" means the trailing **30 business-day observations**, current day included (about six calendar weeks). | FX-007 | The source publishes business days only; there are no weekend or holiday rows. |
| **D4** | Windows without enough history return **NULL** and carry an `is_full_window` flag, instead of showing partial values. | FX-005 to FX-009 | Source history starts on 2021-09-20, so 12-month and 52-week values are not complete until September 2022. |

---

## FX-003 — Daily FX Change

```text
Daily FX Change % =
(Rate_t / Rate_previous_business_day - 1) × 100
```

---

## FX-004 — Month-over-Month FX Change

```text
MoM FX Change % =
(Rate_month_end / Rate_previous_month_end - 1) × 100

Rate_month_end = rate on the last available business day of the month (D2)
```

---

## FX-005 — Year-over-Year FX Change

```text
YoY FX Change % =
(Rate_month_end / Rate_month_end_12_months_earlier - 1) × 100
```

NULL until 12 months of history exist (D4).

---

## FX-006 — YTD FX Change

```text
YTD FX Change % =
(Rate_t / Rate_last_business_day_previous_year - 1) × 100
```

NULL for 2021, because the source has no prior year-end observation (D4). The BCRD official accumulated appreciation/depreciation (reciprocal method) is kept as a reference column (D1).

---

## FX-007 — 30-Day Moving Average

```text
MA30 =
AVG(rate) over the trailing 30 business-day observations, current day included
```

NULL until 30 observations exist (D3, D4).

---

## FX-008 / FX-009 — 52-Week Range

```text
52-Week High =
MAX(rate) over the trailing 52 weeks (364 calendar days), current day included

52-Week Low =
MIN(rate) over the trailing 52 weeks (364 calendar days), current day included
```

NULL until 52 weeks of history exist (D4).

Analytical dataset:

```text
silver.bcrd_exchange_rates_daily   → one row per business day (buy and sell rate)
gold.exchange_rate_metrics         → Date × Currency × Rate Type (long format for BI)
```

---

# 9. Monetary Policy KPIs

| KPI ID | KPI Name | Unit | Priority |
|---|---|---|---|
| **MON-001** | Monetary Policy Rate | % | MVP |
| **MON-002** | Policy Rate Change | Basis Points | MVP |
| **MON-003** | Policy Rate YTD Change | Basis Points | MVP |
| **MON-004** | Inflation–Policy Rate Spread | Percentage Points | MVP |
| **MON-005** | Real Policy Rate Proxy | % / Percentage Points | MVP |

---

## MON-002 — Policy Rate Change

```text
Policy Rate Change (bps) =
(Current Rate - Previous Rate) × 100
```

Example:

```text
7.00% → 6.75%

Change =
(6.75 - 7.00) × 100
= -25 bps
```

---

## MON-004 — Inflation–Policy Rate Spread

```text
Spread =
Monetary Policy Rate - YoY Inflation
```

---

## MON-005 — Real Policy Rate Proxy

For exploratory purposes:

```text
Real Policy Rate Proxy =
Monetary Policy Rate - YoY Inflation
```

> This indicator should explicitly be labeled as a **proxy**. It is not intended to represent a complete expected real interest-rate methodology.

Candidate analytical dataset:

```text
gold.monetary_policy_metrics
```

---

# 10. Fuel Market KPIs

**Validation status:** Validated (2026-10-23) against the official MICM weekly fuel-price file (`precios-de-combustibles-2010-2026`, 872 published weeks, 2010-01-02 to 2026-08-28). Stored in `gold.fuel_price_metrics` (grain: price week × fuel, 15,296 rows).

| KPI ID | KPI Name | Unit | Granularity | Status |
|---|---|---|---|---|
| **FUEL-001** | Current Fuel Price | DOP/gallon | Weekly | Validated |
| **FUEL-002** | Previous Week Price | DOP/gallon | Weekly | Validated |
| **FUEL-003** | Weekly Price Change | DOP/gallon | Weekly | Validated |
| **FUEL-004** | Weekly Price Change % | % | Weekly | Validated |
| **FUEL-005** | Monthly Price Change % | % | Weekly (vs last week of previous month) | Validated |
| **FUEL-006** | YoY Price Change % | % | Weekly (vs week 364–371 days earlier) | Validated |
| **FUEL-007** | YTD Price Change % | % | Weekly (vs last week of previous year) | Validated |
| **FUEL-008** | 4-Week Moving Average | DOP/gallon | Weekly | Validated |
| **FUEL-009** | 12-Week Moving Average | DOP/gallon | Weekly | Validated |
| **FUEL-010** | 52-Week High | DOP/gallon | Weekly (trailing 364 days) | Validated |
| **FUEL-011** | 52-Week Low | DOP/gallon | Weekly (trailing 364 days) | Validated |
| **FUEL-012** | Fuel Price Volatility | % | Weekly (std. dev. of weekly % changes, 12 weeks) | Validated |

Source decisions (from profiling):

- **XLSX is the authoritative format.** Every CSV value equals the XLSX value rounded to whole pesos (0 differences above 0.5 on 19,184 comparable values), so the CSV loses the centavos. Both files are kept in Bronze; the CSV is used only as a reconciliation check.
- **Zero means not published.** A price of 0 (e.g. Gasoil Óptimo before November 2012) is stored as NULL with `is_published = false` and excluded from KPIs.
- **Repeated weeks:** four weeks (9 December 2023 to 5 January 2024) are published twice with some different values. The later block in the file is kept; the earlier copies go to `quality.dq_rejected_records`.
- Price weeks are built from `DIA DESDE` / `DIA HASTA` and the month label, which is sometimes the start and sometimes the end month and has typos; source gaps (3) and overlaps (3) are reported, not altered.
- Windows without enough history return NULL with an `is_full_window_*` flag (FX decision D4).

Fuel dimension values in the validated source (22 series, DOP per gallon): Gasolina Premium, Gasolina Regular, Gasoil Óptimo, Gasoil Regular, Gasoil Premium (until 2015), GLP, Kerosene, Avtur, Fuel Oil, Fuel Oil 1% azufre, and the electricity-generation (EGP-C / EGP-T, interconnected and not interconnected) variants of gasoil and fuel oil.

---

## Weekly Price Change

```text
Weekly Change =
Price_t - Price_t-1
```

## Weekly Price Change %

```text
Weekly Change % =
(Price_t / Price_t-1 - 1) × 100
```

## 4-Week Moving Average

```text
MA4 =
AVG(Price over trailing 4 observations)
```

## 12-Week Moving Average

```text
MA12 =
AVG(Price over trailing 12 observations)
```

## Fuel Price Volatility

A rolling standard deviation of periodic price returns is initially proposed.

The final methodology and window will be defined after evaluating the available historical data.

Candidate analytical dataset:

```text
gold.fuel_price_metrics
```

---

# 11. International Oil KPIs

| KPI ID | KPI Name | Unit | Granularity |
|---|---|---|---|
| **OIL-001** | WTI Price | USD/barrel | Daily |
| **OIL-002** | Brent Price | USD/barrel | Daily |
| **OIL-003** | WTI WoW % | % | Weekly |
| **OIL-004** | Brent WoW % | % | Weekly |
| **OIL-005** | WTI MoM % | % | Monthly |
| **OIL-006** | Brent MoM % | % | Monthly |
| **OIL-007** | WTI 30-Day Moving Average | USD/barrel | Daily |
| **OIL-008** | Brent 30-Day Moving Average | USD/barrel | Daily |

Potential source:

```text
U.S. EIA or another reputable market source
```

The final source will be determined during Data Source Assessment.

Candidate dataset:

```text
gold.oil_market_metrics
```

---

# 12. Economic Relationship KPIs

These KPIs are intended for **exploratory cross-domain analysis**.

| KPI ID | KPI Name | Initial Priority |
|---|---|---|
| **REL-001** | Oil/Fuel Correlation | MVP |
| **REL-002** | Oil/Fuel Lag Correlation T+1 | Phase 2 |
| **REL-003** | Oil/Fuel Lag Correlation T+2 | Phase 2 |
| **REL-004** | Oil/Fuel Lag Correlation T+4 | Phase 2 |

Example analytical concept:

```text
International Oil Price
        │
        ▼
Potential Lag
        │
        ▼
Dominican Fuel Price
```

The analysis may compare:

```text
Oil_t      ↔ Fuel_t
Oil_t      ↔ Fuel_t+1
Oil_t      ↔ Fuel_t+2
Oil_t      ↔ Fuel_t+4
```

The exact meaning of `T+1`, `T+2`, and `T+4` will depend on the aligned analytical frequency.

For example, if fuel observations are weekly:

```text
T+1 = 1 week
T+2 = 2 weeks
T+4 = 4 weeks
```

### Important Analytical Limitation

```text
Correlation ≠ Causation
```

A statistically observed relationship should not automatically be interpreted as evidence that one variable caused another.

Potential candidate dataset:

```text
gold.economic_relationship_metrics
```

---

# 13. Consumer & Basic Basket KPIs

**Validation status:** Partially validated (2026-10-23) against the Pro Consumidor file "Precios Productos de Primera Necesidad, por segmento de comercialización", July–September 2026 (200 products, 5 retail segments: almacenes, colmados, mercados, supermercados grandes, supermercados pequeños). Stored in `gold.consumer_price_metrics` (grain: month × product × presentation, 468 rows).

| KPI ID | KPI Name | Unit | Status |
|---|---|---|---|
| **CON-001** | Average Product Price | DOP / unit | Validated |
| **CON-002** | Median Product Price | DOP / unit | Validated |
| **CON-003** | Minimum Product Price | DOP / unit | Validated (with cheapest segment) |
| **CON-004** | Maximum Product Price | DOP / unit | Validated (with most expensive segment) |
| **CON-005** | Product MoM % | % | Validated, like-for-like: average of the per-segment change for segments priced in both consecutive months (192 of 468 rows) |
| **CON-006** | Product YoY % | % | Not calculable: the source covers 3 months |
| **CON-007** | Product YTD % | % | Not calculable: the source covers 3 months |
| **CON-008** | Product Price Volatility | % | Not calculable: too few observations per product |
| **CON-009** | Regional Price Difference % | % | Not calculable: the source has no geography. `price_spread_pct` (max vs min across retail segments) is provided instead and is not a regional measure |
| **CON-010** | Category Price Index | Index | Proposed: needs a category mapping and weighting methodology |

Source decisions (from profiling):

- **XLSX is used**; the CSV has inconsistent delimiters.
- The file title states the report period. **30 rows whose year is outside that period** (2027, 2035, 2041 and others, clear capture errors) are rejected to `quality.dq_rejected_records`, not corrected.
- Prices are compared only within the same product **and** presentation. Because the segments priced change from month to month, the month-over-month change is never computed on the cross-segment average (that would mix price changes with sample changes).

Potential analytical dimensions:

```text
Date
Product
Category
Subcategory
Brand
Presentation
Quantity
Unit
Store
Municipality
Province
Region
```

---

## Product Price Comparability

Product-price comparisons require careful standardization.

For example:

```text
Rice — Brand A — 1 lb
```

should not automatically be treated as equivalent to:

```text
Rice — Brand B — 5 lb
```

The Silver layer will therefore need to evaluate:

- Product identity
- Brand
- Presentation
- Quantity
- Unit of measure
- Store
- Geography
- Observation date

Potential standardized metrics may eventually include:

```text
Price per unit
Price per pound
Price per kilogram
Price per liter
```

where appropriate.

Candidate dataset:

```text
gold.consumer_price_metrics
```

---

# 14. Agricultural Price KPIs

| KPI ID | KPI Name | Unit |
|---|---|---|
| **AGR-001** | Average Agricultural Price | DOP / unit |
| **AGR-002** | MoM Price Change % | % |
| **AGR-003** | YoY Price Change % | % |
| **AGR-004** | YTD Price Change % | % |
| **AGR-005** | Price Volatility | % |
| **AGR-006** | Seasonal Price Index | Index |
| **AGR-007** | Regional Price Difference % | % |

Potential products include:

```text
Rice
Plantain
Banana
Chicken
Eggs
Beans
Potatoes
Tomatoes
Onions
Garlic
```

The final product list will depend on source availability.

Potential dimensions:

```text
Date
Product
Unit
Market
Municipality
Province
Region
```

Candidate dataset:

```text
gold.agricultural_price_metrics
```

---

# 15. Energy & Electricity KPIs

| KPI ID | KPI Name | Unit | Priority |
|---|---|---|---|
| **ENE-001** | Electricity Tariff | DOP/kWh or source unit | Phase 2 |
| **ENE-002** | MoM Tariff Change % | % | Phase 2 |
| **ENE-003** | YoY Tariff Change % | % | Phase 2 |
| **ENE-004** | YTD Tariff Change % | % | Phase 2 |
| **ENE-005** | Average Cost per kWh | DOP/kWh | Phase 2 |

Potential dimensions:

```text
Date
Tariff Category
Distributor
Region
```

Candidate sources may include official Dominican electricity-sector institutions.

However:

> **This domain remains Pending Source Validation.**

Candidate dataset:

```text
gold.energy_price_metrics
```

---

# 16. Housing & Rental KPIs

Housing is initially classified as **Phase 2**.

Initial KPI:

| KPI ID | KPI Name | Unit | Status |
|---|---|---|---|
| **HOU-001** | Median Rental Asking Price | DOP/month | Pending Source Validation |

Potential dimensions:

```text
Date
Property Type
Bedrooms
Bathrooms
Municipality
Sector
Region
```

Potential calculation:

```text
Median Rental Asking Price =
MEDIAN(Comparable Rental Listings)
```

However, this KPI will only be implemented if a reliable, legally appropriate, and technically sustainable data source can be identified.

Unauthorized scraping is outside the scope of the project.

Candidate dataset:

```text
gold.housing_price_metrics
```

---

# 17. Cross-Domain Analytical Framework

One of the long-term objectives of the platform is to move beyond isolated KPI monitoring.

The platform should eventually enable analysis such as:

```text
International Oil
       ↓
Exchange Rate
       ↓
Domestic Fuel Prices
       ↓
Transportation Costs
       ↓
Consumer Prices
       ↓
Inflation
```

Other potential analytical relationships include:

```text
USD/DOP ↔ Inflation
USD/DOP ↔ Fuel Prices
USD/DOP ↔ Consumer Prices

WTI ↔ Fuel Prices
Brent ↔ Fuel Prices

Fuel Prices ↔ Inflation

Food Prices ↔ Inflation

Monetary Policy Rate ↔ Inflation
```

These relationships should be treated as analytical hypotheses to investigate rather than predetermined conclusions.

The project should distinguish between:

- Correlation
- Temporal association
- Lagged relationship
- Statistical significance
- Economic interpretation
- Causality

Causal claims should not be made solely from correlation analysis.

---

# 18. Candidate Gold Analytical Layer

The KPI Catalog provides the first indication of what the future Gold layer may require.

Initial candidate datasets include:

```text
gold/
│
├── inflation_metrics
├── exchange_rate_metrics
├── monetary_policy_metrics
├── fuel_price_metrics
├── oil_market_metrics
├── consumer_price_metrics
├── agricultural_price_metrics
├── energy_price_metrics
├── housing_price_metrics
└── economic_relationship_metrics
```

These names are **conceptual candidates**, not final physical table definitions.

Final Gold architecture will be determined after:

1. Data Source Assessment
2. Data Profiling
3. Data Dictionary
4. Source-to-Target Mapping
5. Solution Architecture
6. Logical Data Modeling
7. Physical Data Modeling

The project intentionally avoids creating Gold tables before understanding the source data and required grain.

---

# 19. Dashboard Mapping

The KPI Catalog will eventually support multiple analytical dashboard pages.

| Dashboard Page | Primary Domains |
|---|---|
| **Executive Economic Overview** | Cross-domain |
| **Inflation & CPI** | Inflation |
| **Monetary Policy** | Monetary |
| **FX Market** | Foreign Exchange |
| **Fuel & Oil Market** | Fuel + International Oil |
| **Basic Basket & Consumer Prices** | Consumer Products |
| **Agricultural Prices** | Agriculture |
| **Energy & Electricity** | Energy |
| **Housing & Cost of Living** | Housing |
| **Regional Analysis** | Consumer + Agriculture + Housing |
| **Economic Relationships** | Cross-domain |

The exact dashboard structure may evolve after source and data-grain validation.

---

# 20. KPI Governance

Each KPI in the detailed Excel catalog contains the following governance attributes:

| Field | Purpose |
|---|---|
| **KPI_ID** | Stable unique identifier |
| **Domain** | Analytical subject area |
| **Business_Question** | Business question supported |
| **KPI_Name** | Business-friendly metric name |
| **Business_Definition** | Plain-language meaning |
| **Calculation_Logic** | Proposed calculation |
| **Unit** | Measurement unit |
| **Granularity** | Analytical frequency / grain |
| **Dimensions** | Required analytical dimensions |
| **Required_Data** | Minimum required data |
| **Expected_Source** | Candidate source |
| **Gold_Dataset** | Candidate analytical dataset |
| **Dashboard_Page** | Intended presentation layer |
| **Priority** | MVP / Phase 2 / Future |
| **Validation_Status** | Current validation state |
| **Notes** | Methodological or implementation caveats |

---

# 21. Validation Status

KPIs can use the following validation states:

| Status | Meaning |
|---|---|
| **Proposed** | KPI has been defined but source/data feasibility has not been fully validated |
| **Pending Source Validation** | KPI depends on identifying or validating an appropriate source |
| **Validated** | Required data, methodology, and source have been validated |
| **Deferred** | KPI has been intentionally postponed |

At this stage, many KPIs remain **Proposed**.

This is intentional.

The project should not label a KPI as validated until its required data and calculation methodology have been confirmed.

---

# 22. Calculation Principles

KPI calculations should follow several common principles.

## 22.1 Percentage Change

Generic period-over-period change:

```text
Percentage Change =
(Current Value / Previous Value - 1) × 100
```

---

## 22.2 Year-over-Year Change

```text
YoY % =
(Current Value / Value Same Period Previous Year - 1) × 100
```

---

## 22.3 Year-to-Date Change

```text
YTD % =
(Current Value / Last Comparable Value Previous Year - 1) × 100
```

The exact reference observation must be defined for each domain.

---

## 22.4 Moving Average

```text
Moving Average =
AVG(Value over defined rolling window)
```

Examples:

```text
30-Day Moving Average
4-Week Moving Average
12-Week Moving Average
```

---

## 22.5 Volatility

A candidate approach is:

```text
Volatility =
STDDEV(Periodic Returns over defined rolling window)
```

The specific methodology will be determined based on:

- Data frequency
- Number of observations
- Business interpretation
- Historical coverage

---

## 22.6 Basis Points

For interest-rate changes:

```text
1 Percentage Point = 100 Basis Points
```

Example:

```text
7.00% → 6.75%

Change = -0.25 percentage points
       = -25 basis points
```

---

# 23. Data Granularity & Dimensions

Different domains operate at different natural grains.

Examples:

| Domain | Expected Grain |
|---|---|
| Inflation | Month × CPI Category |
| Foreign Exchange | Date × Currency × Rate Type |
| Monetary Policy | Effective Date × Rate |
| Fuel | Week × Fuel Type |
| Oil | Date × Benchmark |
| Consumer Products | Date × Product × Store × Location |
| Agriculture | Date × Product × Market/Location |
| Electricity | Period × Tariff Category |
| Housing | Date × Property Segment × Location |

These grains are preliminary.

The final grain of each fact table will be defined during data modeling.

---

## Shared Analytical Dimensions

Potential shared dimensions include:

```text
dim_date
dim_product
dim_location
dim_fuel
dim_source
dim_currency
dim_category
dim_unit
```

These are conceptual candidates and should not yet be interpreted as final physical tables.

---

# 24. Source Validation Requirements

The next major project phase will validate the sources required to calculate these KPIs.

For every candidate source, the project should evaluate:

### Source Identity

- Institution
- Dataset
- URL / endpoint
- Data owner

### Access Method

- API
- CSV
- Excel
- JSON
- PDF
- HTML table
- Other approved mechanism

### Data Characteristics

- Available fields
- Historical coverage
- Update frequency
- Granularity
- Geographic coverage
- Units
- Data types

### Technical Feasibility

- Automated ingestion capability
- Authentication requirements
- Rate limits
- Download stability
- Schema consistency
- Incremental ingestion feasibility

### Data Quality

- Completeness
- Missing observations
- Duplicates
- Historical consistency
- Naming consistency
- Unit consistency

### Governance

- Public availability
- Terms of use
- Usage restrictions
- Attribution requirements

The source should then receive a feasibility assessment.

Example:

| Rating | Meaning |
|---|---|
| **High** | Reliable and suitable for automated MVP ingestion |
| **Medium** | Usable but requires additional transformation or operational handling |
| **Low** | Significant limitations |
| **Deferred** | Not appropriate for current MVP |

---

# 25. Definition of Done

The **Business Questions & KPI Catalog** will be considered complete for the Business Discovery phase when:

- Business questions are documented.
- Each MVP KPI has a unique identifier.
- Each KPI has a business definition.
- Calculation logic is proposed.
- Units are documented.
- Expected granularity is documented.
- Required dimensions are identified.
- Required source data is identified.
- Candidate sources are identified.
- KPI priority is defined.
- Validation status is documented.
- Candidate Gold datasets are mapped.
- Candidate dashboard pages are mapped.
- Major methodological limitations are documented.
- The detailed Excel catalog is stored in the repository.
- The Markdown documentation is stored in the repository.

The catalog may continue to evolve after Data Source Assessment.

---

# 26. Next Steps

The current project documentation sequence is:

```text
01 — Business Requirements Document
              COMPLETE
                  ↓
02 — Project Charter
              COMPLETE
                  ↓
03 — Business Questions & KPI Catalog
              CURRENT
                  ↓
04 — Data Source Assessment
              NEXT
                  ↓
05 — Data Dictionary
                  ↓
06 — Source-to-Target Mapping
                  ↓
07 — Solution Architecture
                  ↓
08 — Logical & Physical Data Model
                  ↓
09 — Data Quality Rules & Data Contracts
                  ↓
10 — Databricks Environment Setup
                  ↓
11 — Bronze Layer
                  ↓
12 — Silver Layer
                  ↓
13 — Gold Layer
                  ↓
14 — Databricks Workflows
                  ↓
15 — Monitoring & Data Quality
                  ↓
16 — Databricks SQL
                  ↓
17 — Databricks Dashboard
                  ↓
18 — Power BI
                  ↓
19 — Testing & Validation
                  ↓
20 — Business Insights
                  ↓
21 — Portfolio Publication
```

The immediate next deliverable is:

```text
04_Data_Source_Assessment
```

The Data Source Assessment will determine whether the data required by the KPI Catalog is actually available, reliable, historically sufficient, and technically suitable for ingestion.

Only after source feasibility is understood should the project finalize its physical architecture and begin Databricks implementation.

---

## Document History

| Version | Date | Description | Author |
|---|---|---|---|
| **1.0** | September 2026 | Initial Business Questions & KPI Catalog | Stanly Fernandez |

---

## Related Project Documentation

| Document | Format | Status |
|---|---|---|
| `01_Business_Requirements_Document` | DOCX / Markdown | Draft |
| `02_Project_Charter` | DOCX / Markdown | Draft |
| `03_Business_Questions_KPI_Catalog` | XLSX / Markdown | Draft |
| `04_Data_Source_Assessment` | TBD | Next |
| `05_Data_Dictionary` | TBD | Planned |
| `06_Source_to_Target_Mapping` | TBD | Planned |
| `07_Solution_Architecture` | TBD | Planned |
| `08_Data_Model` | TBD | Planned |
| `09_Data_Quality_Rules` | TBD | Planned |

---

## Repository Documentation Principle

The repository follows the principle:

> **Business first. Data second. Architecture third. Implementation fourth.**

The objective is not simply to demonstrate that a pipeline can be built.

The objective is to demonstrate why the pipeline exists, which business questions it supports, how its data is governed, how its metrics are calculated, and how the final analytical outputs can be trusted.

---

**RD Economic & Financial Intelligence Platform**  
*End-to-End Data Engineering & Business Intelligence Portfolio Project*
