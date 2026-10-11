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
| 10 | Databricks Environment Setup | Planned |
| 11 | Bronze Layer | Planned |
| 12 | Silver Layer | Planned |
| 13 | Gold Layer | Planned |
| 14 | Databricks Workflows | Planned |
| 15 | Monitoring & Data Quality | Planned |
| 16 | Databricks SQL Analytics | Planned |
| 17 | Databricks Dashboard | Planned |
| 18 | Power BI Dashboard | Planned |
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
| BCRD — CPI, CPI Groups, Core CPI, CPI Regions, Family Basket by Quintile and Region | Initial profiling completed; detailed validation pending | Six additional official spreadsheets obtained; monthly grain, base periods, methodology and wide-format normalization require documented checks |
| MICM — Fuel Prices | Profiling documented; reconciliation in progress | Official CSV and XLSX obtained; format differences, repeated periods and zero prices require resolution |
| Pro Consumidor — Consumer Prices | Not started | Next source-discovery priority |
| Ministry of Agriculture — Agricultural Prices | Not started | Source-format and historical coverage assessment pending |
| EIA — WTI / Brent | Not started | External driver only under RD-First governance |

**Current phase:** Data Discovery & Profiling  
**Next milestone:** Complete MICM reconciliation, assess Pro Consumidor and Agriculture datasets, and prepare evidence-based inputs for `05_Data_Dictionary` and `06_Source-to-Target Mapping`.

**Technical documentation:** [MICM Fuel Prices — Data Discovery & Profiling](../profiling/micm/README.md)

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
| Superintendencia de Electricidad — SIE | Electricity Tariffs | Dominican Republic | Phase 2 |
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
02. BCRD — CPI and Family Basket datasets [initial profiling completed]
03. BCRD — Monetary Policy Rate [pending source-file profiling]
04. MICM — Dominican Fuel Prices [reconciliation in progress]
05. Pro Consumidor — Consumer / Basic Basket Prices [next]
06. Ministry of Agriculture — Agricultural Prices [pending]
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

1. Resolve or explicitly document the MICM CSV/XLSX value discrepancies, repeated reporting periods, units and zero-value semantics. Do not assume one format is authoritative without verification.
2. Assess official Pro Consumidor consumer-price datasets and their coverage, grain, format and reuse constraints.
3. Assess Ministry of Agriculture agricultural-price datasets.
4. Profile the BCRD monetary policy rate source and verify incremental extraction options for BCRD data.
5. Consolidate source schemas, candidate business keys, quality rules, methodology notes, and KPI traceability as inputs to `05_Data_Dictionary`.

The MICM dataset is **not production approved**. The existence of source files or preliminary profiling is not evidence that all source values are reconciled.

**GitHub policy:** commit source profiling notes, mappings, tests and code; preserve original source files outside the public repository until the data publication and repository policy is reviewed.

**Implementation gate:** do not create Databricks catalogs, tables, notebooks or workflows until source profiling, data dictionary, source-to-target mapping and solution architecture have been reviewed.

---

## Project Status

```text
Business Discovery       ██████████  COMPLETE
Source Assessment        ██████████  COMPLETE
Data Profiling           ████░░░░░░  IN PROGRESS (illustrative)
Data Modeling            ░░░░░░░░░░  PLANNED
Databricks Engineering   ░░░░░░░░░░  PLANNED
Analytics & BI           ░░░░░░░░░░  PLANNED
```

---

**RD Economic & Financial Intelligence Platform**

*End-to-End Data Engineering & Business Intelligence Portfolio Project*
