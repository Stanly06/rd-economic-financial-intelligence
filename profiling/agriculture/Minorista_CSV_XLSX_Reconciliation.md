Agricultural Retail Prices — CSV vs XLSX Reconciliation
Project: RD Economic & Financial Intelligence Platform
Source: Ministry of Agriculture, Dominican Republic
Dataset: Retail agricultural prices, August 2017–September 2026 (source filename; full temporal coverage not independently certified here)
Status: File-level reconciliation completed; source-data quality validation remains open
Date: 2026-10-11
1. Scope and methodology
Compared the supplied CSV and user-converted XLSX, in source row order, across all 14 columns. CSV was read as Windows-1252 with semicolon delimiters. XLSX cells were read from workbook XML with shared strings resolved. Comparisons were performed at three levels: exact text, normalized whitespace/numeric representation, and classification of remaining differences. A numeric absolute tolerance of 0.000001 was used only to classify file-representation differences, not to define analytical price precision or business rounding rules.
2. Results
Metric	Result
CSV data rows	51,558
XLSX data rows	51,558
Columns in each file	14
CSV rows with incorrect field count	0
Rows with exact cell-by-cell textual equality	33,996
Rows equal after trimming whitespace and normalizing numeric strings	50,561
Rows with remaining representation differences	997
Differing cells in these 997 rows	1,211
Cells with localized Excel error-label differences	257
Cells with numerical floating-point/decimal precision differences (<= 0.000001)	954
Other substantive cell differences after these classifications	0 observed


The 997 differing rows may have more than one differing cell. The 257 and 954 counts are cells, not rows. Exact textual differences outside the 997 remaining rows include harmless whitespace/numeric string formatting; they were not separately categorized.
3. Illustrative differences
- CSV #¡DIV/0! vs XLSX #DIV/0!: same spreadsheet division error, localized text.
- CSV #¡REF! vs XLSX #REF!: same spreadsheet reference error, localized text.
- CSV 44.59083333 vs XLSX 44.590833333333336: export/display precision difference.
- CSV 41.41 vs XLSX 41.410000000000004: floating-point representation difference.
Interpretation: No material numerical disagreement was detected under the stated tolerance, and both files align row by row. This does not mean the underlying source data are clean: Excel errors, missing prices, zeros, inconsistent labels, and invalid years must be treated separately.
4. Decision and proposed controls
1. Preserve both originals, including filenames, acquisition timestamps, and checksums, in controlled raw storage; do not commit them to the public repository.
2. Treat CSV and XLSX as reconciled representations, not independent observations to append together.
3. Select the canonical ingest representation based on ingestion reproducibility and metadata preservation; neither file is proven universally authoritative merely by matching.
4. Convert localized Excel errors to explicit null/error status with raw value retained for audit. Never interpret them as numeric zero.
5. Establish a business-approved rule for missing/zero prices and define product, unit, market, and weekly-date normalization before analytical aggregations.
6. Keep decimal precision rules explicit in the Source-to-Target mapping; the tolerance above is a reconciliation tolerance only.
5. Remaining open work before closing agricultural profiling
- Confirm actual temporal coverage, duplicate business keys, missing-value patterns, zero-price incidence, and market/product/unit harmonization.
- Reconcile wholesale anomalies and decide canonical ingestion for both retail and wholesale datasets.
- Map AGR-001–AGR-007 to verified source columns and approved calculation methodologies.
- Update the agricultural profiling README with this reconciliation result and record the final data-quality decisions.
Scope boundary: This document closes the retail CSV/XLSX file-level comparison, not the full agricultural source validation or production-readiness assessment.
