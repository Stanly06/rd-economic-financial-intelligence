# Power BI — Connection, Model and Report Design

Power BI is the external consumer of the Gold layer. This guide documents how the report connects to Databricks, the semantic model, and the first report pages.

**Status:** report built in Power BI Desktop (7 pages: Foreign Exchange, Inflation, FX vs Inflation, Cost of Living, Fuel Prices, Consumer Prices, Electricity) on the model and measures below. The `.pbix` file is kept outside the repository.

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
| `Fuel Prices` | `gold.fuel_price_metrics` | Price week × fuel | FUEL-001 to FUEL-012 |
| `Consumer Prices` | `gold.consumer_price_metrics` | Month × product × presentation | CON-001 to CON-005 |
| `Electricity` | `gold.electricity_metrics` | Month × distributor | ENE-005 to ENE-009 |
| `Electricity Bill` | `gold.electricity_bts1_bill` | Month × distributor × monthly kWh | ENE-003, ENE-004 |
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
- Headline, core and national measures remove series/segment filters (`REMOVEFILTERS`), so clicking a group, region or quintile bar never blanks the KPI cards; they still respond to dates.
- Edit interactions: the group and region bars (Inflation page) and the quintile and region bars (Cost of Living page) do not filter each other.
- FX 52-week values start in September 2022 and YTD values in 2022 by design (KPI decision D4); selecting an earlier month shows them blank.

## Report theme

[`rd_intelligence_theme.json`](rd_intelligence_theme.json) (View → Themes → Browse for themes): navy `#0B3C7D` and red `#CE1126` from the Dominican flag, teal and amber accents, light page background, white rounded visuals with soft shadow, navy table headers. Each page has a full-width navy header (title + source) and descriptive visual titles.

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

### Page 5 — Fuel Prices

| Visual | Fields |
|---|---|
| Multi-value card | `Premium Price`, `Regular Price`, `Gasoil Regular Price`, `GLP Price` (latest week, RD$/gal) |
| Line chart | Axis `Fuel Prices[period_start_date]`; value `Fuel Price Series`; legend `Fuel Prices[fuel_name]` |
| Table | `fuel_name`, `Fuel Price`, `Fuel Weekly Change %`, `Fuel Monthly Change %`, `Fuel YoY %`, `Fuel YTD %`, `Fuel 52W High`, `Fuel 52W Low`, `Fuel Volatility 12W` |
| Bar chart | Axis `fuel_name`; values `Fuel YoY %`, `Fuel YTD %` |

### Page 6 — Consumer Prices

| Visual | Fields |
|---|---|
| Multi-value card | `CON Products Tracked`, `CON Products Up`, `CON Products Down`, `CON MoM %` |
| Table | `product`, `presentation`, `CON Avg Price`, `CON Median Price`, `CON Min Price`, `CON Max Price`, `CON Cheapest Segment`, `CON Most Expensive Segment`, `CON Spread %`, `CON MoM %` |
| Bar chart | Axis `product`; value `CON MoM % Top 15` |

### Page 7 — Electricity

| Visual | Fields |
|---|---|
| Multi-value card | `ELEC Selling Price`, `ELEC Selling Price YoY %`, `ELEC Purchase Price cUSD`, `ELEC Losses Rolling %`, `ELEC CRI Rolling %`, `BTS1 Bill 200 kWh Applied`, `BTS1 Bill 200 kWh Reference` |
| Line chart | Axis `Electricity[reference_month]`; value `ELEC Selling Price Series`; legend `Electricity[distributor]` |
| Line chart | Axis `Electricity Bill[reference_month]`; values `Bill 200 kWh Applied (Edesur)`, `Bill 200 kWh Reference (Edesur)` |
| Line chart | Axis `Electricity[reference_month]`; value `ELEC Losses Rolling Series`; legend `Electricity[distributor]` |

Queries for the two electricity tables use the same `DatabricksMultiCloud.Catalogs` source as the other tables. The electricity page canvas is 1920 × 1080 like the others.

## 4. Data notes for report users

- FX source extract covers 2021-09-20 to 2026-09-18. September 2021 and September 2026 are partial months.
- 52-week and year-over-year FX values start in September 2022.
- CPI base period: October 2019 – September 2020 = 100. All calculated inflation values reconcile with BCRD published variations.
- The BCRD family basket is the ENGIH-2018 basket indexed by CPI. Its national and regional year-over-year change therefore equals headline and regional CPI inflation; the basket adds the **DOP level** and the **income-quintile** view. Quintile values before October 2020 are a BCRD retropolation.
- Fuel prices are MICM official weekly prices in RD$ per gallon, from the XLSX file (the CSV rounds to whole pesos). Prices were frozen from August to December 2025, so in the latest week year-over-year and year-to-date changes are equal. GLP shows a one-week value of RD$163.55 (week of 2024-08-31) between weeks at about RD$132; it is kept as published and flagged as a probable source error.
- Consumer prices cover July–September 2026 only. Month-over-month change compares the same product, presentation and retail segment in both months; year-over-year and regional comparisons are not available from this source.
- Electricity: MEM distributor indicators and SIE regulated tariffs from the MEM annex, January 2020 to July 2026. The reference vs applied tariff gap is a proxy of the subsidy, not an official figure; the BTS-1 bill excludes taxes and other charges.
