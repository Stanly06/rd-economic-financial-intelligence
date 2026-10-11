# MICM Fuel Prices — Data Discovery & Profiling

**Project:** RD Economic & Financial Intelligence Platform  
**Status:** Discovery / conditional backfill candidate — **not production approved**  
**Source:** Dominican Republic Ministry of Industry, Commerce and MSMEs (MICM), via Dominican open-data portal  
**Business traceability:** Fuel price monitoring and FUEL-001 through FUEL-012 in `03_Business_Questions_KPI_Catalog`.

## Source files

- `precios-de-combustibles-2010-2026.csv` — original downloaded file, semicolon-delimited, Windows-1252-compatible encoding.
- `precios-de-combustibles-2010-2026.xlsx` — original downloaded spreadsheet; retain separately for source-value reconciliation.
- Do not commit original source data to the public repository until publication rights, licensing, and repository data policy are reviewed. Preserve originals in the controlled raw landing area.

## Verified CSV profiling

| Check | Result |
|---|---|
| Data records | 872 |
| Source fields | 26 |
| First listed price interval | 2–8 January 2010 |
| Last listed price interval | 22–28 August 2026 |
| Observed grain | One record per listed weekly price interval, with exceptions |
| Blank CSV field values | 0 |
| Repeated period keys | 3 distinct periods repeated twice each |
| Repeated periods | 9–15, 16–22, 23–29 December 2023 |

**Caution:** No blank field values does not imply complete or valid prices. Zero values and publication gaps require separate tests. Weekly continuity, units, precision and date semantics remain to be validated.

## CSV vs XLSX reconciliation

Prior comparison found different numeric precision between formats, including gasoline regular for the first period (CSV `151` vs XLSX `150.7`). Therefore **CSV and XLSX must not be assumed value-equivalent**. Use XLSX as a *candidate* precision-preserving backfill source, pending comprehensive field-level reconciliation against official publication values. Avoid unverified global discrepancy counts.

## Candidate Silver schema (subject to profiling)

| Field | Meaning |
|---|---|
| `period_start_date` | Official start date of price interval |
| `period_end_date` | Official end date of price interval |
| `fuel_type` | Standardized source fuel category |
| `price_dop` | Published price, with source precision preserved |
| `price_unit` | Unit from official metadata; not yet verified |
| `source_file` | Raw artifact lineage |
| `ingestion_timestamp` | Technical lineage |

Proposed business key: (`period_start_date`, `period_end_date`, `fuel_type`) **after resolving source duplicate periods**. Unpivot fuel-price columns into long format for Silver; preserve original source field names and original values in Raw/Bronze.

## Candidate data-quality rules

1. Valid and ordered period start/end dates; investigate gaps and overlaps.
2. Duplicate candidate business keys are flagged for manual reconciliation, not silently dropped.
3. Price values must be parseable and units must be documented.
4. Zero prices are flagged and investigated per product/period, not blindly converted to null.
5. Validate price precision, including CSV vs XLSX differences.
6. Reconcile weekly period counts and latest publication date with official MICM updates.
7. Validate calculated FUEL KPIs only after establishing a trustworthy weekly price series.

## Open decisions and next actions

- Resolve the three December 2023 repeated intervals using source documentation.
- Audit numerical differences across formats and choose authoritative backfill representation.
- Verify currency/price unit and the meaning of special EGP categories.
- Confirm source publication cadence and whether a stable machine-readable incremental feed exists.
- Continue discovery for Pro Consumidor, Agriculture, and EIA (oil is an external driver only).
- Feed verified fields into `05_Data_Dictionary`, transformations into `06_Source-to-Target_Mapping`, and architecture into `07_Solution_Architecture` before creating Databricks tables.

**RD-first:** MICM fuel prices are Dominican domestic indicators. International oil prices must be explicitly tagged as external explanatory drivers, not Dominican prices.
