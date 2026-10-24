# Project Documentation

This directory contains the business, functional, data, architecture, and technical documentation for the **RD Economic & Financial Intelligence Platform**.

The documentation follows the complete project lifecycle, from business discovery and data-source assessment to data engineering, analytics, orchestration, and business intelligence implementation.

---

## Project Documentation Roadmap

| # | Document | Status |
|---|---|---|
| 01 | [Business Requirements Document](01_Business_Requirements_Document.md) | Complete |
| 02 | [Project Charter](02_Project_Charter.md) | Complete |
| 03 | [Business Questions & KPI Catalog](03_Business_Questions_KPI_Catalog.md) | Complete |
| 04 | [Data Source Assessment](04_Data_Source_Assessment.md) | Complete |
| 05 | Data Dictionary | Planned |
| 06 | Source-to-Target Mapping | Planned |
| 07 | Solution Architecture | Planned |
| 08 | Logical & Physical Data Model | Planned |
| 09 | Data Quality Rules & Data Contracts | Planned |
| 10 | Databricks Environment Setup | In Progress — Initial infrastructure validated |
| 11 | Bronze Layer | In Progress — BCRD, MICM and Pro Consumidor implemented in development |
| 12 | Silver Layer | In Progress — BCRD, MICM and Pro Consumidor implemented in development |
| 13 | Gold Layer | In Progress — FX, INF, COL, FUEL and CON KPIs implemented in development |
| 14 | Databricks Workflows | In Progress — Lakeflow Job implemented (16 tasks, 5 parallel chains) |
| 15 | Monitoring & Data Quality | Planned |
| 16 | Databricks SQL Analytics | Planned |
| 17 | Databricks Dashboard | Planned |
| 18 | Power BI Dashboard | In Progress — report built (7 pages: FX, Inflation, FX vs Inflation, Cost of Living, Fuel, Consumer, Electricity) |
| 19 | Testing & Validation | Planned |
| 20 | Business Insights | Planned |
| 21 | Portfolio Publication | Planned |

---

# Current Project Phase

## Phase 2 — Data Discovery & Profiling

Business Discovery and the initial Data Source Assessment are complete. The project is validating real source files against the approved business questions and KPI catalog before committing to physical data models or Databricks pipelines.

**Current activity:** source-level profiling, source-format reconciliation, data-quality assessment, and documentation of unresolved issues.

## Current Data Discovery & Profiling Progress

| Dataset / Source | Status | Evidence and next validation |
|---|---|---|
| BCRD — USD/DOP Exchange Rates | Initial profiling completed | Historical Excel reviewed; official incremental extraction remains unconfirmed |
| BCRD — CPI, CPI Groups, Core CPI, CPI Regions, Family Basket by Quintile and Region | Validated; Bronze, Silver and Gold implemented | Six workbooks parsed into five monthly Silver tables with 0 rejects; calculated inflation reconciles with BCRD published values |
| MICM — Fuel Prices | Validated; pipelines implemented | XLSX authoritative (CSV = XLSX rounded to whole pesos, 0 differences on 19,184 values); zero = not published; four December 2023 weeks published twice resolved to the later block |
| Pro Consumidor — Consumer Prices | Validated for Jul–Sep 2026; pipelines implemented | XLSX used (CSV malformed); 30 rows with years outside the report period rejected; only 3 months and no geography, so YoY, YTD, volatility and regional KPIs are not calculable yet |
| Ministry of Agriculture — Agricultural Prices | Preliminary profiling and CSV/XLSX reconciliation completed | Wholesale and retail files (Aug 2017 – Sep 2026) profiled and reconciled; quality validation and KPI feasibility (AGR-001 to AGR-007) remain open |
| EIA — WTI / Brent | Not started | External driver only under RD-First governance |

**Current phase:** Data Discovery & Profiling  
**Next milestone:** Build the Ministry of Agriculture pipelines, build the electricity series from the MEM monthly reports (sources assessed below), obtain more Pro Consumidor history, and prepare evidence-based inputs for `05_Data_Dictionary` and `06_Source-to-Target_Mapping`.

**Technical documentation:**
- [MICM Fuel Prices — Data Discovery & Profiling](../profiling/micm/README.md)
- [Pro Consumidor — Consumer Prices Data Discovery & Profiling](../profiling/proconsumidor/README.md)
- [Ministry of Agriculture — Agricultural Prices Data Discovery & Profiling](../profiling/agriculture/README.md)
### Databricks Lakehouse Infrastructure Status

**Environment:** Databricks Free Edition  
**Implementation status:** Initial infrastructure implemented and validated.

The following infrastructure components have been successfully verified:

- Unity Catalog: `rd_economic_intelligence`
- Schemas: `bronze`, `silver`, `gold`, `metadata`, `quality`
- Raw Unity Catalog Volumes: `bcrd_raw`, `micm_raw`, `proconsumidor_raw`, `agriculture_raw`
- Raw landing directories for BCRD exchange rates, CPI, monetary policy, MICM fuel prices, Pro Consumidor consumer prices, and Ministry of Agriculture retail and wholesale prices.

**Validation result:** All infrastructure checks passed.

**GitHub implementation:** [Databricks Setup Notebooks](../src/setup/)

**Important:** Infrastructure validation confirms that the catalog, schemas, volumes, and landing directories exist. It does not confirm that source datasets have been ingested or that Bronze, Silver, and Gold pipelines are operational.

### Bronze Layer Status

**Implementation status:** First Bronze pipeline implemented and verified in development.

| Pipeline | Target table | Result |
|---|---|---|
| [01_BCRD_Exchange_Rates_Bronze](../src/bronze/01_BCRD_Exchange_Rates_Bronze.ipynb) | `rd_economic_intelligence.bronze.bcrd_exchange_rates_daily` | 1,253 rows loaded (2021-09-20 to 2026-09-18); row count matches source; all observational quality checks passed (no invalid or duplicate dates, no null or non-positive rates, no buy rate above sell rate) |

Design rules applied:

- Source values are preserved; only column names are converted to Delta-safe snake_case, with the mapping documented in the notebook.
- Every row carries lineage metadata: source file, path, sheet, source row number, file size and modification time, report period, batch ID and ingestion timestamp.
- A structural contract stops the load if the BCRD file layout changes.
- Data-quality checks are observational in Bronze: they report and never filter.
- Re-runs are idempotent per source file: previously loaded rows from the same file are replaced, not duplicated.

**Technical finding:** Databricks Free Edition serverless compute does not include `openpyxl`, which pandas requires to read `.xlsx` files. Every Excel-based ingestion notebook installs a pinned version (`openpyxl==3.1.5`) in its first code cell.

**Important:** This is a development implementation, not a production pipeline. Incremental loading is still pending (see the MICM and Pro Consumidor section below for the other Bronze pipelines).

### Silver Layer Status

**Implementation status:** First Silver transformation implemented and verified in development.

| Pipeline | Target table | Result |
|---|---|---|
| [01_BCRD_Exchange_Rates_Silver](../src/silver/01_BCRD_Exchange_Rates_Silver.ipynb) | `rd_economic_intelligence.silver.bcrd_exchange_rates_daily` | 1,253 rows (2021-09-20 to 2026-09-18), one per business day; 0 rejected; reconciliation passed (Silver + rejected = Bronze) |

Design rules applied:

- Typed business columns: `rate_date` (DATE), `buy_rate` and `sell_rate` (DECIMAL(10,4)), plus derived `spread` and `mid_rate`. Rates are DOP per 1 USD.
- BCRD official appreciation/depreciation values are kept as `bcrd_*_ref_pct` reference columns only. They use the reciprocal method and the opposite sign of a conventional change (KPI decision D1).
- Enforced rules: valid date, positive buy and sell rates, buy rate not above sell rate, one row per date. Failing rows go to `quality.dq_rejected_records`; they are never silently dropped.
- Delta table constraints (`NOT NULL` and `CHECK`) protect the table from future invalid writes.
- Every run logs rule results in `quality.dq_rule_results`. Table and column descriptions are stored in Unity Catalog.
- Load pattern: full refresh from Bronze (idempotent). To be revisited when incremental ingestion is added.

**Data finding:** six gaps of five calendar days between published rates. All match Dominican public holidays when BCRD does not publish (Holy Week in 2022–2026, and Altagracia/Duarte days in January 2022). No data is missing. This confirms KPI decision D3: moving averages count business-day observations, not calendar days.

### Gold Layer Status

**Implementation status:** First Gold KPI model implemented and verified in development. The USD/DOP pipeline now runs end to end: Raw → Bronze → Silver → Gold.

| Pipeline | Target table | Grain | KPIs | Rows |
|---|---|---|---|---|
| [01_BCRD_Exchange_Rates_Gold](../src/gold/01_BCRD_Exchange_Rates_Gold.ipynb) | `gold.exchange_rate_metrics` | Date × currency pair × rate type | FX-001, FX-002, FX-003, FX-006, FX-007, FX-008, FX-009 | 2,506 |
| [01_BCRD_Exchange_Rates_Gold](../src/gold/01_BCRD_Exchange_Rates_Gold.ipynb) | `gold.exchange_rate_monthly_metrics` | Month × currency pair × rate type | FX-004, FX-005, month-end FX-006 | 122 |

Daily and monthly KPIs live in separate tables so BI tools never aggregate monthly values over daily rows.

Validation results (all passed):

- Row count equals Silver × 2 rate types; one row per date, currency pair and rate type.
- Moving-average and 52-week values are NULL exactly when their window is incomplete (KPI decision D4).
- 52-week low never exceeds the high, and every rate falls inside its 52-week range.
- **Reconciliation with BCRD official values:** our YTD change, restated with the BCRD reciprocal method, matches the published BCRD accumulated appreciation/depreciation on **2,358 of 2,358** comparable days (tolerance 0.15 points for BCRD's one-decimal rounding). This confirms the calculation logic and the sign convention of decision D1.

**Data finding:** the source extract starts on 2021-09-20 and ends on 2026-09-18, so the first and last months do not cover a full month. They are flagged with `is_partial_month` so dashboards can label them as month-to-date. Full 52-week windows start on 2022-09-19 and full year-over-year values in September 2022.

### CPI and Family Basket Pipelines

**Implementation status:** Implemented and verified in development.

| Layer | Notebook | Output | Result |
|---|---|---|---|
| Bronze | [02_BCRD_CPI_Bronze](../src/bronze/02_BCRD_CPI_Bronze.ipynb) | `bronze.bcrd_cpi_raw_rows` | 1,843 rows from 6 workbooks, captured as published |
| Silver | [02_BCRD_CPI_Silver](../src/silver/02_BCRD_CPI_Silver.ipynb) | 5 tables (below) | 6,476 records, 0 rejected, all rules passed |
| Gold | [02_BCRD_CPI_Gold](../src/gold/02_BCRD_CPI_Gold.ipynb) | `gold.inflation_metrics` | 5,568 rows, INF-001 to INF-006 |
| Gold | [03_BCRD_Cost_of_Living_Gold](../src/gold/03_BCRD_Cost_of_Living_Gold.ipynb) | `gold.cost_of_living_metrics` | 908 rows, COL-001 to COL-003 |

Silver tables: `bcrd_cpi_national_monthly` (1984+), `bcrd_cpi_core_monthly` (2000+), `bcrd_cpi_groups_monthly` (12 groups, 1999+), `bcrd_cpi_regions_monthly` (4 regions, 2011+), `bcrd_family_basket_monthly` (quintiles and national 2018+, regions Oct-2020+).

Design decisions:

- **Bronze captures rows, not columns.** The BCRD workbooks are presentation tables (titles, multi-row headers, the year written once per block, Spanish month names, index/variation pairs, methodology notes), each with a different layout. Bronze stores every row as published; layout interpretation happens in Silver, in tested, reusable parsers ([`src/shared/bcrd_cpi_parsers.py`](../src/shared/bcrd_cpi_parsers.py)).
- **Enforced rules:** unique business key, positive values, contiguous months per series, no unparseable values. Silver is not written if any enforced rule fails.
- **Region labels standardized:** BCRD writes "Región Norte" in the CPI file and "Región Norte o Cibao" in the basket file; both map to `Norte o Cibao`, and the source label is kept.
- **Retropolation flagged:** basket quintile values before October 2020 are a BCRD retropolation (`is_retropolated`).

Reconciliation with BCRD published values (all passed): monthly variation 5,550/5,550; 12-month 808/808; year-to-date 808/808.

**Data finding:** the family basket is the ENGIH-2018 basket indexed by CPI, so its national and regional year-over-year change equals CPI inflation. The cost-of-living KPIs add the DOP level and the income-quintile view, not an independent inflation signal.

### MICM Fuel and Pro Consumidor Pipelines

**Implementation status:** Implemented and verified in development.

| Layer | Notebook | Output | Result |
|---|---|---|---|
| Bronze | [04_MICM_Fuel_Prices_Bronze](../src/bronze/04_MICM_Fuel_Prices_Bronze.ipynb) | `bronze.micm_fuel_prices_raw` | 872 XLSX + 872 CSV rows, all source columns kept as JSON |
| Silver | [04_MICM_Fuel_Prices_Silver](../src/silver/04_MICM_Fuel_Prices_Silver.ipynb) | `silver.micm_fuel_prices_weekly` | 19,096 rows, 22 fuels, 2010-01-02 to 2026-08-28; 4 superseded weeks rejected |
| Gold | [04_MICM_Fuel_Prices_Gold](../src/gold/04_MICM_Fuel_Prices_Gold.ipynb) | `gold.fuel_price_metrics` | 15,296 rows, FUEL-001 to FUEL-012 |
| Bronze | [05_ProConsumidor_Prices_Bronze](../src/bronze/05_ProConsumidor_Prices_Bronze.ipynb) | `bronze.proconsumidor_prices_raw` | 600 rows plus the report-period title |
| Silver | [05_ProConsumidor_Prices_Silver](../src/silver/05_ProConsumidor_Prices_Silver.ipynb) | `silver.proconsumidor_prices_monthly` | 570 rows, 197 products, 5 retail segments; 30 rejected (year outside report period); 21 label variants canonicalized |
| Gold | [05_ProConsumidor_Prices_Gold](../src/gold/05_ProConsumidor_Prices_Gold.ipynb) | `gold.consumer_price_metrics` | 461 rows, CON-001 to CON-005 |

Design decisions:

- **MICM: XLSX is authoritative.** Every CSV value equals the XLSX value rounded to whole pesos (0 differences above 0.5 on 19,184 values), so the CSV loses precision. The CSV stays in Bronze for an observational reconciliation check.
- **MICM price weeks** are rebuilt from `DIA DESDE`, `DIA HASTA` and a month label that is sometimes the start month, sometimes the end month, and has typos ([`src/shared/micm_parsers.py`](../src/shared/micm_parsers.py)). Source gaps (3) and overlaps (3) are reported, not altered.
- **MICM zero prices** mean "not published" (NULL, `is_published = false`) and are excluded from KPIs.
- **Pro Consumidor anomalous years** (2027 to 2041 in a July–September 2026 report) are rejected, not corrected.
- **Pro Consumidor month-over-month** is like-for-like by retail segment: the segments priced change from month to month, so comparing cross-segment averages would mix price changes with sample changes.

**Data finding:** fuel prices were frozen from August to December 2025 (for example Gasolina Premium RD$290 every week), so in the latest week the year-over-year and year-to-date changes are identical.

### MEM Electricity Pipeline

**Implementation status:** Implemented and verified in development (2026-10-24).

| Layer | Notebook | Output | Result |
|---|---|---|---|
| Bronze | [06_MEM_Electricity_Bronze](../src/bronze/06_MEM_Electricity_Bronze.ipynb) | `bronze.mem_electricity_raw_rows` | 182 + 39 sheet rows from the July 2026 annex |
| Silver | [06_MEM_Electricity_Silver](../src/silver/06_MEM_Electricity_Silver.ipynb) | `silver.mem_ede_monthly`, `silver.mem_tariffs_quarterly` | 35,446 monthly values (2009–Jul 2026); 4,430 tariff values (29 periods, 2020–Sep 2026); all enforced rules passed |
| Gold | [06_MEM_Electricity_Gold](../src/gold/06_MEM_Electricity_Gold.ipynb) | `gold.electricity_metrics`, `gold.electricity_tariff_monthly`, `gold.electricity_bts1_bill` | 316 / 6,822 / 486 rows, ENE-001 to ENE-009, January 2020 to July 2026 |

Design decisions:

- **Source choice:** SIE tariff resolutions are scanned PDFs; the MEM monthly PDF report has text but one month per file. The MEM **annex workbook** has the full monthly history and the tariff table in machine-readable form, so it is the primary source. The latest annex replaces the previous one (each carries all history).
- **Reconciliation:** average selling price matches the MEM PDF report for May 2026 (Edenorte RD$10.13/kWh, Edesur RD$10.51/kWh), enforced in Gold.
- **Tariff periods** are expanded to months; the overlapping periods `abr - may 26` and `abr - jun 26` resolve to the later column. Before October 2021 the applied tariff is one value for all distributors.
- **Reference vs applied tariff** gap is reported as a subsidy proxy, not as an official subsidy figure.

**Data finding:** in July 2026 a 200 kWh BTS-1 bill is about RD$1,321 (Edenorte) with the applied tariff versus about RD$3,412 with the reference tariff; Edeeste's 12-month energy losses (about 56%) are roughly twice those of Edenorte and Edesur.

### Orchestration Status

Lakeflow Job `rd_economic_medallion_pipeline` ([definition](../resources/jobs/bcrd_medallion_pipeline.job.json)) runs five independent chains in parallel from the Git folder (branch `main`): BCRD FX, BCRD CPI (then cost of living), MICM fuel, Pro Consumidor and MEM electricity. 16 notebook tasks on serverless compute, one retry per task, failure e-mail alerts, maximum one concurrent run. A weekday 07:00 (America/Santo_Domingo) schedule is defined but **paused** while source files are uploaded manually.

The progress table tracks operational source discovery. It does **not** change the completion status of documents 05–21 in the formal roadmap.

---

## Completed Deliverables

The following project artifacts have been completed:

### 01 — Business Requirements Document

Defines:

- Business problem
- Project objectives
- Business scope
- Stakeholders
- Functional requirements
- Non-functional requirements
- Analytical requirements
- Expected business value

Files:

```text
01_Business_Requirements_Document.docx
01_Business_Requirements_Document.md
```

---

### 02 — Project Charter

Defines:

- Project purpose
- Project scope
- MVP boundaries
- Project phases
- Major deliverables
- Assumptions
- Constraints
- Risks
- Success criteria

Files:

```text
02_Project_Charter.docx
02_Project_Charter.md
```

---

### 03 — Business Questions & KPI Catalog

Translates business requirements into measurable analytical questions and KPIs.

Main analytical domains include:

- Inflation & CPI
- Foreign Exchange
- Monetary Policy
- Fuel Prices
- Consumer Prices
- Agricultural Prices
- International Oil Drivers
- Electricity
- Housing / Rentals

Files:

```text
03_Business_Questions_KPI_Catalog.xlsx
03_Business_Questions_KPI_Catalog.md
```

---

### 04 — Data Source Assessment

Evaluates the availability, authority, historical coverage, granularity, format, automation potential, and engineering feasibility of the datasets required to calculate the proposed KPIs.

Files:

```text
04_Data_Source_Assessment.xlsx
04_Data_Source_Assessment.md
```

The assessment also establishes the project's **RD-First Data Strategy**.

---

# RD-First Data Strategy

The primary analytical subject of the platform is the:

> **Dominican Republic**

Core datasets must therefore describe economic, financial, market, price, or cost-of-living conditions in the Dominican Republic.

Examples include:

```text
Dominican CPI
Dominican Inflation
USD/DOP Exchange Rate
Dominican Monetary Policy Rate
Dominican Fuel Prices
Dominican Consumer Prices
Dominican Agricultural Prices
Dominican Electricity Tariffs
Dominican Housing Costs
```

---

## External Data Governance

International datasets are not included simply because they are economically relevant globally.

An international dataset may only be incorporated when it has a defined analytical relationship with a Dominican Republic KPI.

Governance rule:

```text
IF Geographic_Scope != "Dominican Republic"
AND Source_Role != "External Driver"

THEN

Exclude dataset from platform
```

Example:

```text
WTI / Brent
      ↓
International Oil Market
      ↓
Potential External Pressure
      ↓
Dominican Fuel Prices
      ↓
Dominican Inflation / Cost of Living
```

WTI and Brent therefore represent:

```text
Geographic Scope = International
Source Role       = External Driver
```

They must never be interpreted or presented as Dominican price data.

---

# Core Data Sources

The current source assessment identified the following primary sources. BCRD family-basket datasets are also being evaluated as a cost-of-living extension; any resulting new KPI IDs require formal catalog review.

| Institution | Domain | Geographic Scope | Project Role |
|---|---|---|---|
| Banco Central de la República Dominicana — BCRD | Inflation / CPI | Dominican Republic | Core Domestic |
| Banco Central de la República Dominicana — BCRD | USD/DOP Exchange Rate | Dominican Republic | Core Domestic |
| Banco Central de la República Dominicana — BCRD | Monetary Policy | Dominican Republic | Core Domestic |
| Ministerio de Industria, Comercio y Mipymes — MICM | Fuel Prices | Dominican Republic | Core Domestic |
| Pro Consumidor | Consumer / Basic Basket Prices | Dominican Republic | Core Domestic |
| Ministerio de Agricultura | Agricultural Prices | Dominican Republic | Core Domestic |
| Superintendencia de Electricidad — SIE (tariffs) and Ministerio de Energía y Minas — MEM (distributor performance annex) | Electricity Tariffs and Costs | Dominican Republic | Phase 2 — implemented |
| U.S. EIA — WTI / Brent | International Oil | International | External Driver |
| TBD | Housing / Rentals | Dominican Republic | Phase 2 / Pending |

---

# MVP Data Domains

The initial MVP currently includes:

```text
RD ECONOMIC & FINANCIAL INTELLIGENCE PLATFORM
│
├── Inflation & CPI
│      └── BCRD
│
├── Foreign Exchange
│      └── BCRD
│
├── Monetary Policy
│      └── BCRD
│
├── Fuel Prices
│      └── MICM
│
├── Consumer / Basic Basket Prices
│      └── Pro Consumidor
│
├── Agricultural Prices
│      └── Ministry of Agriculture
│
└── External Economic Driver
       └── WTI / Brent
```

Potential Phase 2 domains:

```text
Electricity
Housing / Rentals
Advanced Cross-Domain Analytics
```

---

# Current Activity — Data Profiling

The project is now moving from:

```text
"What data should exist?"
```

to:

```text
"What does the actual data look like?"
```

Actual source files will be downloaded and inspected before physical table designs are finalized.

---

## Data Profiling Objectives

Each dataset will be evaluated across the following dimensions.

### Schema

```text
Column names
Column count
Column order
Data types
Schema consistency
```

### Completeness

```text
Row count
Null values
Missing periods
Missing categories
Incomplete observations
```

### Uniqueness

```text
Duplicate rows
Duplicate observations
Candidate business keys
```

### Temporal Coverage

```text
Minimum date
Maximum date
Expected frequency
Missing dates
Historical gaps
```

### Numerical Quality

```text
Minimum values
Maximum values
Average
Median
Standard deviation
Unexpected zeros
Negative values
Potential outliers
```

### Categorical Quality

```text
Distinct products
Distinct regions
Distinct stores
Distinct fuel types
Distinct CPI categories
Distinct units
```

### Standardization Requirements

```text
Date normalization
Text normalization
Product normalization
Unit standardization
Geographic normalization
Category mapping
```

---

# Data Profiling Order

The source-discovery sequence follows business priority and source readiness:

```text
01. BCRD — USD/DOP Exchange Rates [initial profiling completed]
02. BCRD — CPI and Family Basket datasets [validated; pipelines implemented]
03. BCRD — Monetary Policy Rate [pending source-file profiling]
04. MICM — Dominican Fuel Prices [validated; pipelines implemented]
05. Pro Consumidor — Consumer / Basic Basket Prices [validated for Jul–Sep 2026; pipelines implemented]
06. Ministry of Agriculture — Agricultural Prices [preliminary profiling and reconciliation completed]
07. EIA — WTI / Brent external oil driver [pending]
```

BCRD source files already acquired for initial profiling comprise USD/DOP, national CPI, CPI by expenditure group, core CPI, regional CPI, family basket by quintile/national, and family basket by region. File acquisition and initial inspection do not imply that all detailed data-quality checks or incremental ingestion designs have been approved.

---

# Profiling Workflow

For each source:

```text
Official Source
      ↓
Download Actual Dataset
      ↓
Preserve Raw File
      ↓
Inspect File Structure
      ↓
Profile Dataset
      ↓
Identify Data Quality Issues
      ↓
Identify Candidate Business Key
      ↓
Determine Standardization Requirements
      ↓
Document Findings
      ↓
Feed Data Dictionary
      ↓
Feed Source-to-Target Mapping
```

---

# Project Lifecycle

The complete project workflow is:

```text
01 — Business Requirements
          ✓
          ↓
02 — Project Charter
          ✓
          ↓
03 — Business Questions & KPIs
          ✓
          ↓
04 — Data Source Assessment
          ✓
          ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      DATA PROFILING
        ← CURRENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
16 — Databricks SQL Analytics
          ↓
17 — Databricks Dashboard
          ↓
18 — Power BI Dashboard
          ↓
19 — Testing & Validation
          ↓
20 — Business Insights
          ↓
21 — Portfolio Publication
```

---

# Preliminary Lakehouse Architecture

The target implementation will follow a Medallion Architecture.

```text
OFFICIAL DATA SOURCES
          │
          ▼
     INGESTION
          │
          ▼
┌───────────────────────┐
│        BRONZE         │
│ Raw Source Data       │
│ Ingestion Metadata    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│        SILVER         │
│ Cleaned               │
│ Standardized          │
│ Validated             │
│ Deduplicated          │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│         GOLD          │
│ Business Metrics      │
│ KPI Models            │
│ Analytical Tables     │
└──────────┬────────────┘
           │
           ▼
    DATABRICKS SQL
           │
           ├──────────────► Databricks Dashboard
           │
           └──────────────► Power BI
```

The physical implementation of this architecture will only be finalized after Data Profiling and Data Modeling are completed.

---

# Preliminary Gold Layer

Candidate analytical datasets currently include:

```text
gold.inflation_metrics
gold.exchange_rate_metrics
gold.monetary_policy_metrics
gold.fuel_price_metrics
gold.consumer_price_metrics
gold.agricultural_price_metrics
gold.external_oil_metrics
gold.economic_relationship_metrics
```

Potential Phase 2 datasets:

```text
gold.energy_price_metrics
gold.housing_price_metrics
```

These names remain conceptual until the Data Model and Source-to-Target Mapping are finalized.

---

# Documentation Governance

Project documentation should evolve together with the implementation.

A document may initially be classified as:

```text
Draft
```

and later move through:

```text
Draft
  ↓
Reviewed
  ↓
Validated
  ↓
Final
```

The documentation should be updated whenever source profiling or implementation reveals information that changes an earlier assumption.

---

# Repository Principle

> **Business first. Data second. Architecture third. Implementation fourth.**

The project intentionally avoids beginning with Databricks notebooks or pipelines before understanding the business requirements and the actual data.

A second engineering principle now applies:

> **Do not design pipelines around assumptions. Design pipelines around validated data.**

Therefore:

```text
Business Requirements
        ↓
Business Questions
        ↓
KPIs
        ↓
Source Assessment
        ↓
Actual Data Profiling
        ↓
Data Dictionary
        ↓
Data Contracts
        ↓
Architecture
        ↓
Engineering
        ↓
Analytics
```

---

# Next Milestone

## Complete Source Discovery and Profiling Evidence

The immediate priorities are:

1. Obtain earlier Pro Consumidor reports to enable CON-006 to CON-008, and geographic detail for CON-009.
2. Automate the monthly download of the MEM annex (electricity) so the Job can run on schedule.
3. Assess Ministry of Agriculture agricultural-price datasets.
4. Profile the BCRD monetary policy rate source and verify incremental extraction options for BCRD data.
5. Consolidate source schemas, candidate business keys, quality rules, methodology notes, and KPI traceability as inputs to `05_Data_Dictionary`.

No dataset is **production approved** yet. Production approval requires the data dictionary, source-to-target mapping and solution architecture to be reviewed.

**GitHub policy:** commit source profiling notes, mappings, tests and code; preserve original source files outside the public repository until the data publication and repository policy is reviewed.

**Implementation gate:** pipelines are built source by source. A source enters Bronze development only after its profiling is complete (BCRD USD/DOP is the first). Production approval of any pipeline still requires the data dictionary, source-to-target mapping and solution architecture to be reviewed.

---

## Project Status

```text
Business Discovery       ██████████  COMPLETE
Source Assessment        ██████████  COMPLETE
Data Profiling           ██████░░░░  IN PROGRESS (illustrative)
Data Modeling            ░░░░░░░░░░  PLANNED
Databricks Engineering   ███████░░░  IN PROGRESS (BCRD, MICM, Pro Consumidor end to end + Job)
Analytics & BI           ████░░░░░░  IN PROGRESS (Power BI report, 7 pages)
```

---

**RD Economic & Financial Intelligence Platform**

*End-to-End Data Engineering & Business Intelligence Portfolio Project*
