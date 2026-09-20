# Data Source Assessment

## RD Economic & Financial Intelligence Platform

> **Assessment of official, public, reliable, and technically feasible data sources required to build the Dominican Republic Economic & Financial Intelligence Platform.**

---

## Document Information

| Attribute | Details |
|---|---|
| **Project Name** | RD Economic & Financial Intelligence Platform |
| **Document Type** | Data Source Assessment |
| **Document Version** | 1.0 |
| **Status** | Draft / Data Profiling Pending |
| **Project Type** | Data Engineering & Business Intelligence Case Study |
| **Primary Platform** | Databricks |
| **Architecture Approach** | Lakehouse / Medallion Architecture |
| **Geographic Scope** | Dominican Republic |
| **Project Owner** | Stanly Fernandez |
| **Repository** | `rd-economic-financial-intelligence` |
| **Detailed Working File** | `04_Data_Source_Assessment.xlsx` |

---

# Table of Contents

1. [Purpose](#1-purpose)
2. [Assessment Objectives](#2-assessment-objectives)
3. [RD-First Data Governance Principle](#3-rd-first-data-governance-principle)
4. [Source Selection Criteria](#4-source-selection-criteria)
5. [Source Assessment Summary](#5-source-assessment-summary)
6. [Banco Central de la República Dominicana](#6-banco-central-de-la-república-dominicana)
7. [MICM — Dominican Fuel Prices](#7-micm--dominican-fuel-prices)
8. [Pro Consumidor — Consumer Prices](#8-pro-consumidor--consumer-prices)
9. [Ministry of Agriculture — Agricultural Prices](#9-ministry-of-agriculture--agricultural-prices)
10. [SIE — Electricity Tariffs](#10-sie--electricity-tariffs)
11. [External Driver — International Oil](#11-external-driver--international-oil)
12. [Housing & Rental Data](#12-housing--rental-data)
13. [KPI-to-Source Traceability](#13-kpi-to-source-traceability)
14. [Data Ingestion Assessment](#14-data-ingestion-assessment)
15. [MVP Source Decision](#15-mvp-source-decision)
16. [Data Quality & Engineering Risks](#16-data-quality--engineering-risks)
17. [Preliminary Ingestion Strategy](#17-preliminary-ingestion-strategy)
18. [Source Governance](#18-source-governance)
19. [Data Profiling Requirements](#19-data-profiling-requirements)
20. [Definition of Done](#20-definition-of-done)
21. [Next Steps](#21-next-steps)

---

# 1. Purpose

The purpose of the **Data Source Assessment** is to determine whether the data required by the Business Questions and KPI Catalog can be obtained from reliable and technically sustainable sources.

The assessment connects:

```text
Business Question
        ↓
KPI
        ↓
Required Data
        ↓
Candidate Source
        ↓
Source Assessment
        ↓
Data Profiling
        ↓
Ingestion Strategy
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

The objective is to prevent technical implementation from beginning before the required data has been evaluated.

This document therefore acts as the bridge between:

```text
BUSINESS DISCOVERY
        ↓
DATA DISCOVERY
        ↓
TECHNICAL DESIGN
```

---

# 2. Assessment Objectives

The Data Source Assessment evaluates whether each candidate source can support the analytical requirements of the platform.

Each source is evaluated according to:

- Institution
- Dataset
- Geographic scope
- Source role
- Historical coverage
- Update frequency
- Data granularity
- Access mechanism
- File format
- Automation potential
- Expected data quality
- Schema stability
- Incremental ingestion feasibility
- KPI coverage
- Engineering complexity
- Legal and operational sustainability
- MVP relevance

The assessment also identifies:

- Sources suitable for the MVP
- Sources requiring additional investigation
- Sources better suited for Phase 2
- Sources that should be excluded
- External variables that may support Dominican economic analysis

---

# 3. RD-First Data Governance Principle

The platform follows an explicit:

## RD-First Rule

> **The RD Economic & Financial Intelligence Platform prioritizes data representing prices, economic indicators, markets, financial conditions, and cost-of-living conditions in the Dominican Republic.**

The primary analytical subject of the platform is:

```text
DOMINICAN REPUBLIC
```

The core datasets should therefore describe Dominican conditions.

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

## 3.1 International Data Rule

International datasets are not included simply because they are economically interesting.

International data may only be incorporated when it has a clear analytical relationship with a Dominican KPI.

The governance rule is:

```text
IF Geographic_Scope != "Dominican Republic"
AND Source_Role != "External Driver"

THEN

Exclude dataset from platform
```

Example of an accepted international variable:

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

WTI and Brent are therefore classified as:

```text
Geographic Scope = International
Source Role       = External Driver
```

They must never be presented as Dominican price data.

---

# 4. Source Selection Criteria

Candidate sources are evaluated across five major dimensions.

## 4.1 Business Relevance

The dataset must support at least one defined business question or KPI.

```text
Source
   ↓
KPI
   ↓
Business Question
```

Datasets without a clear analytical purpose should not be incorporated.

---

## 4.2 Geographic Relevance

Priority is given to:

```text
Dominican Republic data
```

International sources require explicit justification as external drivers.

---

## 4.3 Source Authority

Preferred sources include:

- Dominican government institutions
- Dominican regulatory agencies
- Dominican statistical institutions
- Official public datasets
- International government institutions when required for external drivers

Primary official sources are preferred over secondary aggregators.

---

## 4.4 Technical Feasibility

Preferred formats include:

```text
API
JSON
CSV
XLSX
ODS
```

Less desirable formats include:

```text
HTML
PDF
Manual publications
```

PDF-based sources are not automatically rejected, but they introduce additional extraction and validation complexity.

---

## 4.5 Historical Coverage

Historical depth is important for calculating:

```text
MoM
YoY
YTD
Moving Averages
Volatility
Seasonality
Correlation
Lag Analysis
52-Week High / Low
```

A dataset containing only current observations may therefore support monitoring but not all historical KPIs.

---

# 5. Source Assessment Summary

The current assessment identified the following principal sources.

| Source ID | Institution | Domain | Geography | Role | MVP |
|---|---|---|---|---|---|
| SRC-001 | BCRD | CPI | Dominican Republic | Core Domestic | Yes |
| SRC-002 | BCRD | CPI Groups | Dominican Republic | Core Domestic | Yes |
| SRC-003 | BCRD | Core Inflation | Dominican Republic | Core Domestic | Yes |
| SRC-004 | BCRD | USD/DOP | Dominican Republic | Core Domestic | Yes |
| SRC-005 | BCRD | Monetary Policy | Dominican Republic | Core Domestic | Yes |
| SRC-006 | MICM | Fuel Prices | Dominican Republic | Core Domestic | Yes |
| SRC-007 | Pro Consumidor | Consumer Prices | Dominican Republic | Core Domestic | Yes |
| SRC-008 | Pro Consumidor | Price Surveys | Dominican Republic | Support / Fallback | Support |
| SRC-009 | Ministry of Agriculture | Producer Prices | Dominican Republic | Core Domestic | Yes |
| SRC-010 | Ministry of Agriculture | Wholesale Prices | Dominican Republic | Core Domestic | Yes |
| SRC-011 | Ministry of Agriculture | Retail Prices | Dominican Republic | Core Domestic | Yes |
| SRC-012 | Ministry of Agriculture | Interdiary Prices | Dominican Republic | Core Domestic | Yes |
| SRC-013 | Ministry of Agriculture | Supermarket Prices | Dominican Republic | Core Domestic | Yes |
| SRC-014 | SIE | Electricity Tariffs | Dominican Republic | Core Domestic | Phase 2 |
| SRC-015 | U.S. EIA | WTI / Brent | International | External Driver | Yes — External |
| SRC-016 | TBD | Housing / Rentals | Dominican Republic | Core Domestic | Deferred |

---

# 6. Banco Central de la República Dominicana

The **Banco Central de la República Dominicana (BCRD)** is expected to be the primary source for the macroeconomic and financial component of the platform.

The initial BCRD datasets include:

```text
BCRD
│
├── Consumer Price Index
├── CPI by Expenditure Group
├── Core / Underlying Inflation
├── USD/DOP Exchange Rate
└── Monetary Policy Rate
```

---

## 6.1 Consumer Price Index

### Source ID

```text
SRC-001
```

### Domain

```text
Inflation & CPI
```

### Geographic Scope

```text
Dominican Republic
```

### Source Role

```text
Core Domestic
```

### Expected Frequency

```text
Monthly
```

### Supported KPIs

```text
INF-001 CPI Index
INF-002 Monthly Inflation
INF-003 YoY Inflation
INF-004 YTD Inflation
```

### Preliminary Assessment

```text
Business Value:          HIGH
Historical Value:        HIGH
Automation Potential:    HIGH
Data Quality Risk:       LOW
MVP Decision:            INCLUDE
```

Before implementation, the actual downloaded dataset must be profiled.

---

# 6.2 CPI by Expenditure Group

### Source ID

```text
SRC-002
```

Supports:

```text
INF-006 Inflation by Expenditure Group
```

Expected analytical grain:

```text
Month
×
Expenditure Group
```

Potential engineering consideration:

Historical CPI classifications or base periods may introduce changes in category taxonomy.

This must be evaluated during Data Profiling.

---

# 6.3 Core / Underlying Inflation

### Source ID

```text
SRC-003
```

Supports:

```text
INF-005 Core Inflation
```

The platform should preserve the official methodology used by the source.

The project should not independently redefine core inflation.

---

# 6.4 USD/DOP Exchange Rate

### Source ID

```text
SRC-004
```

### Domain

```text
Foreign Exchange
```

### Geographic Scope

```text
Dominican Republic
```

The USD/DOP exchange rate represents the value of the Dominican peso relative to the U.S. dollar and therefore remains a domestic analytical indicator.

Potential observations include:

```text
Date
Buy Rate
Sell Rate
Appreciation / Depreciation
```

Supported KPIs:

```text
FX-001 USD/DOP Buy Rate
FX-002 USD/DOP Sell Rate
FX-003 Daily FX Change
FX-004 MoM FX Change
FX-005 YoY FX Change
FX-006 YTD FX Change
FX-007 30-Day Moving Average
FX-008 52-Week High
FX-009 52-Week Low
```

### Assessment

```text
Source Readiness:        HIGH
Automation Potential:   HIGH
Engineering Complexity: LOW
MVP:                    YES
```

This dataset is a strong candidate for one of the first ingestion pipelines implemented in Databricks.

---

# 6.5 Monetary Policy Rate

### Source ID

```text
SRC-005
```

### Domain

```text
Monetary Policy
```

Supported KPIs:

```text
MON-001 Monetary Policy Rate
MON-002 Policy Rate Change
MON-003 Policy Rate YTD Change
MON-004 Inflation–Policy Rate Spread
MON-005 Real Policy Rate Proxy
```

The natural structure should preserve policy-rate effective dates rather than artificially generating new rate observations when no policy change occurred.

Potential structure:

```text
Effective Date
Policy Rate
```

A monthly analytical snapshot may later be derived in Silver or Gold.

---

# 7. MICM — Dominican Fuel Prices

The **Ministerio de Industria, Comercio y Mipymes (MICM)** is the primary candidate source for official Dominican fuel prices.

### Source ID

```text
SRC-006
```

### Geographic Scope

```text
Dominican Republic
```

### Domain

```text
Fuel Market
```

### Expected Frequency

```text
Weekly
```

Potential fuel categories include:

```text
Premium Gasoline
Regular Gasoline
Premium Diesel
Regular Diesel
LPG
Natural Gas
Other Published Fuels
```

The actual taxonomy will be derived from the source.

Supported KPIs:

```text
FUEL-001 Current Fuel Price
FUEL-002 Previous Week Price
FUEL-003 Weekly Price Change
FUEL-004 Weekly Price Change %
FUEL-005 Monthly Price Change %
FUEL-006 YoY Price Change %
FUEL-007 YTD Price Change %
FUEL-008 4-Week Moving Average
FUEL-009 12-Week Moving Average
FUEL-010 52-Week High
FUEL-011 52-Week Low
FUEL-012 Fuel Price Volatility
```

### Assessment

```text
Business Value:          HIGH
RD Relevance:            HIGH
Historical Value:        HIGH
Automation Potential:    MEDIUM
Engineering Complexity:  MEDIUM
MVP Decision:            INCLUDE
```

### Primary Risk

The major uncertainty is not the economic relevance of the data.

The primary issue is:

```text
Historical publication format consistency
```

Before designing ingestion, representative historical files should be collected and compared.

---

# 8. Pro Consumidor — Consumer Prices

Pro Consumidor is a primary candidate source for consumer and basic-basket price analysis.

### Primary Source

```text
SRC-007
```

### Supporting Source

```text
SRC-008
```

### Geographic Scope

```text
Dominican Republic
```

Potential structured formats include:

```text
XLSX
CSV
ODS
JSON
```

Structured formats should be preferred over PDF reports.

---

## 8.1 Supported KPIs

Potentially supported:

```text
CON-001 Average Product Price
CON-002 Median Product Price
CON-003 Minimum Product Price
CON-004 Maximum Product Price
CON-005 Product MoM %
CON-006 Product YoY %
CON-007 Product YTD %
CON-008 Product Price Volatility
CON-009 Regional Price Difference %
CON-010 Category Price Index
```

However, not all KPIs should automatically be considered validated.

---

## 8.2 Historical Dependency

Metrics such as:

```text
YoY
YTD
Seasonality
Long-term volatility
```

require comparable historical observations.

Therefore:

```text
Current Price KPIs → High feasibility

Historical Change KPIs → Dependent on historical comparability
```

This will be tested during Data Profiling.

---

## 8.3 Product Comparability

Consumer products may differ by:

```text
Product
Brand
Presentation
Quantity
Unit
Store
Location
Date
```

Therefore:

```text
Rice Brand A — 1 lb
```

must not automatically be treated as equivalent to:

```text
Rice Brand B — 5 lb
```

Standardization may eventually require normalized metrics such as:

```text
DOP per pound
DOP per kilogram
DOP per liter
DOP per unit
```

where economically appropriate.

---

# 9. Ministry of Agriculture — Agricultural Prices

Agricultural data represents one of the richest potential domains identified during the assessment.

Potential layers include:

```text
Agricultural Price System
│
├── Producer Prices
├── Wholesale Prices
├── Retail Prices
├── Interdiary Market Prices
└── Supermarket Prices
```

This creates the possibility of analyzing different stages of the Dominican agricultural price chain.

---

# 9.1 Producer Prices

### Source ID

```text
SRC-009
```

Potential analytical grain:

```text
Period
×
Product
×
Region
```

This layer represents prices closer to agricultural production.

---

# 9.2 Wholesale Prices

### Source ID

```text
SRC-010
```

Potential grain:

```text
Period
×
Product
×
Wholesale Market
×
Region
```

---

# 9.3 Retail Prices

### Source ID

```text
SRC-011
```

Potential grain:

```text
Period
×
Product
×
Retail Market
×
Region
```

---

# 9.4 Interdiary Prices

### Source ID

```text
SRC-012
```

This dataset may provide higher-frequency observations than the monthly historical datasets.

Potential use cases include:

```text
Short-term price monitoring
Price volatility
Market differences
Regional differences
Rapid price movements
```

---

# 9.5 Supermarket Prices

### Source ID

```text
SRC-013
```

Potential grain:

```text
Period
×
Product
×
Supermarket Chain
```

This source may provide a useful analytical bridge between:

```text
Agricultural Prices
        ↓
Retail Distribution
        ↓
Consumer Prices
```

---

# 9.6 Agricultural KPIs

These sources potentially support:

```text
AGR-001 Average Agricultural Price
AGR-002 MoM Price Change %
AGR-003 YoY Price Change %
AGR-004 YTD Price Change %
AGR-005 Price Volatility
AGR-006 Seasonal Price Index
AGR-007 Regional Price Difference %
```

### Assessment

```text
RD Relevance:            HIGH
Historical Coverage:     HIGH
Business Value:          HIGH
Automation Potential:    HIGH / MEDIUM
Engineering Complexity:  MEDIUM
MVP Decision:            INCLUDE
```

The main engineering challenge is expected to be standardization.

Potential problems include:

```text
Product naming
Unit differences
Market classifications
Regional naming
File structure differences
Missing periods
```

---

# 10. SIE — Electricity Tariffs

The **Superintendencia de Electricidad (SIE)** is the primary candidate source for regulated electricity tariffs.

### Source ID

```text
SRC-014
```

### Geographic Scope

```text
Dominican Republic
```

Potential dimensions include:

```text
Period
Distributor
Tariff Category
Consumption Block
Price per kWh
```

Potential distributors include:

```text
EDENORTE
EDESUR
EDEESTE
```

Supported KPIs:

```text
ENE-001 Electricity Tariff
ENE-002 MoM Tariff Change %
ENE-003 YoY Tariff Change %
ENE-004 YTD Tariff Change %
ENE-005 Average Cost per kWh
```

### Assessment

```text
RD Relevance:            HIGH
Source Authority:        HIGH
Engineering Complexity:  HIGHER
Automation Potential:    MEDIUM / LOW
MVP Decision:            PHASE 2
```

The primary challenge is that tariff information may require processing regulatory documents and understanding tariff categories and consumption blocks.

Therefore, electricity remains valuable but is not required for the initial MVP.

---

# 11. External Driver — International Oil

### Source ID

```text
SRC-015
```

### Source Role

```text
External Driver
```

### Geographic Scope

```text
International
```

Potential benchmarks:

```text
WTI
Brent
```

These prices are not considered Dominican data.

Their inclusion is justified only because they may provide useful context for analyzing Dominican fuel prices.

---

## 11.1 Supported KPIs

```text
OIL-001 WTI Price
OIL-002 Brent Price
OIL-003 WTI WoW %
OIL-004 Brent WoW %
OIL-005 WTI MoM %
OIL-006 Brent MoM %
OIL-007 WTI 30-Day Moving Average
OIL-008 Brent 30-Day Moving Average
```

These indicators should be presented as:

```text
External Market Indicators
```

not Dominican economic indicators.

---

## 11.2 Relationship Analysis

Potential relationships:

```text
WTI_t   ↔ Dominican Fuel_t
WTI_t   ↔ Dominican Fuel_t+1
WTI_t   ↔ Dominican Fuel_t+2
WTI_t   ↔ Dominican Fuel_t+4

Brent_t ↔ Dominican Fuel_t
Brent_t ↔ Dominican Fuel_t+1
Brent_t ↔ Dominican Fuel_t+2
Brent_t ↔ Dominican Fuel_t+4
```

Supported relationship KPIs:

```text
REL-001 Oil/Fuel Correlation
REL-002 Oil/Fuel Lag Correlation T+1
REL-003 Oil/Fuel Lag Correlation T+2
REL-004 Oil/Fuel Lag Correlation T+4
```

The frequency must be aligned before calculating these relationships.

For example:

```text
Daily Oil
    ↓
Weekly Aggregation
    ↓
Weekly Dominican Fuel
```

---

## Analytical Limitation

```text
Correlation ≠ Causation
```

These metrics should be interpreted as exploratory relationships.

They should not automatically be presented as evidence that international oil price movements caused a specific Dominican fuel-price movement.

---

# 12. Housing & Rental Data

### Source ID

```text
SRC-016
```

### Geographic Scope

```text
Dominican Republic
```

### Initial KPI

```text
HOU-001 Median Rental Asking Price
```

### Current Status

```text
Pending Source Validation
```

### MVP Decision

```text
DEFER
```

At this stage, a sufficiently sustainable source combining:

```text
Historical coverage
Location
Property characteristics
Consistent observations
Legal automated access
```

has not yet been approved.

The project will not use unauthorized scraping as a workaround.

This domain may be reconsidered during Phase 2.

---

# 13. KPI-to-Source Traceability

The current mapping is:

| Domain | KPI Range | Primary Source | Status |
|---|---|---|---|
| Inflation | INF-001–INF-004 | SRC-001 | MVP |
| Inflation Groups | INF-006 | SRC-002 | MVP |
| Core Inflation | INF-005 | SRC-003 | MVP |
| Foreign Exchange | FX-001–FX-009 | SRC-004 | MVP |
| Monetary Policy | MON-001–MON-005 | SRC-005 + SRC-001 | MVP |
| Fuel | FUEL-001–FUEL-012 | SRC-006 | MVP |
| International Oil | OIL-001–OIL-008 | SRC-015 | External Driver |
| Oil/Fuel Relationships | REL-001–REL-004 | SRC-015 + SRC-006 | MVP / Phase 2 |
| Consumer Prices | CON-001–CON-010 | SRC-007 + SRC-013 | Conditional |
| Agricultural Prices | AGR-001–AGR-007 | SRC-009–SRC-013 | MVP |
| Electricity | ENE-001–ENE-005 | SRC-014 | Phase 2 |
| Housing | HOU-001 | SRC-016 | Deferred |

---

# 14. Data Ingestion Assessment

Different sources will require different ingestion strategies.

The platform should not force every dataset into the same ingestion mechanism.

Potential patterns include:

```text
Structured File
     ↓
Scheduled Download
     ↓
Bronze

API / Structured Endpoint
     ↓
Incremental Request
     ↓
Bronze

Periodic Publication
     ↓
New File Detection
     ↓
Bronze

PDF
     ↓
Document Retrieval
     ↓
Extraction
     ↓
Validation
     ↓
Bronze / Staging
```

---

## Preliminary Source Patterns

| Source | Preferred Input | Expected Pattern |
|---|---|---|
| BCRD CPI | Structured export | Scheduled ingestion |
| BCRD FX | Excel / structured | Daily ingestion |
| BCRD TPM | Structured series | Event-aware ingestion |
| MICM Fuel | Publication / file | Weekly ingestion |
| Pro Consumidor | CSV / JSON | Structured file ingestion |
| Agriculture | XLSX / CSV | File ingestion |
| International Oil | Structured data | Daily external-driver ingestion |
| SIE | PDF | Document extraction — Phase 2 |
| Housing | TBD | Deferred |

These strategies remain preliminary until actual files are profiled.

---

# 15. MVP Source Decision

Based on business value, RD relevance, data availability, historical depth, and engineering effort, the recommended MVP is:

```text
RD ECONOMIC & FINANCIAL INTELLIGENCE PLATFORM

MVP
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
├── Consumer / Basic Basket
│      └── Pro Consumidor
│
├── Agricultural Prices
│      └── Ministry of Agriculture
│
└── External Driver
       └── WTI / Brent
```

---

## Phase 2

```text
Electricity
    └── SIE

Housing
    └── Source TBD

Advanced Cross-Domain Analysis
```

This provides sufficient scope for a substantial end-to-end Data Engineering and Business Intelligence platform without unnecessarily increasing the first implementation phase.

---

# 16. Data Quality & Engineering Risks

The source assessment identified several risks that must be tested during Data Profiling.

---

## 16.1 Schema Changes

Historical files may not always contain identical:

```text
Column names
Column order
Data types
Categories
Units
File structures
```

---

## 16.2 Product Naming

The same product may appear as:

```text
Platano
Plátano
Platano Barahonero
Plátano Barahonero
```

Potential standardization will be required.

---

## 16.3 Unit Standardization

Examples:

```text
lb
pound
kg
unit
dozen
gallon
liter
```

These cannot be blindly compared.

A canonical unit strategy will eventually be required.

---

## 16.4 Missing Observations

Government publications may not contain observations for every expected period.

Potential controls:

```text
Missing date detection
Missing publication alert
Missing product observation
Incomplete regional coverage
```

---

## 16.5 Duplicates

Potential business keys must be evaluated.

Example:

```text
Date
+
Product
+
Store
+
Location
+
Presentation
```

may form a logical key for some consumer datasets.

The actual key must be derived from the data.

---

## 16.6 Historical Taxonomy Changes

Categories may change over time.

Examples:

```text
CPI categories
Agricultural product names
Fuel categories
Regional classifications
```

Historical standardization should preserve source lineage.

---

# 17. Preliminary Ingestion Strategy

The eventual Databricks pipeline may follow:

```text
OFFICIAL SOURCES
       ↓
INGESTION
       ↓
BRONZE
       ↓
VALIDATION
       ↓
SILVER
       ↓
GOLD
       ↓
DATABRICKS SQL
       ↓
POWER BI
```

However, ingestion mechanisms will vary by source.

---

## 17.1 Bronze Principle

Bronze should preserve the original source as closely as practical.

Potential metadata:

```text
source_id
source_url
source_file
ingestion_timestamp
source_publication_date
file_hash
batch_id
ingestion_status
```

Business transformations should generally not occur in Bronze.

---

## 17.2 Silver Responsibilities

Silver will eventually handle:

```text
Schema normalization
Data type enforcement
Date normalization
Product normalization
Unit standardization
Duplicate handling
Null handling
Category mapping
Geographic normalization
Data-quality validation
```

---

## 17.3 Gold Responsibilities

Gold will contain business-ready analytical metrics.

Candidate datasets currently include:

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

Phase 2 candidates:

```text
gold.energy_price_metrics
gold.housing_price_metrics
```

These remain conceptual until profiling and data modeling are completed.

---

# 18. Source Governance

Each source should eventually maintain metadata such as:

```text
source_id
institution
dataset_name
source_role
geographic_scope
source_url
access_method
format
frequency
expected_grain
owner
active_flag
last_successful_ingestion
```

Potential future metadata table:

```text
metadata.data_sources
```

This will allow pipelines to maintain traceability from source to analytical output.

---

## 18.1 External Driver Governance

External sources require:

```text
Source Role = External Driver
```

and must have:

```text
Linked Dominican KPI
        +
Documented analytical purpose
```

Otherwise they should not be included.

---

# 19. Data Profiling Requirements

The completion of Source Assessment does **not** mean the physical datasets have been fully validated.

The next technical activity is:

# Data Profiling

Actual source files must be downloaded and inspected.

For each dataset, profiling should evaluate:

### Schema

```text
Column names
Column count
Data types
Column order
Nested structures
```

### Completeness

```text
Row count
Null count
Missing periods
Missing categories
```

### Uniqueness

```text
Duplicate rows
Candidate business keys
Duplicate observations
```

### Temporal Coverage

```text
Minimum date
Maximum date
Missing dates
Frequency consistency
```

### Numerical Validation

```text
Minimum value
Maximum value
Average
Median
Standard deviation
Outliers
Negative values
Unexpected zero values
```

### Categorical Validation

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
Unit conversion
Location normalization
Category mapping
```

---

# 20. Definition of Done

The Data Source Assessment is considered complete for the Data Discovery stage when:

- Candidate sources have been identified.
- Geographic scope has been classified.
- Domestic and external sources are separated.
- Each source has a defined analytical role.
- Sources are mapped to KPIs.
- Historical coverage has been assessed at a preliminary level.
- Expected update frequency is documented.
- Expected granularity is documented.
- Available formats have been assessed.
- Automation potential has been evaluated.
- Major engineering risks have been identified.
- MVP / Phase 2 decisions have been documented.
- External drivers have documented justification.
- Unsupported sources have been deferred rather than artificially incorporated.
- The detailed Excel assessment exists.
- The GitHub-readable Markdown assessment exists.
- Datasets requiring physical profiling have been identified.

---

# 21. Next Steps

The project has now progressed through:

```text
01 — Business Requirements Document
              COMPLETE
                  ↓
02 — Project Charter
              COMPLETE
                  ↓
03 — Business Questions & KPI Catalog
              COMPLETE
                  ↓
04 — Data Source Assessment
              COMPLETE
                  ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA PROFILING
              NEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  ↓
05 — Data Dictionary
                  ↓
06 — Source-to-Target Mapping
                  ↓
07 — Solution Architecture
                  ↓
08 — Data Model
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

---

## Immediate Next Activity

The next activity is **Data Profiling**.

The recommended profiling order is:

```text
1. BCRD — USD/DOP
2. BCRD — CPI
3. BCRD — Monetary Policy Rate
4. MICM — Fuel Prices
5. Pro Consumidor — Consumer Prices
6. Ministry of Agriculture — Agricultural Prices
7. WTI / Brent — External Driver
```

The first profiling exercise should use **USD/DOP** because it provides a relatively clear and manageable dataset for establishing the profiling methodology that will later be reused across more complex sources.

For every source, the project should:

```text
Download Actual Dataset
        ↓
Preserve Raw File
        ↓
Inspect Structure
        ↓
Profile Data
        ↓
Document Findings
        ↓
Define Candidate Business Key
        ↓
Define Data Quality Rules
        ↓
Update Source Assessment
        ↓
Feed Data Dictionary
```

Only after profiling the actual datasets should the project finalize Bronze and Silver table designs.

---

# Document History

| Version | Date | Description | Author |
|---|---|---|---|
| **1.0** | September 2026 | Initial Data Source Assessment | Stanly Fernandez |

---

# Related Project Documentation

| Document | Format | Status |
|---|---|---|
| `01_Business_Requirements_Document` | DOCX / Markdown | Complete |
| `02_Project_Charter` | DOCX / Markdown | Complete |
| `03_Business_Questions_KPI_Catalog` | XLSX / Markdown | Complete |
| `04_Data_Source_Assessment` | XLSX / Markdown | Complete |
| `05_Data_Dictionary` | TBD | Planned |
| `06_Source_to_Target_Mapping` | TBD | Planned |
| `07_Solution_Architecture` | TBD | Planned |
| `08_Data_Model` | TBD | Planned |
| `09_Data_Quality_Rules` | TBD | Planned |

---

# Engineering Principle

> **Do not design pipelines around assumptions. Design pipelines around validated data.**

The project therefore follows:

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
Data Contract
        ↓
Architecture
        ↓
Engineering
        ↓
Analytics
```

This ensures that the technical implementation remains directly connected to measurable business requirements and validated source data.

---

**RD Economic & Financial Intelligence Platform**  
*End-to-End Data Engineering & Business Intelligence Portfolio Project*
