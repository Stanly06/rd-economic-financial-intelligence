# RD Economic & Financial Intelligence Platform
## Architecture Decision Record — Storage & Governance v1.0

**Status:** Proposed for review (not implemented)  
**Architecture:** Hybrid (ingestion/EDA by source; transformations by layer/domain)  
**Scope:** Dominican-first BCRD, MICM, Pro Consumidor, and Agriculture datasets.

### ADR-001: Unity Catalog logical layout
Use a proposed catalog `rd_economic_intelligence` with schemas:

| Schema | Purpose |
|---|---|
| `bronze` | Source-preserving Delta tables and landing Volumes |
| `silver` | Typed, validated, standardized Delta tables |
| `gold` | Approved analytical facts, dimensions, and KPI tables/views |
| `metadata` | Source registry, ingestion runs, file manifest, watermarks |
| `quality` | Rule results, anomalies, quarantine records, exceptions |

The catalog and schemas are **design targets**, subject to workspace capabilities, privileges, and cloud storage configuration.

### ADR-002: Landing files in governed Volumes
Candidate managed Volumes (subject to governance and storage decisions):

- `/Volumes/rd_economic_intelligence/bronze/bcrd_raw/`
- `/Volumes/rd_economic_intelligence/bronze/micm_raw/`
- `/Volumes/rd_economic_intelligence/bronze/proconsumidor_raw/`
- `/Volumes/rd_economic_intelligence/bronze/agriculture_raw/`

A candidate file convention is `<dataset>/ingest_date=YYYY-MM-DD/run_id=<run_id>/<original_filename>`. The original bytes must be preserved. Capture the source URL, retrieval timestamp, content hash, source license/terms, original filename, and ingestion run ID in a file manifest. Never commit raw source files or credentials to the public repository.

### ADR-003: Bronze, Silver, and Gold contracts
- **Bronze:** retain source columns, provenance, and batch identifiers; do not silently overwrite source errors.
- **Silver:** normalize names, dates, units, and types according to versioned rules; retain raw value and correction/quality status when applicable; quarantine unresolved anomalies.
- **Gold:** expose only business-defined metrics at explicit grains, with tested calculation logic and source traceability. External oil series are tagged as external drivers, not Dominican domestic observations.

### ADR-004: Metadata and data-quality controls
Proposed logical entities (not physical DDL yet):
- `metadata.source_registry`: dataset owner, URL, format, cadence, license and status.
- `metadata.ingestion_runs`: run ID, source, start/end, status, row counts and errors.
- `metadata.file_manifest`: file path, hash, extraction time, source and run ID.
- `metadata.watermarks`: source-specific last successfully processed date/identifier.
- `quality.rule_results`: rule ID, dataset, run ID, counts and severity.
- `quality.quarantine_records`: record reference, reason, source and review status.

Watermarks advance **only after** a successful, validated processing step; backfills and reruns must be idempotent. Do not assume all sources support incremental API ingestion: file snapshots may be necessary.

### ADR-005: Naming conventions
- Python modules: `snake_case.py`.
- SQL files: descriptive `snake_case.sql`; avoid duplicating DDL logic across notebooks.
- Tables: `<source>_<dataset>` in Bronze, domain-based names in Silver, `dim_`/`fact_` or business aggregates in Gold.
- Jobs: `job_<source>_<dataset>_<purpose>`; tasks: `<layer>_<domain>_<action>`.
- Data-quality rules: stable IDs per domain/source.
- All physical names are provisional until the Data Dictionary and Source-to-Target Mapping are approved.

### ADR-006: Security and deployment boundaries
- Start with one development catalog for a portfolio MVP; use environment separation (separate catalogs or deployment targets) before any production rollout.
- Use least-privilege grants and secrets management; no personal tokens in source control.
- Confirm whether managed Volumes or external Volumes are appropriate for the workspace and data retention requirements.
- Databricks Asset Bundles can be introduced for repeatable deployment when initial pipelines exist.

### Remaining decisions before implementation
1. Verify Databricks workspace cloud, Unity Catalog access, storage permissions and available compute.
2. Approve managed vs external Volumes and retention/versioning approach.
3. Define dataset-specific grains and field-level contracts in the Data Dictionary.
4. Complete agriculture profiling closure and unresolved source-quality decisions.
5. Agree on a first vertical slice (recommended: BCRD USD/DOP).

**Not implemented:** No Unity Catalog objects, Volumes, Delta tables, jobs, or pipelines have been created by this document.
