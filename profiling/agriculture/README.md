# Ministry of Agriculture — Agricultural Prices Data Discovery & Preliminary Profiling

**Project:** RD Economic & Financial Intelligence Platform  
**Domain:** Agricultural Prices  
**Status:** Preliminary CSV profiling completed; Excel cross-format reconciliation pending  
**Assessment date:** 2026-10-11

## 1. Purpose and scope

Assess the source structure, temporal coverage, market dimensions, unit comparability, and initial data-quality risks of Dominican agricultural retail and wholesale price datasets. Findings below are based on inspection of the supplied original CSV files. The accompanying XLSX and XLS files have been received but **have not yet been reconciled row by row** with the CSV files. No data engineering implementation or production validation is claimed.

## 2. Source inventory

| Source file | Format | Preliminary observation |
|---|---|---|
| `Informe-de-precios-Minorista-Agosto-2017-Septiembre-2026.csv` | CSV | 51,558 data rows; 14 columns including seven market/retail outlet price fields |
| `Informe-de-precios-Minorista-Agosto-2017-Septiembre-2026.xls` | XLS | Received; content and format comparison pending |
| `Informe-de-precios-Mayorista-Agosto-2017-Septiembre-2026..csv` | CSV | 44,533 physical rows; 44,532 rows have expected eight-column structure; no header row |
| `Informe-de-precios-Mayorista-Agosto-2017-Septiembre-2026..xlsx` | XLSX | Received; content and format comparison pending |

CSV parsing observed: semicolon delimiter and Windows-1252 encoding. The wholesale CSV lacks a header row; column labels below are **inferred from record position**, not read from a header.

## 3. Observed structures

### 3.1 Retail (minorista)

`Productos`, `Rubro`, `Categoria`, `Unidad `, `Mercado Nuevo`, `Mercado Conaprope `, `Mercado Los Mina`, `Mercado Villa Consuelo`, `Mercado Cristo Rey`, `Mercadom`, `Supermercado `, `Semana`, `Mes`, `Año`.

- 51,558 records with the expected 14 fields.
- 578 distinct product strings after trimming leading/trailing spaces (not semantically standardized).
- 24 distinct rubro strings after trimming.
- 53 distinct unit strings after trimming.
- 4,181 rows marked year 2026, including 517 marked September 2026.
- Seven separate price fields representing markets or outlet categories; these are **not** province codes.
- No exact observation date; temporal grain is represented by week label, month, and year.

### 3.2 Wholesale (mayorista)

Inferred positions: `Productos`, `Rubro`, `Categoria`, `Unidad`, `Precio`, `Semana`, `Mes`, `Año`.

- 44,533 physical CSV rows; 44,532 match the eight-column layout, while one has 14 fields and requires investigation.
- 608 distinct product strings after trimming (not semantically standardized).
- 23 distinct rubro strings after trimming.
- 113 distinct unit strings after trimming.
- 3,457 rows explicitly marked year 2026, including 413 marked September 2026; the month label also appears as lowercase `julio` in 99 of those 2026 rows.
- 229 exact duplicate eight-field records; the business meaning of duplicates is not yet established.
- Wholesale data have one price column and do not identify a market location in this CSV structure.

## 4. Preliminary data-quality findings

| Finding | Evidence | Proposed disposition |
|---|---|---|
| Zero retail prices | Examples: `Mercado Nuevo` 6,591/51,558 (12.8%); `Mercado Villa Consuelo` 14,034/51,558 (27.2%) | Investigate whether zero means unavailable; do not treat as a genuine zero price by default |
| Zero wholesale prices | 3,854/44,532 (8.7%) | Flag for source-semantic review |
| Missing/error markers | Retail `N/D`, blank, `#¡REF!`, `#¡DIV/0!`; wholesale blank and `-` | Standardize to typed missing/error statuses with raw values retained |
| Inconsistent week labels | Retail includes `Tercero`, `Segundo`, `3333`; wholesale includes `Sengunda`, `Cuanta`, `Priemera` | Establish controlled mapping with explicit exception reporting |
| Malformed wholesale row | One physical row has 14 fields rather than eight | Quarantine for review, preserve raw record |
| Wholesale duplicates | 229 exact duplicate eight-field records | Check source and intended grain before any deduplication |
| Year anomalies | Retail includes blank year and `2025\``; wholesale includes `20252025+B38846:C38849` | Flag, preserve original text and investigate |
| Nonstandard category values | Retail `Categoria` includes `Frutas` on 11 rows; wholesale has several non-`Mayorista` values | Check for source misalignment/corruption |
| Cross-format consistency | XLS/XLSX not yet reconciled to CSV | Compare row counts, schemas, values, dates, and formulas |

All counts above are preliminary and tied to the supplied CSV versions.

## 5. Analytical feasibility and limitations

**Potentially feasible after validation:** product/rubro price summaries, market-specific retail price comparisons, weekly/monthly price trends, and descriptive retail/wholesale analysis.

**Conditional:** retail-to-wholesale price spreads require verified product equivalence, matching time periods, compatible units (e.g. lb vs sack/quintal), and clarity on market coverage. Product labels alone are insufficient.

**Not supported as stated by the CSV alone:** nationwide representative price indices, province-level comparisons, exact daily price changes, or claims of complete September 2026 coverage.

Formal AGR KPI IDs and definitions must be reconciled against the project's business question/KPI catalog before publishing a KPI feasibility matrix.

## 6. Candidate normalization approach — design only

1. Preserve source file, ingestion metadata, raw row, and source column values in a future Bronze layer.
2. Unpivot the seven retail price columns into a market/outlet dimension for a candidate Silver design, while preserving original labels.
3. Parse numeric price and missing/error statuses separately; quarantine malformed rows and invalid time fields.
4. Standardize month and week labels using controlled mappings and audit fields.
5. Maintain original units and only derive normalized unit prices when conversion factors are unambiguous and validated.
6. Use a curated product mapping rather than assuming similar strings represent identical products.
7. Build Gold metrics only after validating the intended observation grain and official KPI definitions.

No Databricks objects or pipelines have been created as part of this profiling.

## 7. Candidate data-quality controls

- `DQ-AGR-001`: CSV row width and source schema validation.
- `DQ-AGR-002`: Required product, rubro, unit, period, and category checks.
- `DQ-AGR-003`: Year/month/week domain validation and anomaly logging.
- `DQ-AGR-004`: Numeric price parsing, missing/error marker classification, and zero-price review.
- `DQ-AGR-005`: Duplicate detection against a documented source business key.
- `DQ-AGR-006`: Unit dictionary and price-per-unit comparability checks.
- `DQ-AGR-007`: Cross-format CSV–XLS/XLSX reconciliation.
- `DQ-AGR-008`: Retail market coverage and completeness profiling.

## 8. Open questions / next steps

1. Inspect and reconcile the two original Excel files against their CSV counterparts, including the single malformed wholesale CSV record.
2. Identify whether zero prices mean unavailable quotations or valid observations.
3. Confirm whether weekly labels correspond to consistent observation dates and whether September 2026 is complete.
4. Resolve exact source grain and meaning of 229 wholesale duplicate rows.
5. Define a validated conversion dictionary for pounds, quintals, sacks, units, and hundreds.
6. Review the business catalog's agricultural KPI definitions and build an evidence-based feasibility matrix.
7. Record data source URLs, release/version metadata, and licensing before operational ingestion.

## 9. Project traceability

- [Documentation roadmap](../../docs/README.md)
- [MICM profiling](../micm/README.md)
- [Pro Consumidor profiling](../proconsumidor/README.md)

**Status:** Source files received; preliminary CSV profiling documented; Excel reconciliation and formal KPI validation pending.
