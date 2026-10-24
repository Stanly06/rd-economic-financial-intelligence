"""Parsers for the MEM 'Informe de Desempeño' annex workbook (Anexos .xlsx).

Bronze stores each sheet row as a list of cell values (strings, ISO dates or numbers as text).
These pure-Python functions turn those rows into tidy records for Silver.
"""
import re
from datetime import date, datetime

DISTRIBUTORS = ("Edenorte", "Edesur", "Edeeste")
MONTHS = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8,
          "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12}


def _num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _as_month(v):
    """Header cell -> first day of month, or None."""
    if isinstance(v, (datetime, date)):
        return date(v.year, v.month, 1)
    if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}(T.*| .*)?", v.strip()):
        y, m = int(v[:4]), int(v[5:7])
        return date(y, m, 1)
    return None


def split_indicator(label):
    """'Precio Medio de Venta de Energía (DOP/kWh)' -> ('Precio Medio de Venta de Energía', 'DOP/kWh')."""
    m = re.match(r"^\s*(.*?)\s*\(([^()]*)\)\s*$", label or "")
    return (m.group(1).strip(), m.group(2).strip()) if m else ((label or "").strip(), None)


def parse_ede_sheet(rows, header_row=6, label_col=1):
    """EDE's sheet: an indicator row (total of the three distributors) followed by one row per distributor.
    Monthly values sit under the month header cells. Returns dicts:
    month, indicator, unit, distributor ('Total EDE' or name), value, source_row (1-based)."""
    hdr = rows[header_row]
    month_cols = [(j, _as_month(v)) for j, v in enumerate(hdr)]
    month_cols = [(j, m) for j, m in month_cols if m]
    out, current = [], None
    for i, r in enumerate(rows):
        if i <= header_row:
            continue
        label = r[label_col] if label_col < len(r) else None
        label = label.strip() if isinstance(label, str) else label
        if not label:
            continue
        if label in DISTRIBUTORS:
            if current is None:
                continue
            dist = label
        else:
            current = split_indicator(label)
            dist = "Total EDE"
        for j, m in month_cols:
            v = _num(r[j]) if j < len(r) else None
            if v is not None:
                out.append({"month": m, "indicator": current[0], "unit": current[1], "distributor": dist,
                            "value": v, "source_row": i + 1})
    return out


def parse_period(label):
    """Tariff period header -> (start_month, end_month). Handles 'Ene - Mar 2020', 'Nov - Dic 21',
    'abr - jun 26', a single date (one month) and extra spaces."""
    if isinstance(label, (datetime, date)) or _as_month(label):
        m = _as_month(label)
        return m, m
    s = re.sub(r"\s+", " ", str(label)).strip().lower()
    m = re.fullmatch(r"([a-záé]{3})\w*\s*-\s*([a-záé]{3})\w*\s+(\d{2,4})", s)
    if not m:
        return None, None
    y = int(m.group(3)); y = y + 2000 if y < 100 else y
    a, b = MONTHS.get(m.group(1)), MONTHS.get(m.group(2))
    if not a or not b:
        return None, None
    ya = y if a <= b else y - 1
    return date(ya, a, 1), date(y, b, 1)


def parse_tariff_sheet(rows, period_row=10, type_row=11, dist_row=12, tariff_col=1, concept_col=2, first_col=3):
    """'Nuevo Regimen tarifario' sheet. Each period block has 'Tarifa Indexada/Referencia' columns per
    distributor and 'Tarifa Aplicada' columns (one shared column until Sep 2021, then per distributor).
    Header labels are written once per block and carried to the right.
    Returns dicts: period_label, period_start, period_end, period_order, tariff, concept, tariff_type
    ('reference' or 'applied'), source_tariff_type, distributor ('Todas' when shared), value, source_row."""
    width = max(len(r) for r in rows)
    pr, tr, dr = (list(rows[k]) + [None] * (width - len(rows[k])) for k in (period_row, type_row, dist_row))
    cols, period, ptype, order = [], None, None, -1
    for j in range(first_col, width):
        if pr[j] is not None and str(pr[j]).strip():
            period = pr[j]; order += 1; ptype = None
        if tr[j] is not None and str(tr[j]).strip():
            ptype = str(tr[j]).strip()
        if period is None or ptype is None:
            continue
        dist = str(dr[j]).strip() if dr[j] else "Todas"
        cols.append((j, period, order, ptype, dist))
    out, tariff, group = [], None, None
    for i in range(dist_row + 1, len(rows)):
        r = list(rows[i]) + [None] * (width - len(rows[i]))
        if r[tariff_col] and str(r[tariff_col]).strip():
            tariff = str(r[tariff_col]).strip(); group = None
        concept = str(r[concept_col]).strip() if r[concept_col] else None
        if not concept or tariff is None:
            continue
        if concept.endswith(":"):
            group = concept.rstrip(":").strip()
        full_concept = concept if (group is None or concept.endswith(":")) else f"{group} — {concept}"
        for j, period, o, ptype, dist in cols:
            v = _num(r[j])
            if v is None:
                continue
            start, end = parse_period(period)
            out.append({"period_label": str(period).strip() if not isinstance(period, (datetime, date)) else _as_month(period).isoformat(),
                        "period_start": start, "period_end": end, "period_order": o, "tariff": tariff,
                        "concept": full_concept.replace("Rago", "Rango"),
                        "tariff_type": "applied" if "aplicada" in ptype.lower() else "reference",
                        "source_tariff_type": ptype, "distributor": dist, "value": v, "source_row": i + 1})
    return out
