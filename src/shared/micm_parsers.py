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


# ============================================================
# Weekly price notices (PDF "AVISO") published by the MICM
# ============================================================
import io
import json

NOTICES_PAGE = "https://micm.gob.do/direcciones/combustibles/avisos-semanales-de-precios/avisos-semanales-de-precios-de-combustibles/"

# Notice row label (normalised prefix) -> column name used by the open-data file, so both sources share the same fuel_code.
# The notice has one EGP row for "interconnected and not interconnected"; it feeds the NO INTERC column (the INTERC
# columns of the open-data file are zero in recent years). Longer prefixes are tried first.
NOTICE_COLUMNS = {
    "gasolina premium": "GASOLINA PREMIUM",
    "gasolina regular": "GASOLINA REGULAR",
    "gasoil regular egp-c": "GASOIL REGULAR EGP-C (NO INTERC)",
    "gasoil regular egp-t": "GASOIL REGULAR EGP-T (NO INTERC)",
    "gasoil regular": "GASOIL REGULAR",
    "gasoil optimo": "GASOIL OPTIMO ",
    "avtur": "AVTUR ",
    "kerosene": "KEROSENE",
    "fuel oil 1% azufre (fo6, 1%s) egp-c": "FUEL OIL  1% AZUFRE (FO6, 1%S) (EGP-C (INTERC)",
    "fuel oil 1% azufre (fo6, 1%s) egp-t": "FUEL OIL  1% AZUFRE (FO6, 1%S) (EGP-T (INTERC)",
    "fuel oil 1% azufre": "FUEL OIL 1% AZUFRE (FO6, 1%S)",
    "fuel oil egp-c": "FUEL OIL EGP-C (NO INTERC)",
    "fuel oil egp-t": "FUEL OIL EGP-T (NO INTERC)",
    "fuel oil": "FUEL OIL ",
    "gas licuado": "GLP ",
}
_PREFIXES = sorted(NOTICE_COLUMNS, key=len, reverse=True)
CORE_FUELS = ["GASOLINA PREMIUM", "GASOLINA REGULAR", "GASOIL REGULAR", "GASOIL OPTIMO ", "GLP "]
_NUM = re.compile(r"^\(?-?[\d,]+\.\d{2}\)?$")
_PERIOD = re.compile(r"\((\d{1,2})\)\s+de\s+([a-záéíóú]+)\s+al\s+d[ií]a\s+[a-záéíóú]+\s+(?:[a-záéíóú]+\s+)*\((\d{1,2})\)\s+de\s+([a-záéíóú]+)"
                     r"\s+de\s+dos\s+mil\s+[a-záéíóú\s]+?\((\d{4})\)", re.I)


def notice_links(html):
    """PDF notice URLs listed on the MICM page, newest first as published (deduplicated, order kept)."""
    seen, out = set(), []
    for u in re.findall(r'href="([^"]*AVISO[^"]*\.pdf)"', html, flags=re.I):
        if u not in seen:
            seen.add(u); out.append(u)
    return out


def _to_number(tok):
    neg = tok.startswith("(")
    v = float(tok.strip("()").replace(",", ""))
    return -v if neg else v


def _norm_label(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s.replace("( ", "(")).strip()


def parse_notice_header(text):
    """Week (start, end) and the exchange rate printed in a notice's text. The rate is None when it cannot be read."""
    flat = re.sub(r"\s+", " ", text)
    m = _PERIOD.search(flat)
    if not m:
        raise ValueError("notice period not found: layout changed")
    d1, m1, d2, m2, y = int(m[1]), MONTHS.get(m[2].lower()), int(m[3]), MONTHS.get(m[4].lower()), int(m[5])
    if m1 is None or m2 is None:
        raise ValueError(f"unknown month in notice period: {m[2]!r}/{m[4]!r}")
    start = dt.date(y - 1 if m1 > m2 else y, m1, d1)
    end = dt.date(y, m2, d2)
    if not 5 <= (end - start).days <= 7:
        raise ValueError(f"unexpected notice length: {start} to {end}")
    fx = re.search(r"TasadeCambio.*?RD\$(\d{2}\.\d{2})", re.sub(r"\s+", "", text))
    return start, end, (float(fx[1]) if fx else None)


def parse_notice_words(words, page_width):
    """Fuel rows of a notice from positioned words (pdfplumber ``extract_words``: text, x0, top).

    The PDFs are not built the same way every week (label before or after the numbers in reading order, characters
    spaced out), so rows are rebuilt from coordinates: each label line takes the numbers printed at the same height.
    The public price is the second-to-last number of the row (the last one is the week-on-week variation); the
    leftmost columns can be garbled when the source overprints them, so they are never read.
    Returns {open_data_column: price DOP/gal}.
    """
    nums = [w for w in words if _NUM.match(w["text"])]
    labels = sorted((w for w in words if not _NUM.match(w["text"]) and w["x0"] < page_width * 0.4), key=lambda w: (w["top"], w["x0"]))
    lines, cur = [], []
    for w in labels:                                   # cluster label words into lines by height
        if cur and abs(w["top"] - cur[-1]["top"]) > 2:
            lines.append(cur); cur = []
        cur.append(w)
    if cur:
        lines.append(cur)
    prices = {}
    for line in lines:
        text = _norm_label(" ".join(w["text"] for w in sorted(line, key=lambda w: w["x0"])))
        col = next((NOTICE_COLUMNS[p] for p in _PREFIXES if text.startswith(p)), None)
        if col is None or col in prices:
            continue
        top = sum(w["top"] for w in line) / len(line)
        row = sorted((w for w in nums if abs(w["top"] - top) <= 3), key=lambda w: w["x0"])
        if len(row) >= 2:                              # the 'AVTUR 6.5%' header has no numbers at its height
            prices[col] = _to_number(row[-2]["text"])
    return prices


def parse_notice_pdf(data):
    """Parse the bytes of a weekly notice PDF (needs pdfplumber). Fails if the layout contract is broken."""
    import pdfplumber
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        page = pdf.pages[0]
        text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
        words = [w for pg in pdf.pages for w in pg.extract_words(x_tolerance=6, y_tolerance=2)]
        width = page.width
    start, end, fx = parse_notice_header(text)
    prices = parse_notice_words(words, width)
    missing = [c for c in CORE_FUELS if c not in prices]
    if missing:
        raise ValueError(f"notice {start}: core fuels not found {missing}: layout changed")
    bad = {c: p for c, p in prices.items() if not 50 < p < 1000}
    if bad:
        raise ValueError(f"notice {start}: implausible prices {bad}")
    return {"start": start, "end": end, "fx_dop_usd": fx, "prices": prices}
