"""Build the web platform: python web/build.py <rd_platform_data.json> <output_dir>

Writes <output_dir>/index.html (page, ~45 KB), data/core.json (all pages except agriculture)
and data/agri.json (loaded only when the agriculture page opens).
<rd_platform_data.json> is the export of src/exports/08_Web_Platform_Export
(databricks fs cp dbfs:/Volumes/rd_economic_intelligence/gold/web_exports/rd_platform_data.json data.json).
"""
import json, sys, pathlib
from datetime import date
here = pathlib.Path(__file__).parent
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
d = json.loads(src.read_text(encoding="utf-8"))
dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))

# Exchange rate: daily for the last five years (+30 earlier days for the moving average); month-end closes and annual averages since 1991
fx = d["fx"]; last = date.fromisoformat(fx["d"][-1]); cut = date(last.year - 5, last.month, 1).isoformat()
i0 = max(0, next(i for i, x in enumerate(fx["d"]) if x >= cut) - 30)
daily = {k: v[i0:] for k, v in fx.items()}
fxm = {"m": [], "d": [], "s": [], "b": [], "a": []}; acc = {}
for x, b, s in zip(fx["d"], fx["b"], fx["s"]):
    m = x[:7]
    if not fxm["m"] or fxm["m"][-1] != m:
        fxm["m"].append(m); fxm["d"].append(x); fxm["s"].append(s); fxm["b"].append(b); acc[m] = []
    fxm["d"][-1], fxm["s"][-1], fxm["b"][-1] = x, s, b
    acc[m].append(s)
fxm["a"] = [round(sum(acc[m]) / len(acc[m]), 4) for m in fxm["m"]]
years = sorted({x[:4] for x in fx["d"]})
fxy = {"y": years, "a": [round(sum(s for x, s in zip(fx["d"], fx["s"]) if x[:4] == y) / sum(1 for x in fx["d"] if x[:4] == y), 4) for y in years]}

# Agriculture summary for the overview page (the full agriculture data is loaded lazily)
A = d["agri"]; am = len(A["m"]) - 1; ALL = A["markets"].index("Promedio mercados")
moms = [(s[5][am] / s[5][am - 1] - 1) * 100 for s in A["s"] if s[0] == 0 and s[1] == ALL and s[5][am] is not None and s[5][am - 1] is not None]
rub_yoy = [[r["r"], r["yoy"][-1]] for r in A["rub"] if r["c"] == "retail" and r["m"][-1] == A["m"][am] and r["yoy"][-1] is not None]
agri_sum = {"m": A["m"][am], "mom": round(sum(moms) / len(moms), 4), "up": sum(1 for v in moms if v > 0), "n": len(moms), "rubYoy": rub_yoy}

core = {k: v for k, v in d.items() if k != "agri"}
core.update({"fx": daily, "fxm": fxm, "fxy": fxy, "agriSum": agri_sum})
(out / "data").mkdir(parents=True, exist_ok=True)
(out / "data" / "core.json").write_text(dump(core), encoding="utf-8")
(out / "data" / "agri.json").write_text(dump(A), encoding="utf-8")
shell = (here / "shell.html").read_text(encoding="utf-8")
page = shell.replace("/*__CSS__*/", (here / "styles.css").read_text(encoding="utf-8")).replace("/*__APP__*/", (here / "app.js").read_text(encoding="utf-8"))
(out / "index.html").write_text(page, encoding="utf-8")
for f in ("index.html", "data/core.json", "data/agri.json"):
    print(f"{f}: {(out / f).stat().st_size / 1024:,.1f} KB")
