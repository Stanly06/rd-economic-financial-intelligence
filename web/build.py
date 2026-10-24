"""Build the single-file web platform: python web/build.py <data.json> <output.html>

<data.json> is the export written by src/exports/08_Web_Platform_Export
(/Volumes/rd_economic_intelligence/gold/web_exports/rd_platform_data.json), e.g.
databricks fs cp dbfs:/Volumes/rd_economic_intelligence/gold/web_exports/rd_platform_data.json data.json
"""
import json, sys, pathlib
here = pathlib.Path(__file__).parent
shell = (here / "shell.html").read_text(encoding="utf-8")
css = (here / "styles.css").read_text(encoding="utf-8")
app = (here / "app.js").read_text(encoding="utf-8")
data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = shell.replace("/*__CSS__*/", css).replace("/*__APP__*/", app).replace("/*__REAL_DATA__*/", embedded)
pathlib.Path(sys.argv[2]).write_text(out, encoding="utf-8")
print(f"{sys.argv[2]}: {len(out.encode()):,} bytes")
