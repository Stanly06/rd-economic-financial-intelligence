# MICM Fuel Prices — Data Discovery & Profiling

**Project:** RD Economic & Financial Intelligence Platform  
**Status:** Validated in development (2026-10-23); pipelines implemented — **not production approved**  
**Source:** Dominican Republic Ministry of Industry, Commerce and MSMEs (MICM), via Dominican open-data portal  
**Business traceability:** Fuel price monitoring and FUEL-001 through FUEL-012 in `03_Business_Questions_KPI_Catalog`.

## Source files

- `precios-de-combustibles-2010-2026.csv` — original downloaded file, semicolon-delimited, Windows-1252-compatible encoding.
- `precios-de-combustibles-2010-2026.xlsx` — original downloaded spreadsheet; retain separately for source-value reconciliation.
- Do not commit original source data to the public repository until publication rights, licensing, and repository data policy are reviewed. Originals are preserved in the append-only archive `bronze.micm_raw/fuel_prices/<yyyy>/<mm>/` (one folder per arrival month, never overwritten).

## Verified CSV profiling

| Check | Result |
|---|---|
| Data records | 872 |
| Source fields | 26 |
| First listed price interval | 2–8 January 2010 |
| Last listed price interval | 22–28 August 2026 |
| Observed grain | One record per listed weekly price interval, with exceptions |
| Blank CSV field values | 0 |
| Repeated period keys | 4 consecutive weeks published twice |
| Repeated periods | 9–15, 16–22, 23–29 December 2023 and 30 December 2023 – 5 January 2024 |

**Caution:** No blank field values does not imply complete or valid prices. Zero values and publication gaps require separate tests. Weekly continuity, units, precision and date semantics remain to be validated.

## CSV vs XLSX reconciliation

Prior comparison found different numeric precision between formats, including gasoline regular for the first period (CSV `151` vs XLSX `150.7`). Therefore **CSV and XLSX must not be assumed value-equivalent**. Use XLSX as a *candidate* precision-preserving backfill source, pending comprehensive field-level reconciliation against official publication values. Avoid unverified global discrepancy counts.

## Resolution (2026-10-23)

| Open question | Decision | Evidence |
|---|---|---|
| Authoritative format | **XLSX** | Every CSV value equals the XLSX value rounded to whole pesos: 0 differences above 0.5 on 19,184 comparable values. The CSV loses centavos (e.g. `151` vs `150.7`). |
| Repeated December 2023 weeks | Keep the **later block** in the file; earlier rows go to `quality.dq_rejected_records` | The later block follows the file order of publication; values differ for some fuels. |
| Zero prices | **Not published** (NULL, `is_published = false`) | Zeros match periods when a product was not sold, e.g. Gasoil Óptimo before November 2012. 3,800 values. |
| Unit | DOP per gallon | Unit used in MICM weekly price notices; to confirm in the dataset metadata. |
| Week dates | Rebuilt by [`src/shared/micm_parsers.py`](../../src/shared/micm_parsers.py) | The month label is sometimes the start, sometimes the end month, and has typos (`Febreo`). 864 weeks contiguous; 3 gaps and 3 overlaps reported. |

Implemented in `src/bronze|silver|gold/04_MICM_Fuel_Prices_*` (see [docs](../../docs/README.md)).

## Candidate Silver schema (original proposal)

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

## Automatic acquisition

The dataset is published on the national open-data portal (datos.gob.do, CKAN dataset `precios-de-los-combustibles`, organization MICM); the files themselves are served from `micm.gob.do/transparencias/datos-abiertos/precios-de-combustibles/`. The file name carries the year range, so `04_MICM_Fuel_Prices_Download` reads the current URL from the CKAN API on every run. The portal file was newer than the manually landed copy (877 vs 872 weeks).

## Weekly notices (PDF), the newest weeks (added 2026-11-23)

The open-data file is updated late: on 23 Nov 2026 it ended at the week 31 Oct–6 Nov, while the MICM page *Avisos semanales de precios de combustibles* already listed the notices up to 21–27 Nov (signed the Friday before the week starts). Each notice is a one-page PDF with a fixed table (parity price, taxes, margins, official price, public price, variation) and the exchange rate used.

| Check | Result |
|---|---|
| Same price as the open-data file | Week 31 Oct–6 Nov: premium 358.10 (file 358), regular 317.50 (317), gasoil regular 270.80 (270), GLP 135.20 (135). The file shows the whole-peso part; the notice carries the centavos. |
| Layout | Not identical every week: in some PDFs the label comes after the numbers in reading order and the characters are spaced out. The parser rebuilds each row from word coordinates (`micm_parsers.parse_notice_words`) and reads the second-to-last number of the row (the last one is the weekly variation). |
| Cross-check | The prices read by the parser were checked against a second extractor (`pdftotext -layout`) on four notices: every price appears in the text. |
| Mapping | 15 notice rows map to the open-data columns. The notice has one EGP row for "interconnected and not interconnected"; it feeds the `NO INTERC` column. |
| Rule in Silver | The open-data file wins for any week it has; the notices only add later weeks. Where both exist they are compared (tolerance 1 peso); the EGP columns differ by 2 to 3 pesos in some weeks, so that check reports a warning, not a failure. |

## Open decisions and next actions

- Resolve the three December 2023 repeated intervals using source documentation.
- Audit numerical differences across formats and choose authoritative backfill representation.
- Verify currency/price unit and the meaning of special EGP categories.
- Confirm source publication cadence and whether a stable machine-readable incremental feed exists.
- Continue discovery for Pro Consumidor, Agriculture, and EIA (oil is an external driver only).
- Feed verified fields into `05_Data_Dictionary`, transformations into `06_Source-to-Target_Mapping`, and architecture into `07_Solution_Architecture` before creating Databricks tables.

**RD-first:** MICM fuel prices are Dominican domestic indicators. International oil prices must be explicitly tagged as external explanatory drivers, not Dominican prices.
