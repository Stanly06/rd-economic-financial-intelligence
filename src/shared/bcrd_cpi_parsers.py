# ============================================================
# BCRD CPI parsers: Bronze raw rows -> tidy Silver records
# Input per dataset: list of (source_row_number, cells) where cells is a list of
# strings exactly as captured in Bronze (None for empty cells).
# Output: list of dicts (tidy records) + list of rejected dicts.
# ============================================================
import re
from datetime import date

MONTHS = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}


def cell(cells, i):
    if i >= len(cells) or cells[i] is None:
        return None
    v = str(cells[i]).strip()
    return v if v not in ("", "None") else None


def to_year(v):
    if v is None:
        return None
    m = re.fullmatch(r"(\d{4})(\.0)?", v)
    return int(m.group(1)) if m else None


def to_month(v):
    return MONTHS.get(v.strip().lower()) if v else None


def to_num(v):
    if v is None or v in ("-", "--", "n.d.", "nd"):
        return None
    try:
        return float(v)
    except ValueError:
        return "INVALID"


def _num_or_reject(v, name, rejects, base):
    n = to_num(v)
    if n == "INVALID":
        rejects.append({**base, "rule_name": f"numeric_{name}", "raw_value": v})
        return None, False
    return n, True


def parse_year_month_rows(rows, year_col, month_col, value_specs, dataset, year_on_own_row=False):
    """Generic parser for 'Período' layouts: year appears once per block, month on each row.

    value_specs: list of (column_index, output_field, required)
    Returns (records, rejects).
    """
    records, rejects = [], []
    current_year = None
    for row_num, cells in rows:
        y_cell = cell(cells, year_col)
        m_cell = cell(cells, month_col)
        y = to_year(y_cell)
        if y is not None:
            current_year = y
        month = to_month(m_cell)
        if month is None:
            continue  # header, footnote, blank or year-only row
        if current_year is None:
            rejects.append({"dataset": dataset, "source_row_number": row_num,
                            "rule_name": "year_not_found", "raw_value": m_cell})
            continue
        base = {"dataset": dataset, "source_row_number": row_num}
        rec = {"reference_month": date(current_year, month, 1), "source_row_number": row_num}
        ok = True
        for col, field, required in value_specs:
            n, valid = _num_or_reject(cell(cells, col), field, rejects, base)
            ok = ok and valid
            if required and n is None and valid:
                rejects.append({**base, "rule_name": f"missing_{field}", "raw_value": None})
                ok = False
            rec[field] = n
        if ok:
            records.append(rec)
    return records, rejects


def find_header_row(rows, token="Período"):
    for row_num, cells in rows:
        if cell(cells, 0) and cell(cells, 0).startswith(token):
            return row_num, cells
    raise ValueError(f"Header row with '{token}' not found")


# ---------------- Dataset parsers ----------------

def parse_cpi_national(rows):
    # Período | (month) | Indice | Mensual | con Dic. | 12 meses | Promedio 12 meses
    return parse_year_month_rows(
        rows, 0, 1,
        [(2, "cpi_index", True), (3, "mom_pct", False), (4, "ytd_pct", False),
         (5, "yoy_pct", False), (6, "avg_12m_pct", False)],
        "cpi_national")


def parse_cpi_core(rows):
    # Two blocks: annual December rows 'Dic. YYYY' then monthly rows (year | month).
    records, rejects = parse_year_month_rows(
        rows, 0, 1,
        [(2, "core_cpi_index", True), (3, "mom_pct", False), (4, "ytd_pct", False), (5, "yoy_pct", False)],
        "cpi_core")
    for r in records:
        r["observation_type"] = "monthly"
    monthly_keys = {r["reference_month"] for r in records}
    for row_num, cells in rows:
        v = cell(cells, 0)
        m = re.fullmatch(r"Dic\.\s*(\d{4})", v or "")
        if not m:
            continue
        ref = date(int(m.group(1)), 12, 1)
        if ref in monthly_keys:
            continue  # the monthly block already has this December
        base = {"dataset": "cpi_core", "source_row_number": row_num}
        idx, ok1 = _num_or_reject(cell(cells, 2), "core_cpi_index", rejects, base)
        ytd, ok2 = _num_or_reject(cell(cells, 4), "ytd_pct", rejects, base)
        if ok1 and ok2 and idx is not None:
            records.append({"reference_month": ref, "source_row_number": row_num,
                            "core_cpi_index": idx, "mom_pct": None, "ytd_pct": ytd,
                            "yoy_pct": ytd,  # December: accumulated = 12-month
                            "observation_type": "annual_december"})
    return records, rejects


def parse_cpi_groups(rows):
    # Header row: 'Período', group names on odd columns (index + var% pairs).
    hdr_row, hdr = find_header_row(rows)
    groups = [(i, " ".join(cell(hdr, i).split())) for i in range(1, len(hdr)) if cell(hdr, i)]
    records, rejects = [], []
    for col, group in groups:
        recs, rej = parse_year_month_rows(
            rows, 0, 0, [(col, "group_index", True), (col + 1, "mom_pct", False)], "cpi_groups")
        for r in recs:
            r["expenditure_group"] = group
        records += recs
        rejects += rej
    return records, rejects, [g for _, g in groups]


REGION_STANDARD = {
    "región ozama": "Ozama",
    "región norte": "Norte o Cibao",
    "región norte o cibao": "Norte o Cibao",
    "región este": "Este",
    "región sur": "Sur",
}


def standard_region(label):
    key = " ".join(label.replace("*", "").split()).lower()
    if key not in REGION_STANDARD:
        raise ValueError(f"Unknown region label: {label!r}")
    return REGION_STANDARD[key]


def parse_cpi_regions(rows):
    hdr_row, hdr = find_header_row(rows)
    regions = [(i, cell(hdr, i).replace("*", "").strip()) for i in range(2, len(hdr))
               if cell(hdr, i) and cell(hdr, i).lower().startswith("región")]
    records, rejects = [], []
    for col, region in regions:
        recs, rej = parse_year_month_rows(
            rows, 0, 1, [(col, "cpi_index", True), (col + 1, "mom_pct", False)], "cpi_regions")
        for r in recs:
            r["region"] = standard_region(region)
            r["region_source_label"] = region
        records += recs
        rejects += rej
    return records, rejects, [r for _, r in regions]


def parse_basket(rows, dataset, segment_type):
    hdr_row, hdr = find_header_row(rows)
    segments = [(i, cell(hdr, i).replace("*", "").strip()) for i in range(2, len(hdr)) if cell(hdr, i)]
    records, rejects = [], []
    for col, segment in segments:
        recs, rej = parse_year_month_rows(rows, 0, 1, [(col, "basket_cost_dop", True)], dataset)
        for r in recs:
            seg_type = "national" if segment.lower() == "nacional" else segment_type
            std = standard_region(segment) if seg_type == "region" else segment
            r.update({"segment_type": seg_type, "segment": std, "segment_source_label": segment})
            # BCRD note: quintile series before Oct-2020 is a retropolation
            r["is_retropolated"] = dataset == "basket_quintiles" and r["reference_month"] < date(2020, 10, 1)
        records += recs
        rejects += rej
    return records, rejects, [s for _, s in segments]
