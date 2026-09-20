# Business Requirements Document

## RD Economic & Financial Intelligence Platform

> **End-to-End Databricks Lakehouse Platform for Economic, Financial, Inflation, and Cost-of-Living Analytics in the Dominican Republic**

---

## Document Information

| Attribute | Details |
|---|---|
| **Project Name** | RD Economic & Financial Intelligence Platform |
| **Document Type** | Business Requirements Document (BRD) |
| **Document Version** | 1.0 |
| **Status** | Draft |
| **Project Start** | September 2026 |
| **Project Type** | Data Engineering & Business Intelligence Case Study |
| **Target Platform** | Databricks |
| **Architecture Approach** | Lakehouse / Medallion Architecture |
| **Geographic Scope** | Dominican Republic |
| **Project Owner** | Stanly Fernandez |
| **Repository** | `rd-economic-financial-intelligence` |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Problem](#2-business-problem)
3. [Business Objective](#3-business-objective)
4. [Project Goals](#4-project-goals)
5. [Target Users and Stakeholders](#5-target-users-and-stakeholders)
6. [Business Domains](#6-business-domains)
7. [Key Business Questions](#7-key-business-questions)
8. [High-Level KPIs](#8-high-level-kpis)
9. [Functional Requirements](#9-functional-requirements)
10. [Non-Functional Requirements](#10-non-functional-requirements)
11. [Data Refresh Requirements](#11-data-refresh-requirements)
12. [High-Level Deliverables](#12-high-level-deliverables)
13. [Project Scope](#13-project-scope)
14. [Assumptions](#14-assumptions)
15. [Constraints](#15-constraints)
16. [Success Criteria](#16-success-criteria)
17. [Project Phases](#17-project-phases)
18. [Requirements Traceability](#18-requirements-traceability)
19. [Document Approval](#19-document-approval)
20. [Next Steps](#20-next-steps)

---

# 1. Executive Summary

The **RD Economic & Financial Intelligence Platform** is an end-to-end Data Engineering and Business Intelligence initiative designed to centralize, process, analyze, and visualize key economic, financial, monetary, energy, consumer-price, and cost-of-living indicators for the Dominican Republic.

Economic information relevant to households, businesses, analysts, and decision-makers is currently distributed across multiple institutions, websites, files, reports, and publication formats.

The proposed platform will consolidate selected data sources into a centralized **Databricks Lakehouse**, where data will be ingested, validated, standardized, transformed, and prepared for analytical consumption.

The platform is expected to support:

- Historical economic analysis
- Inflation monitoring
- Foreign exchange analysis
- Monetary policy analysis
- Fuel and international oil analysis
- Consumer-price monitoring
- Agricultural-price analysis
- Energy-cost analysis
- Cost-of-living analysis
- Cross-domain economic analysis

The final solution will provide curated analytical datasets for **Databricks SQL**, interactive dashboards, and **Power BI**.

---

# 2. Business Problem

Economic and financial information related to the Dominican Republic is distributed across multiple independent sources.

These sources may differ in:

- Publication format
- Historical coverage
- Update frequency
- Data granularity
- Measurement units
- Geographic coverage
- Naming conventions
- Data structures
- Access methods

For example, an analyst attempting to understand the evolution of the Dominican cost of living may need to independently obtain information about:

- Inflation
- Exchange rates
- Monetary policy
- Fuel prices
- International oil prices
- Consumer products
- Agricultural products
- Electricity
- Housing

The absence of a centralized analytical layer makes it more difficult to compare these variables consistently over time.

The business problem can therefore be summarized as:

> **Economic and cost-of-living information for the Dominican Republic is fragmented across multiple sources, limiting efficient historical analysis, cross-domain comparison, and centralized monitoring.**

---

# 3. Business Objective

The primary business objective is to create a centralized economic intelligence platform capable of transforming fragmented public and external data into reliable, structured, and reusable analytical information.

The platform should enable users to:

- Monitor important economic indicators.
- Analyze historical trends.
- Compare economic variables.
- Identify significant price movements.
- Evaluate inflationary pressures.
- Monitor foreign exchange movements.
- Analyze fuel and international oil markets.
- Evaluate selected cost-of-living components.
- Identify seasonality and volatility.
- Produce consistent economic KPIs.
- Consume analytical information through interactive dashboards.

---

# 4. Project Goals

The project has the following high-level goals:

1. Identify relevant and reliable economic data sources.

2. Centralize selected datasets within a Databricks Lakehouse.

3. Preserve historical observations.

4. Standardize heterogeneous datasets.

5. Implement a scalable Medallion Architecture.

6. Develop automated ingestion processes where technically possible.

7. Implement data-quality validation.

8. Create reusable analytical datasets.

9. Define and calculate standardized economic KPIs.

10. Enable cross-domain economic analysis.

11. Automate recurring data-processing workflows.

12. Develop Databricks SQL analytical capabilities.

13. Develop interactive Databricks dashboards.

14. Develop Power BI dashboards.

15. Maintain technical and business documentation.

16. Create a reproducible end-to-end Data Engineering portfolio project.

---

# 5. Target Users and Stakeholders

The platform is designed as a portfolio case study; therefore, the following represent potential users rather than confirmed organizational stakeholders.

| User / Stakeholder | Primary Need |
|---|---|
| **Executive / Decision Maker** | High-level economic overview |
| **Economic Analyst** | Macroeconomic trends and historical analysis |
| **Financial Analyst** | FX, interest rates, monetary indicators |
| **Banking Analyst** | Monetary and financial conditions |
| **Risk Analyst** | Volatility and economic-risk indicators |
| **Business Analyst** | Business trends and KPI interpretation |
| **Data Analyst** | Clean analytical datasets |
| **BI Analyst** | Reporting and dashboard datasets |
| **Data Engineer** | Reliable data pipelines and data models |
| **Data Architect** | Scalable architecture and governance |

---

# 6. Business Domains

## 6.1 Inflation & Consumer Price Index

The platform should support analysis of:

- Consumer Price Index (CPI)
- Monthly inflation
- Year-over-year inflation
- Year-to-date inflation
- Core inflation, where available
- Inflation by expenditure group
- Historical inflation trends

Potential analysis should allow users to identify which categories are experiencing the greatest price changes.

---

## 6.2 Foreign Exchange

The platform should support analysis of relevant foreign exchange indicators.

Potential variables include:

- USD/DOP exchange rate
- Buy rate
- Sell rate
- EUR/DOP where reliable information is available
- Daily changes
- Monthly changes
- Year-over-year changes
- Year-to-date changes
- Moving averages
- Historical highs and lows
- Dominican peso appreciation/depreciation

---

## 6.3 Monetary & Financial Indicators

The platform should support analysis of selected monetary and financial indicators.

Potential indicators include:

- Monetary Policy Rate
- Interest rates
- Policy-rate changes
- Basis-point movements
- Monetary policy trends
- Monetary Policy Rate versus inflation
- Real policy-rate proxy

Additional indicators may be incorporated depending on data availability and business relevance.

---

## 6.4 Fuel Market

The platform should support historical analysis of Dominican fuel prices.

Potential fuel categories include:

- Premium gasoline
- Regular gasoline
- Premium diesel
- Regular diesel
- LPG
- Natural gas
- Other relevant fuel products

Potential analytical metrics include:

- Current price
- Previous-period price
- Weekly price change
- Weekly percentage change
- Monthly percentage change
- Year-over-year percentage change
- Year-to-date percentage change
- Moving averages
- Historical highs
- Historical lows
- Price volatility

---

## 6.5 International Oil Market

The platform should incorporate selected international oil benchmarks.

Initial benchmarks include:

- West Texas Intermediate (WTI)
- Brent crude oil

The platform should enable comparison between international oil prices and Dominican fuel prices.

Potential analytical relationships include:

- WTI versus domestic fuel prices
- Brent versus domestic fuel prices
- Oil-price changes versus fuel-price changes
- Lagged relationships between international oil and local fuel prices
- Interaction between international oil prices and USD/DOP

---

## 6.6 Basic Household Basket & Consumer Products

Where sufficiently granular and reliable information is available, the platform should support consumer-product analysis.

Potential attributes include:

- Product
- Category
- Subcategory
- Brand
- Presentation
- Quantity
- Unit of measure
- Price
- Store or establishment
- Municipality
- Province
- Region
- Collection date

Potential analysis includes:

- Average price
- Median price
- Minimum price
- Maximum price
- Monthly change
- Year-over-year change
- Year-to-date change
- Price volatility
- Seasonality
- Geographic price differences

---

## 6.7 Agricultural Products

The platform should evaluate the availability of agricultural-price information.

Potential products include:

- Rice
- Plantains
- Bananas
- Chicken
- Eggs
- Beans
- Potatoes
- Tomatoes
- Onions
- Garlic
- Other relevant products

Potential analysis includes:

- Historical price trends
- Monthly changes
- Annual changes
- Volatility
- Seasonality
- Geographic variation

---

## 6.8 Energy & Electricity

Where reliable historical information is available, the platform should support analysis of:

- Electricity tariffs
- Cost per kWh
- Tariff categories
- Historical tariff changes
- Selected energy-cost indicators

The exact analytical scope will depend on the results of the Data Source Assessment.

---

## 6.9 Housing & Rental Market

Housing and rental information may be incorporated as a future analytical domain.

Potential attributes include:

- Rental price
- Property type
- Bedrooms
- Bathrooms
- Municipality
- Sector
- Geographic area
- Observation date

Housing functionality will only be implemented when a legally and technically appropriate source is identified.

---

# 7. Key Business Questions

The platform should help answer questions including:

## Inflation

- How is inflation evolving in the Dominican Republic?
- What is the monthly inflation rate?
- What is the year-over-year inflation rate?
- Which expenditure groups are experiencing the greatest price changes?
- How has core inflation evolved?

## Foreign Exchange

- How has USD/DOP evolved?
- Is the Dominican peso appreciating or depreciating?
- What are the short-term exchange-rate trends?
- What are the long-term exchange-rate trends?
- How do exchange-rate movements compare with inflation?

## Monetary Policy

- How has the Monetary Policy Rate evolved?
- How many basis points has the rate changed?
- How does monetary policy compare with inflation?
- How has the real policy-rate proxy evolved?

## Fuel & Oil

- How have Dominican fuel prices changed?
- Which fuel has experienced the greatest percentage increase?
- How do Dominican fuel prices compare with WTI?
- How do Dominican fuel prices compare with Brent?
- Is there evidence of lagged relationships between international oil prices and local fuel prices?
- How does USD/DOP interact with international oil and domestic fuel prices?

## Consumer Products

- Which consumer products have increased most in price?
- Which products have decreased?
- Which products are most volatile?
- Which products exhibit seasonal patterns?
- Which geographic areas have higher prices?

## Agricultural Products

- Which agricultural products have increased most?
- Which products are most volatile?
- Which products exhibit seasonality?
- How do prices differ geographically?

## Cost of Living

- How is the overall cost-of-living environment changing?
- Which categories are contributing most to household cost pressures?
- How are food, fuel, electricity, FX, inflation, and housing indicators evolving together?

---

# 8. High-Level KPIs

Detailed KPI definitions are maintained in the project's **Business Questions & KPI Catalog**.

High-level KPI categories include:

## Inflation KPIs

- CPI Index
- Monthly Inflation %
- YoY Inflation %
- YTD Inflation %
- Core Inflation %
- Inflation by Expenditure Group

## Foreign Exchange KPIs

- USD/DOP Buy Rate
- USD/DOP Sell Rate
- Daily FX Change %
- MoM FX Change %
- YoY FX Change %
- YTD FX Change %
- Moving Average
- 52-Week High
- 52-Week Low

## Monetary KPIs

- Monetary Policy Rate
- Policy Rate Change
- Policy Rate YTD Change
- Inflation–Policy Rate Spread
- Real Policy Rate Proxy

## Fuel KPIs

- Current Fuel Price
- Weekly Price Change
- Weekly Price Change %
- Monthly Price Change %
- YoY Price Change %
- YTD Price Change %
- Moving Averages
- 52-Week High / Low
- Fuel Price Volatility

## Oil KPIs

- WTI Price
- Brent Price
- Weekly Change %
- Monthly Change %
- Moving Averages

## Consumer & Agricultural KPIs

- Average Price
- Median Price
- Minimum Price
- Maximum Price
- MoM Price Change %
- YoY Price Change %
- YTD Price Change %
- Price Volatility
- Regional Price Difference %
- Seasonal Indicators

---

# 9. Functional Requirements

## FR-01 — Multi-Source Data Ingestion

The system shall support ingestion from multiple approved data sources.

Potential formats include:

- APIs
- CSV
- Excel
- JSON
- Structured files
- Approved web-access methods

---

## FR-02 — Historical Data Preservation

The system shall preserve historical observations required for trend analysis and reproducibility.

Raw historical information should be retained where technically and legally appropriate.

---

## FR-03 — Medallion Architecture

The platform shall organize data using:

- Bronze
- Silver
- Gold

Each layer shall have a clearly defined responsibility.

---

## FR-04 — Data Standardization

The system shall standardize relevant:

- Dates
- Numeric formats
- Units
- Product names
- Categories
- Geographic values
- Currency values
- Source identifiers

---

## FR-05 — Data Quality Validation

The platform shall implement data-quality controls.

Potential validations include:

- Schema validation
- Null checks
- Duplicate detection
- Range validation
- Completeness checks
- Referential validation
- Freshness validation

---

## FR-06 — Incremental Processing

Where supported by the source, pipelines should process only new or changed information rather than repeatedly processing the complete historical dataset.

---

## FR-07 — Pipeline Orchestration

Recurring pipelines shall be orchestrated through Databricks Workflows or the selected Databricks orchestration capability.

---

## FR-08 — Error Handling

The system shall provide mechanisms to identify pipeline failures.

Where appropriate, the solution should support:

- Error logging
- Retry logic
- Failure status
- Audit records

---

## FR-09 — Analytical Data Layer

The system shall create curated datasets designed for analytical consumption.

These datasets should support:

- KPI calculation
- Historical analysis
- Dashboard filtering
- Cross-domain analysis

---

## FR-10 — Databricks SQL Analytics

Curated datasets shall be accessible for analytical querying using Databricks SQL.

---

## FR-11 — Dashboarding

The platform shall provide analytical outputs through:

- Databricks dashboards
- Power BI

---

## FR-12 — Documentation & Traceability

The project shall maintain documentation connecting:

**Business Requirement → Business Question → KPI → Source Data → Transformation → Gold Dataset → Dashboard**

---

# 10. Non-Functional Requirements

## 10.1 Data Quality

Analytical datasets should meet defined quality expectations for:

- Accuracy
- Completeness
- Consistency
- Validity
- Uniqueness
- Timeliness

---

## 10.2 Reliability

Pipelines should execute consistently according to their expected schedule.

Failures should be identifiable and traceable.

---

## 10.3 Scalability

The architecture should allow additional:

- Data sources
- Indicators
- Products
- Geographic dimensions
- Historical observations

without requiring a complete redesign.

---

## 10.4 Maintainability

The solution should use:

- Clear naming conventions
- Modular transformations
- Documented logic
- Reusable code where appropriate
- Separated configuration and business logic where practical

---

## 10.5 Traceability

Analytical outputs should be traceable to their original source and transformation logic.

---

## 10.6 Performance

Gold analytical datasets should be structured to support efficient dashboard and analytical queries.

---

## 10.7 Reproducibility

The project repository should contain sufficient documentation and implementation artifacts to explain and reproduce the principal components of the solution.

---

# 11. Data Refresh Requirements

Different domains will require different refresh schedules.

Initial expected frequencies include:

| Domain | Expected Frequency |
|---|---|
| Foreign Exchange | Daily |
| International Oil | Daily |
| Fuel Prices | Weekly |
| Inflation / CPI | Monthly |
| Monetary Policy | Event-based / Monthly |
| Consumer Products | Source-dependent |
| Agricultural Products | Source-dependent |
| Electricity | Source-dependent |
| Housing | Source-dependent |

These frequencies are preliminary and must be validated during the **Data Source Assessment**.

The overall orchestration framework may execute daily while determining whether new data is available for each source.

---

# 12. High-Level Deliverables

The project is expected to produce:

### Business Documentation

- Business Requirements Document
- Project Charter
- Business Questions & KPI Catalog
- Data Source Assessment

### Data Documentation

- Data Dictionary
- Source-to-Target Mapping
- Data Quality Rules
- Data Contracts where appropriate

### Architecture

- Solution Architecture
- Medallion Architecture
- Data Flow Diagram
- Logical Data Model
- Physical Data Model

### Engineering

- Databricks environment
- Bronze Layer
- Silver Layer
- Gold Layer
- Metadata / audit framework
- Data-quality framework
- Databricks Workflows

### Analytics

- Databricks SQL analytical layer
- Databricks dashboard
- Power BI dashboard
- Economic analysis

### Portfolio

- GitHub repository
- Technical README
- Architecture diagrams
- LinkedIn project series
- YouTube project walkthrough
- Final case study

---

# 13. Project Scope

## 13.1 In Scope

The MVP is expected to evaluate and, where feasible, integrate:

- Inflation / CPI
- Foreign exchange
- Monetary policy
- Fuel prices
- International oil prices
- Consumer / basic basket prices
- Agricultural prices

Energy/electricity may be incorporated based on source feasibility.

The platform will include:

- Historical data
- Data ingestion
- Data transformation
- Data quality
- Analytical modeling
- KPI calculation
- Orchestration
- Databricks analytics
- Power BI reporting
- Documentation

---

## 13.2 Out of Scope

The initial MVP excludes:

- Automated investment recommendations
- Trading recommendations
- Individual financial advice
- Credit-risk scoring
- Personal banking information
- High-frequency market trading data
- Real-time streaming unless later justified
- Unauthorized web scraping
- Production financial forecasting
- Enterprise-scale deployment
- Machine-learning forecasting

Housing and rental analytics may initially remain outside the MVP until an appropriate source is validated.

---

# 14. Assumptions

The project assumes that:

- Relevant public economic datasets are available.
- Selected historical datasets can be accessed.
- Sources permit the intended access method.
- Databricks resources required for development are available.
- Different datasets will have different update frequencies.
- Some sources may not provide APIs.
- Batch processing will be sufficient for the MVP.
- Requirements may change after source assessment.
- Certain domains may be postponed when data quality or accessibility is insufficient.

---

# 15. Constraints

Potential constraints include:

- Limited public APIs.
- Excel-only publications.
- PDF-based publications.
- Changes to government websites.
- Historical schema inconsistencies.
- Missing historical observations.
- Geographic granularity differences.
- Measurement-unit differences.
- Different publication frequencies.
- Data-access restrictions.
- Limited historical housing information.
- Databricks environment and compute limitations.
- Project implementation by a single developer.

---

# 16. Success Criteria

The project will be considered successful when:

1. Relevant MVP data sources are identified and documented.

2. Selected datasets are successfully ingested.

3. Historical information is preserved.

4. Bronze, Silver, and Gold layers are implemented.

5. Data-quality rules are operational.

6. Core economic KPIs are calculated consistently.

7. Pipelines can execute according to defined schedules.

8. Pipeline executions can be monitored or audited.

9. Databricks SQL can query curated analytical datasets.

10. A functional Databricks dashboard is available.

11. A functional Power BI dashboard is available.

12. Cross-domain economic analysis can be performed.

13. Technical documentation is complete.

14. Business documentation is complete.

15. The complete solution is presented as a reproducible professional portfolio case study.

---

# 17. Project Phases

The project will be developed through the following phases:

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Business Discovery | In Progress |
| **Phase 2** | Data Discovery & Source Assessment | Planned |
| **Phase 3** | Solution Architecture & Data Modeling | Planned |
| **Phase 4** | Databricks Environment Setup | Planned |
| **Phase 5** | Bronze Layer Development | Planned |
| **Phase 6** | Silver Layer Development | Planned |
| **Phase 7** | Gold Layer Development | Planned |
| **Phase 8** | Data Quality & Orchestration | Planned |
| **Phase 9** | Databricks SQL & Dashboard | Planned |
| **Phase 10** | Power BI Development | Planned |
| **Phase 11** | Testing & Validation | Planned |
| **Phase 12** | Documentation & Portfolio Publication | Planned |

---

# 18. Requirements Traceability

One of the core principles of the project is maintaining traceability from business need to final analytical output.

The intended traceability model is:

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
Source
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

This approach will help ensure that technical components are implemented because they support a defined analytical or business requirement.

---

# 19. Document Approval

| Attribute | Value |
|---|---|
| **Document** | Business Requirements Document |
| **Version** | 1.0 |
| **Status** | Draft |
| **Project Owner** | Stanly Fernandez |
| **Approval Status** | Pending Data Source Assessment |

The BRD should remain in **Draft** status until the feasibility of the principal data requirements has been evaluated.

Requirements may be modified if the Data Source Assessment identifies significant limitations in availability, historical coverage, granularity, licensing, or automation.

---

# 20. Next Steps

Following the Business Requirements Document, the project documentation sequence is:

```text
01 — Business Requirements Document      COMPLETE
                 ↓
02 — Project Charter                     COMPLETE
                 ↓
03 — Business Questions & KPI Catalog    IN PROGRESS
                 ↓
04 — Data Source Assessment              NEXT
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
Databricks Implementation
```

Technical implementation should begin after the principal business requirements, KPIs, data sources, and architecture have been evaluated.

---

## Document History

| Version | Date | Description | Author |
|---|---|---|---|
| **1.0** | September 2026 | Initial Business Requirements Document | Stanly Fernandez |

---

## Related Project Documentation

| Document | Status |
|---|---|
| `01_Business_Requirements_Document` | Draft |
| `02_Project_Charter` | Draft |
| `03_Business_Questions_KPI_Catalog` | In Progress |
| `04_Data_Source_Assessment` | Planned |
| `05_Data_Dictionary` | Planned |
| `06_Source_to_Target_Mapping` | Planned |
| `07_Solution_Architecture` | Planned |
| `08_Data_Model` | Planned |
| `09_Data_Quality_Rules` | Planned |

---

**RD Economic & Financial Intelligence Platform**  
*End-to-End Data Engineering & Business Intelligence Portfolio Project*
