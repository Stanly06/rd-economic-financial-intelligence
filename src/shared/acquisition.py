"""Automatic acquisition of source files into the append-only raw archive.

Download notebooks find the current file of a source, download it, validate it and call ``land``:

* identical content (SHA-256) already anywhere in the archive -> nothing is written;
* otherwise the file is written unchanged to ``<landing>/<yyyy>/<mm>/<name>`` (arrival month, America/Santo_Domingo);
* if a file with the same name but different content is already archived (sources often republish under the
  same name), the new version is kept as ``<name>__<yyyy-mm-dd>.<ext>``. Nothing is ever overwritten or deleted.

Bronze picks the new files up with Auto Loader (see ``ingestion.py``).

Source availability: a source that cannot be reached after three attempts (connection or timeout error, invalid TLS
certificate, HTTP 5xx) raises ``SourceUnavailable``. Download notebooks catch it with ``source_unavailable``: the outage
is logged in ``quality.source_availability``, the task ends as a warning (``SOURCE_UNAVAILABLE``) and the source keeps its
last data. TLS verification is never disabled. An HTTP 4xx (file moved or access changed), a layout change or a failed
validation is still an error, because it needs a fix in the project.
"""
import hashlib, json, os, time, urllib.error, urllib.parse, urllib.request
from datetime import timezone
from datetime import datetime
from zoneinfo import ZoneInfo

USER_AGENT = "rd-economic-intelligence/1.0 (portfolio data pipeline)"
CKAN_API = "https://datos.gob.do/api/3/action/package_show?id="


class SourceUnavailable(Exception):
    """The source could not be reached (network, TLS certificate or server error). Not a project defect."""


def http_get(url, timeout=180, attempts=3):
    """GET a URL (spaces and accents in file names are percent-encoded) and return the bytes.

    Retries transient failures; raises SourceUnavailable when the source stays unreachable, and lets HTTP 4xx through."""
    safe_url = urllib.parse.quote(url, safe=":/?=&%#")
    last = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT}), timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500:
                raise
            last = e
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = e
        if attempt < attempts:
            time.sleep(10 * attempt)
    raise SourceUnavailable(f"{url} unreachable after {attempts} attempts: {last!r}")


def source_unavailable(dbutils, spark, source, error):
    """Log the outage, mark the task as 'nothing downloaded' and end it as a warning (the source keeps its last data)."""
    detail = str(error)[:1000]
    print(f"WARNING · source unavailable · {source}: {detail}")
    try:
        spark.createDataFrame([(source, "UNAVAILABLE", detail, datetime.now(timezone.utc))],
                              "source string, status string, detail string, checked_ts timestamp") \
             .write.mode("append").saveAsTable("rd_economic_intelligence.quality.source_availability")
    except Exception as e:  # logging must never turn the warning into a failure
        print(f"Could not log the outage: {e!r}")
    dbutils.jobs.taskValues.set(key="downloaded", value=False)
    dbutils.notebook.exit(json.dumps({"status": "SOURCE_UNAVAILABLE", "source": source, "reason": detail}, ensure_ascii=False))


def ckan_resources(package_id, formats):
    """Current download URL per format for a dataset of the national open-data portal (datos.gob.do, CKAN)."""
    package = json.loads(http_get(CKAN_API + package_id, timeout=60))["result"]
    found = {}
    for r in package.get("resources", []):
        fmt = (r.get("format") or "").strip().lower()
        if fmt in formats and fmt not in found:
            found[fmt] = r["url"]
    missing = [f for f in formats if f not in found]
    if missing:
        raise RuntimeError(f"datos.gob.do package '{package_id}' has no {missing} resource")
    return found, package.get("metadata_modified")


def _archived_files(landing):
    for root, dirs, files in os.walk(landing):
        dirs[:] = [d for d in dirs if not d.startswith("_")]   # skip _checkpoints
        for f in files:
            yield os.path.join(root, f)


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def land(data, name, landing, now=None):
    """Write ``data`` to the archive unless identical content is already there. Returns a status dict."""
    now = now or datetime.now(ZoneInfo("America/Santo_Domingo"))
    digest = hashlib.sha256(data).hexdigest()
    archived = list(_archived_files(landing))
    for p in archived:
        if os.path.getsize(p) == len(data) and _sha256_file(p) == digest:
            return {"status": "SKIPPED", "file": name, "reason": f"same content already archived as {p[len(landing):]}"}
    stem, ext = name.rsplit(".", 1)
    is_correction = any(os.path.basename(p) == name for p in archived)
    out_name = f"{stem}__{now:%Y-%m-%d}.{ext}" if is_correction else name
    target_dir = f"{landing}{now:%Y}/{now:%m}/"
    os.makedirs(target_dir, exist_ok=True)
    if os.path.exists(target_dir + out_name):
        out_name = f"{stem}__{now:%Y-%m-%d_%H%M%S}.{ext}"
    with open(target_dir + out_name, "wb") as fh:
        fh.write(data)
    return {"status": "DOWNLOADED", "path": target_dir[len(landing):] + out_name, "new_version_of_archived_name": is_correction,
            "bytes": len(data), "sha256": digest[:16]}
