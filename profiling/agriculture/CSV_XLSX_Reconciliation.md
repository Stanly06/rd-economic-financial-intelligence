# Agricultural Wholesale Prices — CSV vs XLSX Reconciliation

**Project:** RD Economic & Financial Intelligence Platform  
**Domain:** Agricultural Prices  
**Status:** Wholesale comparison completed at raw cell/text level; retail XLS reconciliation pending  
**Assessment date:** 2026-10-11

## 1. Inputs and method

Compared the user-provided Ministry of Agriculture wholesale CSV (`Informe-de-precios-Mayorista-Agosto-2017-Septiembre-2026..csv`) against the corresponding XLSX (`Informe-de-precios-Mayorista-Agosto-2017-Septiembre-2026..xlsx`) in original row order. CSV was read as Windows-1252, semicolon-delimited. XLSX cell values were extracted from workbook XML; shared strings were resolved. Each row was compared across eight expected fields. The comparison is **not** a validation against the issuing agency's source system.

## 2. Reconciliation summary

| Metric | Result |
|---|---:|
| CSV physical rows | 44,533 |
| XLSX worksheet rows | 44,533 |
| Exactly matching aligned rows | 44,084 |
| Rows with one or more differences | 449 |
| Difference rate | 1.008% |

| Difference class | Rows | Interpretation |
|---|---:|---|
| Text formatting, surrounding spaces, and price representation across multiple columns | 413 | Mostly presentation-level; further numeric semantic equivalence checks recommended |
| Numeric floating-point representation only | 33 | Tiny decimal serialization differences, not necessarily business-value discrepancies |
| Excel error label localization (`#NAME?` vs `#¿NOMBRE?`) | 1 | Both are error markers, not valid category values |
| Year field differs | 1 | CSV contains corrupt year text; XLSX has `2025` |
| CSV extra delimiters/columns | 1 | CSV has 14 fields, XLSX has eight |
| **Total** | **449** | Categories are mutually exclusive in this classification |

## 3. Specific exceptions

- **Aligned row 30,941:** Excel category is `#NAME?`; CSV category is `#¿NOMBRE?`. Both should be flagged and preserved in source-specific audit fields.
- **Aligned row 38,838:** CSV year is `20252025+B38846:C38849`, while XLSX year is `2025`. Preserve raw values, flag the CSV anomaly, and require an approved correction rule before Silver.
- **Aligned row 40,585:** CSV row has 14 fields because of six extra trailing empty/whitespace-separated fields; XLSX has eight. Treat as a recoverable structural exception only after confirming the trailing fields are semantically empty.
- **33 rows:** Small decimal differences caused by XLSX numeric representation, for example `5090.9090910000004` vs CSV `5090.909091`. Define numeric tolerance rather than compare formatted strings.
- **413 rows:** Differences include surrounding spaces and numbers represented as `3,700.00` versus `3700`. Do not interpret raw text inequality as a price change.

## 4. Proposed controls (not yet implemented)

1. Preserve raw CSV and XLSX files and row numbers; record checksums and source versions.
2. Parse CSV into eight expected fields; quarantine unexpected nonempty extra fields.
3. Trim surrounding whitespace in analytical fields, retaining raw values for audit.
4. Parse price with documented locale and grouping separators, then compare as decimals using an approved tolerance.
5. Map formula-error strings to a typed error status; do not convert them to legitimate categories.
6. Flag invalid year expressions and only apply source-precedence rules after documented approval.
7. Assess source-key duplicates separately from exact physical-row duplicates.
8. Reconcile the retail CSV against the supplied legacy XLS before closing this control.

## 5. Open decisions

- Confirm whether the XLSX is authoritative for wholesale exceptions, or whether both are alternative exports of a common official dataset.
- Verify that the 413 formatting-related rows have no substantive value differences after controlled normalization.
- Determine a defensible numeric precision/tolerance rule for price comparison.
- Complete the retail `.xls` versus CSV reconciliation.
- Resolve price zero semantics, unit conversions, market geography, and the agricultural KPI feasibility conditions documented in [the agriculture profiling README](README.md).

**Conclusion:** Wholesale files have equal row counts, but they are **not byte- or cell-identical**. Most observed differences are consistent with representation issues; the year anomaly and malformed CSV row are actionable data-quality exceptions. This does not yet establish a canonical source or production-ready dataset.
