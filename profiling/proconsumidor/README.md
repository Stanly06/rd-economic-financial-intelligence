# Pro Consumidor — Consumer Prices Data Discovery & Profiling

**Project:** RD Economic & Financial Intelligence Platform  
**Phase:** Data Discovery & Profiling  
**Status:** Initial profiling completed; source validation and KPI feasibility assessment in progress — **not production approved**  
**Source:** Instituto Nacional de Protección de los Derechos del Consumidor (Pro Consumidor), Dominican Republic  
**Business domain:** Consumer and basic-necessity product prices (CON-001 through CON-010; KPI definitions verified against `03_Business_Questions_KPI_Catalog.xlsx`)

## 1. Purpose and scope

Assess actual source structure, temporal and categorical coverage, data quality, and potential suitability for the platform's consumer-price KPIs. The source is Dominican core data under the **RD-First** strategy. This is source profiling, not a completed Databricks ingestion or validated analytical model.

## 2. Source inventory

| Attribute | Initial finding |
|---|---|
| Files received | `precios de productos de primera necesidad.csv`; `precios de productos de primera necesidad.xlsx` |
| Source title | Precios Productos de Primera Necesidad, por segmento de comercialización — Julio–Septiembre 2026 |
| CSV delimiter / encoding | Semicolon (`;`); UTF-8 with BOM readable |
| Physical CSV lines | 931, including heading and empty/formatted rows |
| Data records with numeric ID | **600** |
| Business fields | **7**: `Id`, `Producto`, `Tipo`, `Precio`, `Mes`, `Año`, `establecimiento` |
| Original product labels | **274** distinct raw; **201** after trimming whitespace; **198** after trimming and case-folding; no semantic product normalization |
| Commercial segments | **5** |
| Months appearing in data | July, August, September |
| Year quality | **570 records marked 2026; 30 records marked other years (2027–2041)** |

Raw CSV and XLSX files are preserved unchanged in the append-only archive `bronze.proconsumidor_raw/consumer_prices/<yyyy>/<mm>/` (one folder per arrival month, because every report uses the same file name). Do not upload source data to the public repository pending source licensing and data-publication review.

## 3. Observed distribution

| Month | Records |
|---|---:|
| July | 210 |
| August | 207 |
| September | 183 |
| **Total** | **600** |

| Commercial segment (`establecimiento`) | Records |
|---|---:|
| Supermercados grandes | 212 |
| Mercados | 125 |
| Supermercados pequeños | 89 |
| Colmados | 89 |
| Almacenes | 85 |
| **Total** | **600** |

The `establecimiento` field describes a **commercial segment**, not an individual named store. No explicit province, municipality, geographic coordinates, or daily observation date exists among the seven business fields.

## 4. Preliminary quality findings

1. **Year anomalies — blocking:** 30 records contain years other than 2026, including future years through 2041, despite the source title identifying July–September 2026. A contiguous ID sequence beginning at ID 437 shows increasing years. Investigate against the official published source before correction. Keep raw values and document any approved correction separately.
2. **Temporal grain:** Only month names and year values are supplied. No day-level date should be fabricated. The tentative grain is *reported month × product × presentation × commercial segment*, subject to verification of source methodology and aggregation rules.
3. **Product normalization:** Product names and presentations contain extra whitespace and mixed brand/unit conventions. A controlled product dictionary and unit mapping are required before comparison.
4. **Price parsing:** CSV contains prices with thousands separators (e.g., `1,455.35`). Parse as decimal using the documented locale; do not interpret comma as a decimal separator.
5. **Geography:** Region- and province-level price comparisons are not supported by the provided fields.
6. **Historical depth:** Three reported months are insufficient for reliable year-over-year comparisons or long historical trend measures.
7. **Uniqueness:** The 600 numeric IDs were observed to be unique in the CSV. IDs should not automatically be treated as stable business keys across future source releases.

**Additional preliminary comparison from prior review:** CSV and XLSX were reported to contain the same 600 records; 11 price-display differences were associated with thousands-separator representation rather than numeric disagreement. This should be reproduced and documented before production sign-off.

## 5. KPI feasibility gate (CON-001–CON-010)

The following definitions were checked against the project's `03_Business_Questions_KPI_Catalog.xlsx` (KPI_Catalog sheet). Assessments are **source-specific** and do not change the catalog's original `Proposed` validation status.

| KPI | Catalog KPI name | Calculation / intent | Feasibility with current extract | Conditions / blockers |
|---|---|---|---|---|
| CON-001 | Average Product Price | `AVG(price)` | **Conditional** | Comparable product, presentation, unit, month, and segment; confirm price observation methodology and valid years |
| CON-002 | Median Product Price | `MEDIAN(price)` | **Conditional** | Sufficient comparable observations per grouping; avoid interpreting a single record as a surveyed median |
| CON-003 | Minimum Product Price | `MIN(price)` | **Conditional** | Comparable observations; not a verified store-level minimum |
| CON-004 | Maximum Product Price | `MAX(price)` | **Conditional** | Comparable observations; not a verified store-level maximum |
| CON-005 | Product MoM % | `(Price_t / Price_prev_month - 1) * 100` | **Conditional** | Same comparable product/presentation/unit/segment in consecutive valid months; define reference price measure |
| CON-006 | Product YoY % | `(Price_t / Price_t-1year - 1) * 100` | **Unsupported by this extract** | Prior-year comparable observations absent |
| CON-007 | Product YTD % | `(Price_t / Price_last_prev_year - 1) * 100` | **Unsupported by this extract** | Previous December baseline absent |
| CON-008 | Product Price Volatility | `STDDEV(periodic returns)` over a defined window | **Conditional / insufficient history for robust measure** | Specify minimum window, regular comparable observations, and treatment of sparse returns |
| CON-009 | Regional Price Difference % | `(Regional Price / Reference Price - 1) * 100` | **Unsupported by this extract** | No region/province/municipality fields; `establecimiento` is a commercial segment, not geography |
| CON-010 | Category Price Index | Methodology to be defined after source/granularity assessment | **Methodology pending** | Define categories, matched products, weighting, base period, and missing-product treatment |

**Important:** The file has month/year but no observation day, named store, or explicit geographic identifier. The original catalog lists richer candidate dimensions; their presence in the catalog does not mean they are available in this source. Do not infer national representativeness from the extract.

## 6. Candidate engineering approach — not implemented

- **Landing/raw:** Retain original CSV and XLSX, filename, acquisition date, checksum, source URL, and file-level metadata.
- **Bronze:** Preserve source values and source column names with ingestion metadata; do not silently repair anomalous years.
- **Silver:** Standardize product and presentation labels, decimal prices, commercial segments, and monthly period keys. Quarantine or flag invalid years pending source confirmation.
- **Gold:** Design consumer-price measures only after business-grain and KPI feasibility validation.
- **Incremental ingestion:** Verify official publication cadence, stable download URL, replacement-file behavior, and revision policy before specifying a production schedule.

Candidate names such as `bronze.proconsumidor_prices`, `silver.consumer_prices`, and `gold.consumer_price_metrics` are **conceptual**, pending Data Dictionary, Source-to-Target Mapping, and architecture approval.

## 7. Proposed data-quality rules

| Rule | Proposed check | Treatment |
|---|---|---|
| DQ-PC-001 | Numeric, non-null source ID | Reject/flag malformed record |
| DQ-PC-002 | Price parses to decimal and is positive | Quarantine invalid values |
| DQ-PC-003 | Year/month consistent with documented source period | Flag anomalous year; preserve raw |
| DQ-PC-004 | Product, presentation, and commercial segment populated | Quarantine incomplete key attributes |
| DQ-PC-005 | No unexplained duplicate at agreed business grain | Investigate; do not blindly deduplicate |
| DQ-PC-006 | Consistent normalized units and product mappings | Record unresolved mappings |
| DQ-PC-007 | CSV/XLSX reconciliation of parsed values | Investigate mismatches |

Thresholds, ownership, and severity require approval during the Data Quality Rules & Data Contracts phase.

## 8. Open questions and next actions

1. Confirm whether the 30 anomalous year values are source-entry or export errors; obtain authoritative corrected records if available.
2. Validate the exact data grain, measurement methodology, currency, unit definitions, and whether values are average observed prices.
3. Confirm if older monthly files exist for year-over-year analysis.
4. Determine whether province, city, individual establishment, or survey sample metadata can be obtained from other official Pro Consumidor publications.
5. Reproduce a full numeric CSV-to-XLSX comparison.
6. Review and approve the documented KPI feasibility matrix; obtain additional source history or dimensions for unsupported KPIs.
7. After validation, feed approved attributes into `05_Data_Dictionary` and `06_Source-to-Target_Mapping`.

## 9. Project status

**Validated in development (2026-10-23); pipelines implemented** in `src/bronze|silver|gold/05_ProConsumidor_Prices_*`. Not production approved.

Decisions applied:

- XLSX is used; the CSV has inconsistent delimiters.
- 30 rows whose year is outside the report period stated in the title (July–September 2026) are rejected to `quality.dq_rejected_records`, not corrected (question 1 above stays open with the source).
- Grain: month × product × presentation × retail segment (5 segments). 570 valid rows, 197 products after mapping 21 label variants (different capitals or spacing) to one canonical label.
- CON-001 to CON-005 calculated; month-over-month is like-for-like by segment because the segments priced change each month. CON-006 to CON-009 need more history or geography (questions 3 and 4); CON-010 needs a methodology.

Related: [Project Documentation Roadmap](../../docs/README.md) · [MICM Fuel Prices Profiling](../micm/README.md)
