# MEM Electricity — Data Discovery & Profiling

**Project:** RD Economic & Financial Intelligence Platform
**Status:** Validated in development (2026-10-24); pipelines implemented — **not production approved**
**Business traceability:** BQ-010 and ENE-001 to ENE-009 in `03_Business_Questions_KPI_Catalog`.

## Sources assessed

| Source | Format | Usable? | Notes |
|---|---|---|---|
| SIE quarterly tariff resolutions (e.g. SIE-079-2026-TF) | Scanned PDF | Only by manual transcription | Legal source of regulated tariffs |
| MEM *Informe de Desempeño de las EEE* (monthly report) | PDF with text | Yes, one month per file | Used for reconciliation |
| MEM *Informe de Desempeño — Anexos* | XLSX | **Yes — primary** | Latest file carries the full history |
| Open-data portal | — | No dataset found | |

## Annex structure (July 2026 file)

- `EDE's`: indicator rows (total of the three distributors) each followed by Edenorte, Edesur and Edeeste rows; 211 monthly columns (January 2009 to July 2026) plus year-to-date and annual summary columns. 38 indicators: energy purchased and billed, average purchase and selling prices (cUSD/kWh and DOP/kWh), billing, collections, losses, collection rate, CRI, customers, employees, expenses.
- `Nuevo Regimen tarifario`: tariff charges (RD$) for BTS1, BTS2, BTD, BTH, MTD1, MTD2 and MTH, by period since January 2020. Each period block has a reference ("Tarifa Indexada" until September 2021, then "Tarifa Referencia") per distributor and an applied tariff (one shared column until September 2021, then per distributor).
- Other sheets (generation, CDEEE, EGEHID, ETED, financial annexes, the 2013–2019 tariff regime) are out of scope for now.

## Findings

- Percent indicators are fractions (0.43 = 43%).
- Period labels are inconsistent (`Oct  - Dic 2020`, a single date for October 2021, `Nov - Dic 21`, `abr - may 26`); parsed by `src/shared/mem_parsers.py`.
- Two periods overlap: `abr - may 26` and `abr - jun 26`.
- DOP/kWh selling price for May 2026 matches the MEM PDF (Edenorte 10.13, Edesur 10.51).

## Automatic acquisition

The MEM website exposes its uploads through the WordPress REST API (`https://mem.gob.do/wp-json/wp/v2/media?search=Anexos`). `06_MEM_Electricity_Download` picks the newest `.xlsx` whose name contains `Desempeno` and `Anexos`, skips it when the same content (SHA-256) is already archived, validates the required sheets and writes it unchanged to an append-only archive, one folder per arrival month (`ede_performance/<yyyy>/<mm>/`). A republished file whose name is already archived but whose content changed is kept as a new version (`<name>__<yyyy-mm-dd>.xlsx`). File names vary month to month (`-vf`, `._-`), so selection is by publication date, not by name pattern.

Do not commit the original workbook; it is kept in the Volume `bronze.mem_raw/ede_performance/`. Files are never overwritten or deleted there: the Volume, not Delta time travel, is the long-term archive of what MEM published.
