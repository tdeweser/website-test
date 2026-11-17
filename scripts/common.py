"""Shared helpers for the scrape / build / check scripts.

Everything that encodes a *rule* of the site (which hosts count as "the old site",
how URLs and slugs are formed, which pages are permanent) lives here so the three
scripts cannot drift apart. See docs/ARCHITECTURE.md.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
MEDIA = STATIC / "media"          # served at /media/
TEMPLATES = ROOT / "templates"
PUBLIC = ROOT / "public"
DESIGN_SYSTEM = ROOT / "design-system"
CACHE = ROOT / ".cache"
DOCS = ROOT / "docs"

SITE = "https://www.ipe.nl"

# Hosts that are "the old site". Nothing in public/ may point at these
# (mailto: addresses excepted). instituut-pe.nl is the institute's former domain.
OLD_HOSTS = {"www.ipe.nl", "ipe.nl", "www.instituut-pe.nl", "instituut-pe.nl"}
# Squarespace asset hosts: every file found on these is downloaded into static/media.
ASSET_HOSTS = {
    "images.squarespace-cdn.com",
    "static1.squarespace.com",
    "file.squarespace-cdn.com",
}

USER_AGENT = "Mozilla/5.0 (compatible; IPE-site-migration/1.0)"


def load_config() -> dict:
    with open(CONTENT / "site.yml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------------------------------------------------------- HTTP

_last_request: dict[str, float] = {}


def fetch(url: str, *, binary: bool = False, delay: float = 0.6, use_cache: bool = True):
    """GET a URL politely (per-host delay) with an on-disk cache in .cache/http/.

    Returns str (or bytes when binary=True). Raises urllib.error.HTTPError on 4xx/5xx.
    """
    key = hashlib.sha1(url.encode("utf-8")).hexdigest()
    path = CACHE / "http" / key[:2] / key
    if use_cache and path.exists():
        data = path.read_bytes()
        return data if binary else data.decode("utf-8", "replace")

    host = urllib.parse.urlsplit(url).netloc
    wait = delay - (time.time() - _last_request.get(host, 0))
    if wait > 0:
        time.sleep(wait)

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as err:
            if err.code in (404, 410, 403):
                raise
            last_err = err
        except (urllib.error.URLError, TimeoutError) as err:
            last_err = err
        time.sleep(2 * (attempt + 1))
    else:
        raise last_err  # type: ignore[misc]
    _last_request[host] = time.time()

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data if binary else data.decode("utf-8", "replace")


def fetch_json(url: str) -> dict:
    return json.loads(fetch(url))


# --------------------------------------------------------------------------- URLs


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "item"


def is_old_site(url: str) -> bool:
    """True for links to the old website (incl. its *.squarespace.com aliases)."""
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc.lower()
    if parts.scheme not in ("", "http", "https"):
        return False
    return (host == "" or host in OLD_HOSTS
            or (host.endswith(".squarespace.com") and host not in ASSET_HOSTS))


def site_path(url: str) -> str:
    """Normalised path of an old-site URL: no host, no trailing slash, unquoted."""
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    path = "/" + path.strip("/")
    return path


def page_url(path: str) -> str:
    """Public URL for a site path: '/a/b' -> '/a/b/', '/' -> '/'."""
    path = "/" + path.strip("/")
    return path if path == "/" else path + "/"


def category_url(name: str) -> str:
    return f"/highlights/categorie/{slugify(name)}/"


def tag_url(name: str) -> str:
    return f"/highlights/tag/{slugify(name)}/"


def ms_to_date(ms: int) -> date:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()


def write_markdown(path: Path, front: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=1000)
    path.write_text(f"---\n{fm}---\n\n{body.strip()}\n", encoding="utf-8")


def read_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body.lstrip("\n")
