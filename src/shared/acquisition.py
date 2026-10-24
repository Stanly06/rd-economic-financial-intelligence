"""Automatic acquisition of source files into the append-only raw archive.

Download notebooks find the current file of a source, download it, validate it and call ``land``:

* identical content (SHA-256) already anywhere in the archive -> nothing is written;
* otherwise the file is written unchanged to ``<landing>/<yyyy>/<mm>/<name>`` (arrival month, America/Santo_Domingo);
* if a file with the same name but different content is already archived (sources often republish under the
  same name), the new version is kept as ``<name>__<yyyy-mm-dd>.<ext>``. Nothing is ever overwritten or deleted.

Bronze picks the new files up with Auto Loader (see ``ingestion.py``).
"""
import hashlib, json, os, urllib.parse, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

USER_AGENT = "rd-economic-intelligence/1.0 (portfolio data pipeline)"
CKAN_API = "https://datos.gob.do/api/3/action/package_show?id="


def http_get(url, timeout=180):
    """GET a URL (spaces and accents in file names are percent-encoded) and return the bytes."""
    safe_url = urllib.parse.quote(url, safe=":/?=&%#")
    with urllib.request.urlopen(urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT}), timeout=timeout) as r:
        return r.read()


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
