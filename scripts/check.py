"""Verify the built site in public/. Exits non-zero when anything is wrong.

    .venv/Scripts/python scripts/check.py

Checks:
  1. no reference to the old site: ipe.nl / instituut-pe.nl URLs, any squarespace host,
     or old @instituut-pe.nl e-mail addresses (mailto:...@ipe.nl is allowed)
  2. every internal href/src (and every #anchor) resolves to a file in public/
  3. every CSS url() resolves
  4. every page has a <title>, the site header and the footer
  5. every content file and every nav entry produced a page
"""
from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONTENT, PUBLIC, load_config, read_markdown  # noqa: E402

OLD_SITE = re.compile(
    r"(?<![@\w.-])(?:https?:)?(?://)?(?:www\.)?(?:ipe|instituut-pe)\.nl\b"   # URLs / bare hosts
    r"|@(?:www\.)?instituut-pe\.nl\b"                                       # old e-mail domain
    r"|(?:[\w-]+\.)*squarespace(?:-cdn)?\.com|sqspcdn\.com",               # any Squarespace host/asset
    re.I,
)
TEXT_TYPES = {".html", ".css", ".js", ".xml", ".txt", ".json", ""}

errors: list[str] = []


def err(msg: str):
    errors.append(msg)


def resolve(url_path: str) -> Path | None:
    p = urllib.parse.unquote(url_path)
    target = PUBLIC / p.lstrip("/")
    if p.endswith("/"):
        target = target / "index.html"
    if target.is_file():
        return target
    if (target / "index.html").is_file():
        return target / "index.html"
    return None


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if not PUBLIC.exists():
        print("public/ does not exist - run scripts/build.py first")
        return 1

    files = [p for p in PUBLIC.rglob("*") if p.is_file()]
    html_files = [p for p in files if p.suffix == ".html"]
    ids_cache: dict[Path, set[str]] = {}

    def ids(path: Path) -> set[str]:
        if path not in ids_cache:
            soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
            ids_cache[path] = {t["id"] for t in soup.find_all(id=True)}
        return ids_cache[path]

    # 1. old-site references in any text file
    for f in files:
        if f.suffix not in TEXT_TYPES:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in OLD_SITE.finditer(text):
            ctx = text[max(0, m.start() - 60): m.end() + 40].replace("\n", " ")
            err(f"old-site reference in {f.relative_to(PUBLIC)}: …{ctx}…")

    # 2 + 4. links, assets, page structure
    link_count = 0
    for f in html_files:
        rel = f.relative_to(PUBLIC)
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        if not soup.title or not soup.title.get_text(strip=True):
            err(f"{rel}: missing <title>")
        if not soup.select_one("header.site-header") or not soup.select_one("footer.site-footer"):
            err(f"{rel}: missing site header or footer")
        for tag, attr in (("a", "href"), ("img", "src"), ("link", "href"), ("script", "src"), ("iframe", "src"), ("source", "src")):
            for el in soup.find_all(tag):
                url = el.get(attr)
                if not url or url.startswith(("mailto:", "tel:", "data:", "http://", "https://", "//")):
                    continue
                link_count += 1
                parts = urllib.parse.urlsplit(url)
                if parts.fragment.startswith(":~:"):  # text fragment, not an element id
                    parts = parts._replace(fragment="")
                if not parts.path:  # same-page anchor
                    if parts.fragment and parts.fragment not in ids(f):
                        err(f"{rel}: anchor #{parts.fragment} not found on page")
                    continue
                if not parts.path.startswith("/"):
                    err(f"{rel}: relative URL '{url}' (use root-relative /… URLs)")
                    continue
                target = resolve(parts.path)
                if target is None:
                    err(f"{rel}: broken link {url}")
                elif parts.fragment and target.suffix == ".html" and parts.fragment not in ids(target):
                    err(f"{rel}: link {url} - anchor not found")

    # 3. CSS url() references
    for css in (p for p in files if p.suffix == ".css"):
        for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css.read_text(encoding="utf-8")):
            ref = m.group(1)
            if ref.startswith(("data:", "http", "#")) or "var(" in ref:
                continue
            if not (css.parent / ref.split("?")[0]).resolve().exists():
                err(f"{css.relative_to(PUBLIC)}: url({ref}) not found")

    # 5. every content file and nav entry has a page
    for folder in ("pages", "highlights", "events"):
        for md in (CONTENT / folder).glob("*.md"):
            meta, _ = read_markdown(md)
            if resolve(meta["url"]) is None:
                err(f"{md.relative_to(CONTENT)}: page {meta['url']} was not built")
    cfg = load_config()
    for entry in cfg["nav"] + [cfg["cta"]]:
        for item in entry.get("items") or [entry]:
            if resolve(item["url"]) is None:
                err(f"nav: {item['title']} -> {item['url']} was not built")

    print(f"Checked {len(html_files)} pages, {link_count} internal links, {len(files)} files.")
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors[:200]:
            print("  -", e)
        return 1
    print("OK: no old-site references, no broken links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
