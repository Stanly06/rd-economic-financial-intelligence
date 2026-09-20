# Project Charter

## RD Economic & Financial Intelligence Platform

> **End-to-End Databricks Lakehouse Project for Economic, Financial, Inflation, and Cost-of-Living Analytics in the Dominican Republic**

---

## Document Information

| Attribute | Details |
|---|---|
| **Project Name** | RD Economic & Financial Intelligence Platform |
| **Document Type** | Project Charter |
| **Document Version** | 1.0 |
| **Status** | Draft |
| **Project Start** | September 2026 |
| **Project Type** | Data Engineering & Business Intelligence Case Study |
| **Primary Platform** | Databricks |
| **Architecture** | Lakehouse / Medallion Architecture |
| **Geographic Scope** | Dominican Republic |
| **Project Owner** | Stanly Fernandez |
| **Repository** | `rd-economic-financial-intelligence` |

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Business Need](#2-business-need)
3. [Project Purpose](#3-project-purpose)
4. [Project Objectives](#4-project-objectives)
5. [Expected Business Outcomes](#5-expected-business-outcomes)
6. [Project Scope](#6-project-scope)
7. [Out of Scope](#7-out-of-scope)
8. [Major Deliverables](#8-major-deliverables)
9. [High-Level Solution Architecture](#9-high-level-solution-architecture)
10. [Key Stakeholders](#10-key-stakeholders)
11. [Project Roles](#11-project-roles)
12. [Key Business Questions](#12-key-business-questions)
13. [Success Criteria](#13-success-criteria)
14. [Key Assumptions](#14-key-assumptions)
15. [Project Constraints](#15-project-constraints)
16. [High-Level Risks](#16-high-level-risks)
17. [High-Level Milestones](#17-high-level-milestones)
18. [Project Governance](#18-project-governance)
19. [Change Management](#19-change-management)
20. [Project Completion Criteria](#20-project-completion-criteria)
21. [Project Authorization](#21-project-authorization)
22. [Next Steps](#22-next-steps)

---

# 1. Project Overview

The **RD Economic & Financial Intelligence Platform** is an end-to-end Data Engineering and Business Intelligence project designed to centralize, process, analyze, and visualize key economic, financial, monetary, energy, consumer-price, and cost-of-living indicators for the Dominican Republic.

The project will integrate information currently distributed across multiple public and external data sources into a centralized **Databricks Lakehouse**.

The solution will implement a **Medallion Architecture** using Bronze, Silver, and Gold data layers to progressively transform raw source data into validated, standardized, and analytics-ready datasets.

The final analytical layer will support **Databricks SQL**, interactive Databricks dashboards, and **Power BI**.

This project is also designed as a professional portfolio case study demonstrating the complete lifecycle of a modern data platform:

**Business Requirements → Data Discovery → Architecture → Data Engineering → Data Quality → Orchestration → Analytics → Business Intelligence → Business Insights**

---

# 2. Business Need

Economic and financial information related to the Dominican Republic is distributed across multiple institutions, websites, datasets, publication formats, and update frequencies.

Users interested in understanding the Dominican economic environment may need to consult several independent sources to analyze:

- Inflation
- Consumer Price Index (CPI)
- Foreign exchange rates
- Monetary policy
- Interest rates
- Fuel prices
- International oil prices
- Basic household basket prices
- Agricultural product prices
- Electricity and energy costs
- Housing and rental costs

This fragmentation makes it difficult to create a consolidated historical view of economic conditions and to analyze relationships between different economic variables.

The project addresses this problem by creating a centralized analytical platform capable of integrating heterogeneous datasets and transforming them into consistent, reliable, and reusable economic indicators.

---

# 3. Project Purpose

The purpose of the **RD Economic & Financial Intelligence Platform** is to build a centralized economic intelligence solution that enables users to monitor and analyze economic, financial, and cost-of-living conditions in the Dominican Republic.

The platform will transform fragmented public and external datasets into structured analytical information through automated data pipelines.

The project should enable users to move from:

**Raw Data → Trusted Data → Economic Indicators → Analytical Insights**

---

# 4. Project Objectives

The project has the following high-level objectives:

1. Identify reliable and relevant economic and financial data sources for the Dominican Republic.

2. Centralize selected datasets within a Databricks Lakehouse.

3. Implement a Medallion Architecture consisting of Bronze, Silver, and Gold layers.

4. Preserve historical observations to enable longitudinal and trend analysis.

5. Implement automated and incremental ingestion whenever supported by the source.

6. Standardize heterogeneous data formats, schemas, units, dates, and classifications.

7. Implement data-quality validations throughout the transformation pipeline.

8. Implement metadata, logging, and pipeline auditing capabilities.

9. Calculate standardized financial, economic, and cost-of-living KPIs.

10. Enable cross-domain analysis between economic variables.

11. Implement scheduled pipeline orchestration using Databricks Workflows.

12. Implement appropriate error handling and retry strategies.

13. Develop analytical datasets optimized for reporting and business intelligence.

14. Develop an interactive Databricks SQL dashboard.

15. Develop a Power BI dashboard using curated analytical datasets.

16. Document the complete lifecycle of the solution.

17. Produce a reproducible professional portfolio case study demonstrating end-to-end Data Engineering capabilities.

---

# 5. Expected Business Outcomes

The completed platform should provide a consolidated analytical view of selected economic and cost-of-living conditions in the Dominican Republic.

Expected outcomes include:

- Reduced fragmentation of economic information.
- Easier access to historical economic data.
- Faster identification of price trends.
- Centralized monitoring of economic indicators.
- Consistent calculation of business KPIs.
- Improved comparison between economic variables.
- Improved identification of anomalies and unusual movements.
- Identification of seasonal patterns.
- Analysis of geographic price differences where data permits.
- Better understanding of relationships between international and domestic economic variables.
- Reusable analytical datasets for dashboards and future analysis.

---

# 6. Project Scope

## 6.1 Inflation & Consumer Price Index

The platform should support analysis of:

- Consumer Price Index (CPI)
- Monthly inflation
- Year-over-year inflation
- Year-to-date inflation
- Core inflation, where available
- Inflation by expenditure category
- Historical inflation trends

---

## 6.2 Foreign Exchange Market

The project should evaluate and integrate relevant foreign exchange indicators, including:

- USD/DOP exchange rate
- Buy rate
- Sell rate
- EUR/DOP where reliable data is available
- Daily variation
- Monthly variation
- Year-over-year variation
- Year-to-date variation
- Moving averages
- Historical highs and lows
- Dominican peso appreciation/depreciation

---

## 6.3 Monetary & Financial Indicators

The platform should support analysis of selected monetary and financial indicators such as:

- Monetary Policy Rate
- Interest-rate indicators
- Changes in basis points
- Monetary policy trends
- Monetary Policy Rate versus inflation
- Real-rate proxy where analytically appropriate

Additional financial indicators may be incorporated following the Data Source Assessment.

---

## 6.4 Fuel Market

The platform should analyze fuel prices including, where data is available:

- Premium gasoline
- Regular gasoline
- Premium diesel
- Regular diesel
- LPG
- Natural gas
- Other relevant fuels

Potential analytical metrics include:

- Current price
- Previous-period price
- Weekly change
- Weekly percentage change
- Monthly percentage change
- Year-over-year percentage change
- Year-to-date percentage change
- Rolling averages
- Historical highs and lows
- Price volatility

---

## 6.5 International Oil Market

International energy indicators should include:

- West Texas Intermediate (WTI)
- Brent crude oil

The project should enable comparisons between international oil prices and domestic fuel prices.

Potential analysis includes:

- Oil price trends
- Fuel price trends
- Oil-to-fuel correlation
- Lagged relationships
- Exchange-rate effects on domestic fuel prices

---

## 6.6 Basic Household Basket & Consumer Products

Where sufficiently granular and reliable information is available, the project should analyze consumer-product prices using attributes such as:

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

Potential metrics include:

- Average price
- Median price
- Minimum price
- Maximum price
- Monthly change
- Year-over-year change
- Price volatility
- Seasonality
- Geographic price differences

---

## 6.7 Agricultural Products

Selected agricultural products may include:

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
- Other relevant agricultural products

Potential analysis includes:

- Historical price trends
- Price volatility
- Seasonality
- Geographic variation
- Monthly and annual changes

---

## 6.8 Electricity & Energy

Where reliable historical information is available, the platform may integrate:

- Electricity tariffs
- Cost per kWh
- Tariff categories
- Historical tariff changes
- Selected energy-cost indicators

---

## 6.9 Housing & Rental Market

Housing and rental indicators may be incorporated when technically and legally appropriate data sources are identified.

Potential attributes include:

- Rental price
- Property type
- Bedrooms
- Bathrooms
- Municipality
- Sector
- Geographic area
- Observation date

Housing-related functionality will depend on the results of the Data Source Assessment.

---

# 7. Out of Scope

The following capabilities are excluded from the initial MVP:

- Automated investment recommendations
- Trading recommendations
- Individual financial advice
- Production financial forecasting
- Credit-risk scoring
- Individual customer banking information
- Personally identifiable financial information
- High-frequency real-time streaming
- Unauthorized web scraping
- Automated monetary-policy recommendations
- Enterprise-scale production deployment
- Machine-learning forecasting models

These capabilities may be evaluated as future enhancements when appropriate.

---

# 8. Major Deliverables

## 8.1 Business & Project Documentation

- Business Requirements Document
- Project Charter
- Business Questions & KPI Catalog
- Data Source Assessment
- Project Plan / Milestone Tracking

## 8.2 Data Documentation

- Data Dictionary
- Source-to-Target Mapping
- Data Quality Rules
- Data Contracts where appropriate
- Naming Conventions
- Metadata definitions

## 8.3 Architecture

- Solution Architecture Diagram
- Medallion Architecture Design
- Logical Data Model
- Physical Data Model
- Data Flow Diagram

## 8.4 Data Engineering

- Databricks Lakehouse
- Bronze Layer
- Silver Layer
- Gold Layer
- Metadata Framework
- Audit Framework
- Data Quality Framework

## 8.5 Orchestration & Reliability

- Databricks Workflows
- Scheduled ingestion
- Dependency management
- Error handling
- Retry strategy
- Pipeline monitoring
- Pipeline execution logging

## 8.6 Analytics & Business Intelligence

- Databricks SQL analytical layer
- Databricks Dashboard
- Power BI semantic/analytical model
- Power BI Dashboard
- Business insights

## 8.7 Portfolio Deliverables

- Public GitHub repository
- Technical README
- Architecture diagrams
- Technical documentation
- Business insights summary
- LinkedIn project series
- YouTube project walkthrough

---

# 9. High-Level Solution Architecture

The initial target architecture follows the pattern below:

```text
┌─────────────────────────────────────────────┐
│                DATA SOURCES                 │
│ BCRD | MICM | ONE | Consumer | Agriculture │
│ Energy | International Market Data | Other │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                  INGESTION                  │
│     APIs | CSV | Excel | JSON | Files       │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                BRONZE LAYER                 │
│            Raw / Historical Data            │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          DATA QUALITY & VALIDATION          │
│ Schema | Nulls | Duplicates | Completeness │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                SILVER LAYER                 │
│ Cleaned | Standardized | Validated | Joined│
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                 GOLD LAYER                  │
│       KPIs | Aggregations | Analytics       │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│             ANALYTICAL / SQL LAYER          │
│                Databricks SQL               │
└───────────────┬─────────────────┬───────────┘
                │                 │
                ▼                 ▼
       ┌────────────────┐ ┌────────────────┐
       │ Databricks     │ │    Power BI    │
       │ Dashboards     │ │   Dashboards   │
       └───────┬────────┘ └───────┬────────┘
               │                  │
               └────────┬─────────┘
                        ▼
              ┌──────────────────┐
              │ BUSINESS INSIGHTS│
              └──────────────────┘
```

> **Note:** This represents the initial conceptual architecture. The final architecture will be defined after the Data Source Assessment and Solution Design phases.

---

# 10. Key Stakeholders

Because this project is a portfolio case study, the stakeholders below represent potential users of an economic intelligence platform rather than actual organizational stakeholders.

| Stakeholder | Primary Interest |
|---|---|
| Executive / Decision Maker | Economic overview and strategic indicators |
| Economic Analyst | Macroeconomic trends and inflation |
| Financial Analyst | FX, interest rates and economic relationships |
| Banking Analyst | Monetary and financial indicators |
| Risk Analyst | Economic trends and volatility |
| BI Analyst | KPIs, reporting and visualization |
| Data Analyst | Analytical datasets and exploratory analysis |
| Data Engineer | Reliable and automated data pipelines |
| Data Architect | Architecture, modeling and scalability |
| Platform Administrator | Reliability, governance and monitoring |

---

# 11. Project Roles

For this portfolio implementation, the project owner performs multiple roles throughout the project lifecycle.

| Role | Primary Responsibility |
|---|---|
| **Business Analyst** | Requirements, business problems and business questions |
| **Project Manager** | Scope, milestones, risks and project coordination |
| **Data Analyst** | Data exploration, analysis and KPI definition |
| **Data Engineer** | Ingestion, transformation, storage and orchestration |
| **Data Architect** | Lakehouse architecture and data modeling |
| **BI Developer** | Databricks SQL and Power BI dashboards |
| **Data Quality Engineer** | Validation, testing and monitoring |
| **Documentation Owner** | Business and technical documentation |

> This multi-role structure is intended to demonstrate the lifecycle of an end-to-end data project and does not represent the staffing model of a production organization.

---

# 12. Key Business Questions

The platform should ultimately help answer questions such as:

### Inflation

- How is inflation evolving in the Dominican Republic?
- What is the current monthly and year-over-year inflation rate?
- Which expenditure categories contribute most to consumer-price changes?
- How has core inflation evolved?

### Foreign Exchange

- How has USD/DOP evolved over time?
- Is the Dominican peso appreciating or depreciating?
- What are the short-term and long-term exchange-rate trends?
- How do exchange-rate movements compare with inflation?

### Monetary Policy

- How has the Monetary Policy Rate evolved?
- How many basis points has the policy rate changed?
- How does monetary policy compare with inflation?
- How has the real-rate proxy evolved?

### Fuel & Oil

- How have Dominican fuel prices changed over time?
- Which fuel has experienced the greatest percentage increase?
- How do domestic fuel prices compare with WTI and Brent?
- Is there evidence of a lag between international oil-price movements and domestic fuel-price changes?
- Does USD/DOP appear to influence the relationship between oil and domestic fuel prices?

### Consumer Products

- Which products have increased most in price?
- Which products have decreased in price?
- Which products are most volatile?
- What seasonal price patterns exist?
- Which geographic areas have higher prices?

### Cost of Living

- How is the overall cost-of-living environment changing?
- Which categories are placing the greatest pressure on household expenses?
- How do inflation, food, energy, fuel, FX, and housing indicators evolve together?

---

# 13. Success Criteria

The project will be considered successful when:

1. Multiple relevant economic datasets are successfully integrated.

2. Historical source data is preserved.

3. Bronze, Silver, and Gold layers are implemented.

4. Data-quality controls are operational.

5. Selected pipelines execute automatically according to defined schedules.

6. Pipeline executions can be audited.

7. Failed pipeline executions can be identified and investigated.

8. Economic and financial KPIs are calculated consistently.

9. Analytical datasets support cross-domain analysis.

10. Databricks SQL can query curated analytical datasets.

11. A functional Databricks dashboard is implemented.

12. A functional Power BI dashboard is implemented.

13. Technical and business documentation is complete.

14. The GitHub repository clearly explains how the solution was designed and implemented.

15. The final project can be demonstrated as an end-to-end Data Engineering portfolio case study.

---

# 14. Key Assumptions

The project assumes that:

- Selected public datasets remain accessible.
- Historical information exists for key indicators.
- Sources permit the intended data-access method.
- Databricks resources required for the project are available.
- Source publication frequencies may differ.
- Source schemas may evolve.
- Some requirements may change after the Data Source Assessment.
- Some domains may be postponed if reliable sources cannot be identified.
- Not every source will provide an API.
- Batch processing will satisfy the requirements of the MVP.

---

# 15. Project Constraints

Potential project constraints include:

- Limited availability of public APIs.
- Government information published primarily as Excel, CSV, PDF, or web tables.
- Inconsistent historical schemas.
- Source website changes.
- Missing historical observations.
- Different geographic granularities.
- Different units of measure.
- Different publication frequencies.
- Limited historical data for certain domains.
- Databricks compute and environment limitations.
- Restrictions on automated collection from third-party platforms.
- Project implementation being performed by a single developer.

---

# 16. High-Level Risks

| Risk | Potential Impact | Initial Mitigation |
|---|---|---|
| Source becomes unavailable | Pipeline cannot obtain new data | Preserve Bronze history and identify alternative source |
| Source schema changes | Transformation failure | Schema validation and controlled transformations |
| API limitations | Delayed or missing updates | Alternative approved ingestion method |
| Poor source data quality | Incorrect analytical results | Data-quality rules and validation |
| Duplicate ingestion | Incorrect metrics | Idempotent and incremental processing |
| Missing observations | Incomplete analysis | Completeness monitoring and quality reporting |
| Different data frequencies | Misleading comparisons | Temporal alignment and appropriate aggregation |
| Unit inconsistencies | Invalid comparisons | Standardization in Silver |
| Pipeline failure | Stale analytical datasets | Monitoring, logging and retry strategy |
| Scope growth | Project delays | MVP prioritization and enhancement backlog |
| Source access restrictions | Dataset cannot be automated | Replace, defer or manually ingest where appropriate |
| Limited compute resources | Performance constraints | Optimize workloads and control scope |

A more detailed Risk Register may be developed during the Project Planning phase.

---

# 17. High-Level Milestones

| Phase | Major Output | Status |
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

Detailed dates and dependencies will be maintained separately within the Project Plan.

---

# 18. Project Governance

Project decisions should follow the sequence:

```text
Business Requirement
        ↓
Business Question / KPI
        ↓
Data Availability Validation
        ↓
Architecture Decision
        ↓
Development
        ↓
Testing & Data Quality
        ↓
Business Validation
        ↓
Documentation
```

Major changes to scope should be documented rather than introduced directly into the implementation.

Architecture and implementation decisions should remain traceable to a business requirement or technical requirement whenever possible.

---

# 19. Change Management

New requirements discovered during the project will be classified as:

| Classification | Definition |
|---|---|
| **MVP Required** | Necessary to achieve the minimum viable project objectives |
| **Enhancement** | Valuable improvement that is not required for the MVP |
| **Future Phase** | Capability intentionally postponed to a later project version |

Changes affecting architecture, source systems, KPIs, project scope, or major technical decisions should be documented before implementation.

This approach will help control scope growth while preserving future ideas.

---

# 20. Project Completion Criteria

The MVP will be considered complete when:

- Required MVP datasets are integrated.
- Historical source data is preserved.
- Automated ingestion is operational for selected sources.
- Bronze datasets are available.
- Silver datasets are standardized and validated.
- Gold analytical datasets are available.
- Required data-quality checks are implemented.
- Core economic KPIs are validated.
- Pipeline execution metadata is available.
- Databricks Workflows execute successfully.
- Databricks SQL analytical queries are operational.
- Databricks dashboard is functional.
- Power BI dashboard is functional.
- Architecture and data models are documented.
- GitHub documentation is complete.
- Final business insights are documented.
- The project can be reproduced and explained as a professional portfolio case study.

---

# 21. Project Authorization

| Attribute | Value |
|---|---|
| **Project** | RD Economic & Financial Intelligence Platform |
| **Document** | Project Charter |
| **Version** | 1.0 |
| **Status** | Draft |
| **Project Owner** | Stanly Fernandez |
| **Project Sponsor** | Hypothetical / Portfolio Case Study |
| **Approval Status** | Pending completion of Business Discovery |

This Project Charter establishes the initial direction, scope, objectives, deliverables, constraints, and success criteria for the project.

The document may be updated as additional information becomes available during Data Discovery and Solution Design.

---

# 22. Next Steps

Following the Project Charter, the project will continue through the following sequence:

```text
Business Requirements                  COMPLETE
        ↓
Project Charter                        CURRENT
        ↓
Business Questions & KPI Catalog       NEXT
        ↓
Data Source Assessment
        ↓
Data Dictionary
        ↓
Source-to-Target Mapping
        ↓
Solution Architecture
        ↓
Data Model
        ↓
Data Quality Rules & Data Contracts
        ↓
Databricks Environment Setup
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
Orchestration & Monitoring
        ↓
Databricks SQL
        ↓
Databricks Dashboard
        ↓
Power BI
        ↓
Testing & Validation
        ↓
Business Insights
        ↓
Portfolio Publication
```

Technical implementation in Databricks will begin after the required business questions, data sources, architecture, and initial data structures have been evaluated.

---

## Document History

| Version | Date | Description | Author |
|---|---|---|---|
| 1.0 | September 2026 | Initial Project Charter | Stanly Fernandez |

---

## Related Project Documentation

| Document | Status |
|---|---|
| `01_Business_Requirements_Document` | Completed |
| `02_Project_Charter` | Draft |
| `03_Business_Questions_KPI_Catalog` | Planned |
| `04_Data_Source_Assessment` | Planned |
| `05_Data_Dictionary` | Planned |
| `06_Source_to_Target_Mapping` | Planned |
| `07_Solution_Architecture` | Planned |
| `08_Data_Model` | Planned |
| `09_Data_Quality_Rules` | Planned |

---

**RD Economic & Financial Intelligence Platform**  
*End-to-End Data Engineering & Business Intelligence Portfolio Project*
