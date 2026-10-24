# Power BI — Connection, Model and Report Design

Power BI is the external consumer of the Gold layer. This guide documents how the report connects to Databricks, the semantic model, and the first report pages.

**Status:** report built in Power BI Desktop (4 pages: Foreign Exchange, Inflation, FX vs Inflation, Cost of Living) on the model and measures below. The `.pbix` file is kept outside the repository.

---

## 1. Connection

| Setting | Value |
|---|---|
| Connector | **Databricks** (this workspace runs on AWS; use the "Databricks" connector, not "Azure Databricks") |
| Server hostname | `dbc-05963ad7-c763.cloud.databricks.com` |
| HTTP path | `/sql/1.0/warehouses/ad32dad2f38d6f6a` (Serverless Starter Warehouse, 2X-Small) |
| Catalog | `rd_economic_intelligence` |
| Data connectivity mode | **Import** (small tables; avoids keeping the warehouse running) |
| Authentication | Personal Access Token dedicated to Power BI (separate from any other token) |

Steps in Power BI Desktop:

1. **Get data → More… → search "Databricks" → select Databricks (not Azure Databricks) → Connect.**
2. Enter the server hostname and HTTP path above. Leave catalog empty. Choose **Import**.
3. Authentication: **Personal Access Token**. Create one in Databricks: *Settings → Developer → Access tokens → Generate new token* (comment `powerbi`, lifetime 90 days).
4. In the Navigator open `rd_economic_intelligence → gold` and select the four tables below, then **Load**.

> The SQL warehouse auto-stops when idle. The first refresh after a pause can take about a minute while it starts.

## 2. Semantic model

| Power BI table | Databricks object | Grain | KPIs |
|---|---|---|---|
| `FX Daily` | `gold.exchange_rate_metrics` | Date × currency pair × rate type | FX-001, 002, 003, 006, 007, 008, 009 |
| `FX Monthly` | `gold.exchange_rate_monthly_metrics` | Month × currency pair × rate type | FX-004, FX-005 |
| `Inflation` | `gold.inflation_metrics` | Month × CPI series | INF-001 to INF-006 |
| `Cost of Living` | `gold.cost_of_living_metrics` | Month × segment | COL-001 to COL-003 |
| `Calendar` | DAX table | Day | — |

Relationships (one-to-many, single direction from `Calendar`):

```text
Calendar[Date] ──1:*── FX Daily[rate_date]
Calendar[Date] ──1:*── FX Monthly[month_start]
Calendar[Date] ──1:*── Inflation[reference_month]
Calendar[Date] ──1:*── Cost of Living[reference_month]
```

All measures are in [`measures.dax`](measures.dax). Percent measures return fractions; format them as **Percentage, 2 decimals**.

Modeling rules:

- Hide technical columns (`_gold_run_id`, `_gold_processed_ts`, `is_full_window_*`, `published_*`) from report view.
- Mark `Calendar` as the date table.
- Never sum rates or percentages; all measures use `MAX`/`AVERAGE` on a single date or month.

## 3. Report pages

### Page 1 — Foreign Exchange (USD/DOP)

Business question BQ-003: *How is the Dominican peso performing against the U.S. dollar?*

| Visual | Fields |
|---|---|
| KPI cards | `FX Buy Rate`, `FX Sell Rate`, `FX Daily Change %`, `FX YTD Change %`, `FX 52W High`, `FX 52W Low` |
| Line chart | Axis `Calendar[Date]`; values `FX Rate`, `FX Rate MA30`; slicer `FX Daily[rate_type]` |
| Column chart | Axis `Calendar[Month]`; value `FX MoM %` (sell); tooltip `FX Month Is Partial` |
| Text box | "Rate up = peso depreciation. Source: BCRD." |
| Slicer | `Calendar[Year]` |

### Page 2 — Inflation

| Visual | Fields |
|---|---|
| KPI cards | `Headline Inflation YoY %`, `Core Inflation YoY %`, `Headline Inflation YTD %`, `Headline Inflation MoM %` |
| Line chart | Axis `Calendar[Month]`; value `Inflation YoY %`; legend `Inflation[series_name]`, filtered to series_type = headline, core |
| Bar chart | Axis `Inflation[series_name]` (filter series_type = expenditure_group, latest month); value `Inflation YoY %` |
| Bar chart | Axis `Inflation[series_name]` (filter series_type = region, latest month); value `Inflation YoY %` |

### Page 3 — FX vs Inflation

| Visual | Fields |
|---|---|
| Line chart | Axis `Calendar[Month]` (2022 onward); values `Headline YoY % (monthly axis)`, `FX Sell YoY % (monthly axis)` |

### Page 4 — Cost of Living

| Visual | Fields |
|---|---|
| KPI cards | `Basket Cost National`, `Basket Cost YoY %`, `Q5 vs Q1 Gap DOP`, `Q5 vs Q1 Ratio` |
| Column chart | Axis `Cost of Living[segment]` (filter segment_type = income_quintile, latest month); value `Basket Cost` |
| Bar chart | Axis `Cost of Living[segment]` (filter segment_type = region, latest month); value `Basket Cost` |
| Line chart | Axis `Calendar[Month]`; value `Basket Cost`; legend `Cost of Living[segment]` (quintiles) |

## 4. Data notes for report users

- FX source extract covers 2021-09-20 to 2026-09-18. September 2021 and September 2026 are partial months.
- 52-week and year-over-year FX values start in September 2022.
- CPI base period: October 2019 – September 2020 = 100. All calculated inflation values reconcile with BCRD published variations.
- The BCRD family basket is the ENGIH-2018 basket indexed by CPI. Its national and regional year-over-year change therefore equals headline and regional CPI inflation; the basket adds the **DOP level** and the **income-quintile** view. Quintile values before October 2020 are a BCRD retropolation.
