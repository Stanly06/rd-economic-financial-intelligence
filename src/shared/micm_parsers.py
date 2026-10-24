# ============================================================
# MICM fuel price helpers (shared by Silver notebooks)
# ============================================================
import datetime as dt
import re
import unicodedata

MONTHS = {"enero": 1, "febrero": 2, "febreo": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
          "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
          "noviembre": 11, "diciembre": 12}


def fuel_code(source_column):
    """Delta-safe, stable code for a MICM fuel column, e.g. 'GASOIL OPTIMO ' -> 'gasoil_optimo'."""
    s = unicodedata.normalize("NFKD", str(source_column)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s


def resolve_periods(rows):
    """Resolve MICM weekly intervals into real dates.

    rows: iterable of (dia_desde, dia_hasta, mes_label, anio) in file order.
    The month label is sometimes the start month and sometimes the end month of a week that
    crosses months, and labels have typos ('Febreo') and stray spaces. The start date is taken
    from the labelled month or the previous one, choosing the candidate closest to the expected
    next start (previous end + 1 day). Returns a list of (start, end, flag) with flag in
    ok | gap | overlap | repeated_period | unknown_month | unresolvable_dates.
    """
    out, prev_start, prev_end = [], None, None
    for a, b, mes, y in rows:
        m = MONTHS.get(str(mes).strip().lower())
        if m is None:
            out.append((None, None, "unknown_month"))
            continue
        y = int(y)
        cands = []
        for mm in (m, m - 1):
            yy, mm = (y - 1, 12) if mm == 0 else (y, mm)
            try:
                s = dt.date(yy, mm, int(a))
            except ValueError:
                continue
            for k in range(2, 13):
                e = s + dt.timedelta(days=k)
                if e.day == int(b):
                    cands.append((s, e))
                    break
        if not cands:
            out.append((None, None, "unresolvable_dates"))
            continue
        if prev_end is None:
            s, e = min(cands, key=lambda c: 0 if c[0].month == m else 1)
        else:
            expected = prev_end + dt.timedelta(days=1)
            s, e = min(cands, key=lambda c: abs((c[0] - expected).days))
        flag = "ok"
        if prev_end is not None:
            d = (s - prev_end).days
            flag = "ok" if d == 1 else ("repeated_period" if s <= prev_start else "overlap" if d < 1 else "gap")
        out.append((s, e, flag))
        prev_start, prev_end = s, e
    return out
