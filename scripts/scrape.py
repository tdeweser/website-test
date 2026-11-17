"""Scrape www.ipe.nl (Squarespace) into Markdown content + local media.

    .venv/Scripts/python scripts/scrape.py            # uses the HTTP cache in .cache/
    .venv/Scripts/python scripts/scrape.py --fresh    # ignore the cache

Output (overwritten on every run):
    content/pages/*.md        permanent pages and linked one-off pages
    content/highlights/*.md   articles (front matter `in_window` says if they are listed)
    content/events/*.md       events
    static/media/img|files/   every image / PDF the content uses
    docs/SCRAPE-REPORT.md     what was taken, what was unlinked and why

Scope rules are documented in docs/ARCHITECTURE.md; settings live in content/site.yml.
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import mimetypes
import re
import shutil
import sys
import urllib.error
import urllib.parse
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from hashlib import sha1
from pathlib import Path

import yaml
from bs4 import BeautifulSoup, Tag
from markdownify import MarkdownConverter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    ASSET_HOSTS, CONTENT, DOCS, MEDIA, SITE, category_url, fetch, fetch_json,
    is_old_site, load_config, ms_to_date, page_url, read_markdown, site_path, slugify,
    tag_url, write_markdown,
)

FETCH_CACHE = True

# ----------------------------------------------------------------------------- report


@dataclass
class Report:
    unlinked: list = field(default_factory=list)      # (source, text, old url, reason)
    broken: list = field(default_factory=list)        # (source, old url, error)
    unknown_blocks: list = field(default_factory=list)
    scripts: list = field(default_factory=list)
    empty_listings: list = field(default_factory=list)
    assets: dict = field(default_factory=dict)        # remote url -> local url
    notes: list = field(default_factory=list)


REPORT = Report()

# ----------------------------------------------------------------------------- inventory


@dataclass
class Entry:
    path: str                 # old-site path, e.g. /highlights/gemeentepolis
    kind: str                 # page | article | event | linked-page
    in_window: bool = False
    item: dict | None = None  # collection JSON item (articles/events)
    html: str | None = None   # page HTML (pages)


class Inventory:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        s = cfg["scrape"]
        self.window_start: date = s["window_start"]
        self.ignore = [p.lower() for p in s["ignore_paths"]]
        self.collections = s["collections"]
        self.index: dict[str, dict] = {}          # lower path -> collection item
        self.authors: dict[str, dict] = {}        # lower path -> author card
        self.author_by_title: dict[str, dict] = {}
        self.entries: dict[str, Entry] = {}       # lower path -> Entry
        self.missing: set[str] = set()

    # -- collections ---------------------------------------------------------
    def load_collections(self):
        for coll in self.collections:
            offset = None
            while True:
                url = f"{SITE}{coll}?format=json" + (f"&offset={offset}" if offset else "")
                data = fetch_json(url)
                for it in data.get("items", []):
                    it["_collection"] = coll.strip("/")
                    self.index[site_path(it["fullUrl"]).lower()] = it
                pag = data.get("pagination") or {}
                if not pag.get("nextPage"):
                    break
                offset = pag["nextPageOffset"]
        print(f"  collections: {len(self.index)} items indexed")

    def load_authors(self):
        coll = self.cfg["scrape"].get("authors")
        if not coll:
            return
        offset = None
        while True:
            data = fetch_json(f"{SITE}{coll}?format=json" + (f"&offset={offset}" if offset else ""))
            for it in data.get("items", []):
                title = htmllib.unescape(it["title"]).strip()
                name = (it.get("categories") or [None])[0]
                m = re.match(r"^(.*?)\s+[-–]\s+(.*)$", title) or re.match(r"^(.*?)\s*\((.*)\)$", title)
                name = name or (m.group(1) if m else title)
                role = m.group(2).strip() if m else ""
                card = {"name": name.strip(), "role": role, "title": title,
                        "_image": it.get("assetUrl"),
                        "email": BeautifulSoup(it.get("excerpt") or "", "html.parser").get_text(" ", strip=True).removeprefix("E:").strip(),
                        "url": tag_url(name)}
                self.authors[site_path(it["fullUrl"]).lower()] = card
                self.author_by_title[title.lower()] = card
            pag = data.get("pagination") or {}
            if not pag.get("nextPage"):
                break
            offset = pag["nextPageOffset"]
        print(f"  authors: {len(self.authors)} author cards")

    def in_window(self, item: dict) -> bool:
        if item.get("_collection") in self.cfg["scrape"].get("always_listed", []):
            return True  # not articles (e.g. events): listed regardless of date
        return ms_to_date(item["publishOn"]) >= self.window_start

    def sitemap_pages(self) -> list[str]:
        """Every plain page in the old sitemap (not posts in a collection)."""
        xml = fetch(SITE + "/sitemap.xml", use_cache=FETCH_CACHE)
        colls = [c.lower() for c in self.collections] + [str(self.cfg["scrape"].get("authors", "")).lower()]
        out = []
        for loc in re.findall(r"<loc>([^<]+)</loc>", xml):
            path = site_path(htmllib.unescape(loc))
            low = path.lower()
            if (low in ("/", "/home") or self.ignored(path)
                    or any(low == c or low.startswith(c + "/") for c in colls if c)):
                continue
            out.append(path)
        return out

    def add(self, entry: Entry):
        self.entries[entry.path.lower()] = entry

    def has(self, path: str) -> bool:
        return path.lower() in self.entries

    def ignored(self, path: str) -> bool:
        p = path.lower()
        return any(p == i or p.startswith(i + "/") for i in self.ignore)


INV: Inventory  # set in main()

# ----------------------------------------------------------------------------- assets

IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"}


def _abs(url: str) -> str:
    url = url.strip()
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return SITE + url
    return url


def download_asset(url: str, kind: str | None = None) -> str | None:
    """Download an image/file once; return its local /media/... URL (None on failure)."""
    url = _abs(htmllib.unescape(url))
    parts = urllib.parse.urlsplit(url)
    base = urllib.parse.urlunsplit((parts.scheme or "https", parts.netloc, parts.path, "", ""))
    if base in REPORT.assets:
        return REPORT.assets[base]

    name = urllib.parse.unquote(parts.path.rsplit("/", 1)[-1]) or "file"
    stem, ext = (name.rsplit(".", 1) + [""])[:2]
    ext = ("." + ext.lower()) if ext else ""
    if kind is None:
        kind = "img" if (ext in IMG_EXT or parts.netloc == "images.squarespace-cdn.com") else "files"

    fetch_url = base
    if parts.netloc == "images.squarespace-cdn.com" and ext not in (".gif", ".svg"):
        fetch_url = base + "?format=1500w"
    try:
        data = fetch(fetch_url, binary=True, delay=0.25, use_cache=FETCH_CACHE)
    except Exception as err:  # noqa: BLE001
        REPORT.broken.append(("(asset)", url, str(err)))
        return None

    if not ext:
        ext = _sniff_ext(data) or ".bin"
    short = sha1(base.encode()).hexdigest()[:8]
    fname = f"{slugify(stem)[:60]}-{short}{ext}" if kind == "img" else f"{slugify(stem)[:80]}{ext}"
    target = MEDIA / kind / fname
    if kind == "files" and target.exists() and target.read_bytes() != data:
        fname = f"{slugify(stem)[:80]}-{short}{ext}"
        target = MEDIA / kind / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    local = f"/media/{kind}/{fname}"
    REPORT.assets[base] = local
    return local


def _sniff_ext(data: bytes) -> str | None:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[:4] == b"%PDF":
        return ".pdf"
    return None


def img_src(img: Tag) -> str | None:
    for attr in ("data-src", "data-image", "src"):
        v = img.get(attr)
        if v and not v.startswith("data:"):
            return v
    return None

# ----------------------------------------------------------------------------- links


class LinkContext:
    """Rewrites links found on one source page and records what it did."""

    def __init__(self, source: str):
        self.source = source

    def rewrite(self, href: str, text: str = "") -> str | None:
        href = (href or "").strip()
        if href.startswith("mailto:"):
            # The institute moved from instituut-pe.nl to ipe.nl; addresses moved too.
            return re.sub(r"@(?:www\.)?instituut-pe\.nl", "@ipe.nl", href, flags=re.I)
        if not href or href.startswith(("tel:", "#", "javascript:")):
            return href or None
        if href.lower().startswith("file:"):
            REPORT.unlinked.append((self.source, text, href[:120], "link to a file on the author's own computer"))
            return None
        href = _abs(href) if href.startswith(("/", "//")) else href
        parts = urllib.parse.urlsplit(href)
        host = parts.netloc.lower()

        if host in ASSET_HOSTS:
            local = download_asset(href)
            if local is None:
                REPORT.unlinked.append((self.source, text, href, "asset download failed"))
            return local

        if not is_old_site(href):
            return href  # external link: kept as-is

        path = site_path(href)
        query = urllib.parse.parse_qs(parts.query)
        frag = f"#{parts.fragment}" if parts.fragment and not parts.fragment.startswith(":~:") else ""
        low = path.lower()

        if low.startswith("/s/"):
            local = download_asset(SITE + urllib.parse.quote(path), kind="files")
            if local is None:
                REPORT.unlinked.append((self.source, text, href, "file download failed"))
            return local
        if low == "/":
            return "/" + frag
        if low in ("/highlights", "/blog") or low.startswith("/highlights/category/") or low.startswith("/highlights/tag/"):
            if query.get("format", [""])[0] == "rss":
                return "/feed.xml"
            if "category" in query:
                return category_url(query["category"][0])
            if "tag" in query:
                return tag_url(query["tag"][0])
            if "year" in query or "month" in query:
                return "/archief/"
            if low.startswith("/highlights/category/"):
                return category_url(path.split("/", 3)[3])
            if low.startswith("/highlights/tag/"):
                return tag_url(path.split("/", 3)[3])
            return "/highlights/"
        if low == "/evenementen":
            return "/events/"
        if low in INV.authors:
            return INV.authors[low]["url"]
        if low == "/auteurs":
            return "/onze-mensen/"
        if INV.has(path):
            return page_url(INV.entries[low].path) + frag
        reason = "out of scope (not linked from an in-scope page)"
        if low in INV.missing:
            reason = "page does not exist on the old site (404)"
        elif INV.ignored(path):
            reason = "Squarespace system page"
        REPORT.unlinked.append((self.source, text, href, reason))
        return None

# ----------------------------------------------------------------------------- HTML -> Markdown


class MD(MarkdownConverter):
    """markdownify with a few IPE tweaks."""

    def convert_img(self, el, text, *args, **kwargs):  # keep only src/alt
        alt = (el.get("alt") or "").replace("\n", " ")
        return f"![{alt}]({el.get('src', '')})"

    def convert_a(self, el, text, *args, **kwargs):  # keep anchor targets (footnotes)
        out = super().convert_a(el, text, *args, **kwargs)
        return f'<a id="{el["id"]}"></a>{out}' if el.get("id") else out


def md(html: str) -> str:
    out = MD(heading_style="ATX", bullets="-", escape_underscores=False,
             escape_asterisks=False, strip=["span", "font"]).convert(html)
    out = re.sub(r"@(?:www\.)?instituut-pe\.nl\b", "@ipe.nl", out, flags=re.I)  # old e-mail domain
    out = re.sub(r"\n{3,}", "\n\n", out)
    out = re.sub(r"[ \t]+\n", "\n", out)
    return out.strip()


OLD_URL_TEXT = re.compile(r"^(https?://)?(www\.)?(ipe|instituut-pe)\.nl\b", re.I)

KEEP_ATTRS = {"a": {"href", "id"}, "img": {"src", "alt"}, "td": {"colspan", "rowspan"},
              "th": {"colspan", "rowspan"}}


def clean_rich_text(el: Tag, ctx: LinkContext) -> str:
    """Sanitise a Squarespace rich-text fragment and return Markdown."""
    el = BeautifulSoup(str(el), "html.parser")
    for t in el.find_all(["style", "script", "noscript", "svg"]):
        t.decompose()
    for a in el.find_all("a"):
        if a.get("name") and not a.get("id"):
            a["id"] = a["name"]
        text = a.get_text(" ", strip=True)
        if not a.get("href"):
            if a.get("id"):  # pure anchor target, e.g. a footnote
                a.attrs = {"id": a["id"]}
            else:
                a.unwrap()
            continue
        new = ctx.rewrite(a.get("href", ""), text)
        if new is None:
            if a.get("id"):
                a.attrs = {"id": a["id"]}
            else:
                a.unwrap()
            continue
        a["href"] = new
        if OLD_URL_TEXT.match(text):  # visible text was an old-site URL
            a.string = new
    for img in el.find_all("img"):
        src = img_src(img)
        local = download_asset(src) if src else None
        if local:
            img["src"] = local
        else:
            img.decompose()
    for h in el.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        for b in h.find_all(["strong", "b", "em"]):
            b.unwrap()
    link_plain_urls(el, ctx)
    colored = element_colors(el)
    for t in el.find_all(True):
        keep = KEEP_ATTRS.get(t.name, set())
        for attr in list(t.attrs):
            if attr not in keep:
                del t[attr]
    for p in el.find_all("p"):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()
    # Paragraphs/headings with their own text colour stay raw HTML with a class.
    raw = {}
    for i, (node, color) in enumerate(colored):
        if node.parent is None:
            continue
        token = f"IPERAWBLOCK{i}X"
        raw[token] = f'<{node.name} class="text-{color}">{node.decode_contents().strip()}</{node.name}>'
        node.replace_with(BeautifulSoup(f"<p>{token}</p>", "html.parser"))
    out = md(str(el))
    for token, html in raw.items():
        out = out.replace(token, html)
    return out


def element_colors(el: Tag) -> list[tuple[Tag, str]]:
    """Text blocks coloured by the editor (sqsrte-text-color--x), when not every block in
    the fragment has that colour (a uniform colour is handled as a block class)."""
    found, blocks = [], [b for b in el.find_all(["p", "h1", "h2", "h3", "h4"]) if not b.find_parent("li")]
    for b in blocks:
        holder = b if "sqsrte-text-color" in " ".join(b.get("class") or []) else b.select_one('[class*="sqsrte-text-color--"]')
        if holder is None or holder.get_text(strip=True) != b.get_text(strip=True):
            continue
        m = re.search(r"sqsrte-text-color--(\w+)", " ".join(holder.get("class") or []))
        if m and m.group(1) in ("accent", "white", "black", "darkAccent", "lightAccent"):
            found.append((b, m.group(1).lower()))
    if found and len(found) == len(blocks) and len({c for _, c in found}) == 1:
        return []
    return found


PLAIN_OLD_URL = re.compile(r"https?://(?:www\.)?(?:ipe|instituut-pe)\.nl[^\s<>\"')\]]*", re.I)


def link_plain_urls(el: Tag, ctx: LinkContext):
    """Old-site URLs typed as plain text: link them to the local copy, or, when the page
    is not in the copy, replace the URL by the title of what it pointed to."""
    for node in list(el.find_all(string=PLAIN_OLD_URL)):
        if node.find_parent("a"):
            continue
        html_parts, last = [], 0
        text = str(node)
        for m in PLAIN_OLD_URL.finditer(text):
            url = m.group(0).rstrip(".,;:")
            html_parts.append(htmllib.escape(text[last:m.start()]))
            item = INV.index.get(site_path(url).lower())
            label = htmllib.unescape(item["title"]) if item else site_path(url)
            local = ctx.rewrite(url, label)
            if local:
                html_parts.append(f'<a href="{htmllib.escape(local)}">{htmllib.escape(label)}</a>')
            else:
                html_parts.append(htmllib.escape(f"“{label}”" if item else label))
            html_parts.append(htmllib.escape(m.group(0)[len(url):]))
            last = m.end()
        html_parts.append(htmllib.escape(text[last:]))
        node.replace_with(BeautifulSoup("".join(html_parts), "html.parser"))


def clean_raw_html(el: Tag, ctx: LinkContext, *, keep_scripts: bool = True) -> str:
    """Keep raw HTML (embeds/code) but localise links and assets."""
    el = BeautifulSoup(str(el), "html.parser")
    for a in el.find_all("a"):
        new = ctx.rewrite(a.get("href", ""), a.get_text(" ", strip=True))
        if new is None:
            a.unwrap()
        else:
            a["href"] = new
    for img in el.find_all("img"):
        src = img_src(img)
        local = download_asset(src) if src else None
        if local:
            img["src"] = local
            for attr in ("data-src", "data-image", "srcset"):
                if img.has_attr(attr):
                    del img[attr]
    if el.find("script"):
        REPORT.scripts.append((ctx.source, str(el.find("script"))[:200]))
        if not keep_scripts:
            for s in el.find_all("script"):
                s.decompose()
    return str(el).strip()

# ----------------------------------------------------------------------------- blocks


def block_type(sb: Tag) -> str:
    name = sb.get("data-definition-name") or ""
    if name:
        return name.split(".")[-1]
    for c in sb.get("class", []):
        if c.startswith("sqs-block-") and c not in ("sqs-block-website-component",):
            return c[len("sqs-block-"):]
    return "unknown"


def convert_block(sb: Tag, ctx: LinkContext) -> str:
    text = _convert_block(sb, ctx)
    if text.strip() and "sqs-background-enabled" in (sb.get("class") or []):
        # Blocks with "background" switched on: a padded box in the theme's accent colour.
        text = f'<div class="block-bg" markdown="1">\n\n{text}\n\n</div>'
    return text


def text_style_classes(el: Tag) -> list[str]:
    """Alignment and size the editor applied to (most of) a text block."""
    paras = el.find_all(["p", "h1", "h2", "h3", "h4", "li"])
    if not paras:
        return []
    classes = []
    for align in ("center", "right"):
        n = sum(1 for p in paras if f"text-align: {align}" in (p.get("style") or "").replace("text-align:", "text-align: ").replace("  ", " "))
        if n * 2 > len(paras):
            classes.append(f"align-{align}")
    for color in ("white", "black", "accent"):  # whole block in one colour
        n = sum(1 for p in paras if p.select_one(f".sqsrte-text-color--{color}") or f"sqsrte-text-color--{color}" in " ".join(p.get("class") or []))
        if n == len(paras):
            classes.append(f"text-{color}")
    ps = [p for p in paras if p.name == "p"]
    for size in ("large", "small"):
        n = sum(1 for p in ps if f"sqsrte-{size}" in " ".join(p.get("class") or []))
        if ps and n * 2 > len(ps):
            classes.append(f"text-{size}")
    return classes


def _convert_block(sb: Tag, ctx: LinkContext) -> str:
    t = block_type(sb)
    content = sb.select_one(".sqs-block-content") or sb

    if t in ("html", "text"):
        inner = sb.select_one(".sqs-html-content") or content
        text = clean_rich_text(inner, ctx)
        classes = text_style_classes(inner)
        if classes and text.strip():
            text = f'<div class="{" ".join(classes)}" markdown="1">\n\n{text}\n\n</div>'
        return text

    if t in ("imageFluid", "image", "imageLayout"):
        img = sb.find("img")
        if not img or not img_src(img):
            return ""
        local = download_asset(img_src(img))
        if not local:
            return ""
        alt = (img.get("alt") or "").strip().replace("\n", " ")
        caption_el = sb.select_one(".image-caption, figcaption")
        caption = caption_el.get_text(" ", strip=True) if caption_el else ""
        link = img.find_parent("a") or sb.select_one("a[href]")
        href = ctx.rewrite(link["href"], alt or caption) if link and link.get("href") else None
        social = social_label(href, local)
        if social:  # tiny icon images linking to a profile -> plain text link
            return f'<a class="social-link" href="{htmllib.escape(href)}" target="_blank" rel="noopener">{social}</a>'
        out = f"![{alt}]({local})"
        if href:
            out = f"[{out}]({href})"
        if caption:
            out = f'<figure markdown="1">\n\n{out}\n\n<figcaption>{htmllib.escape(caption)}</figcaption>\n</figure>'
        return out

    if t in ("embed", "video"):
        frames = sb.find_all("iframe")
        if not frames:
            holder = sb.find(attrs={"data-html": True})
            if holder:
                frames = BeautifulSoup(holder["data-html"], "html.parser").find_all("iframe")
        if not frames:
            REPORT.unknown_blocks.append((ctx.source, t, "embed without iframe"))
            return ""
        scripts = [s for s in sb.find_all("script", src=True) if not is_old_site(_abs(s["src"]))]
        if scripts:
            # Provider widget (e.g. Donorbox widget.js) that sizes its own iframe:
            # keep the iframe's own attributes and the script, no ratio box.
            out = []
            for fr in frames:
                if is_old_site(_abs(fr.get("src", ""))):
                    continue
                fr.attrs = {k: v for k, v in fr.attrs.items() if not k.startswith("data-")}
                fr["loading"] = "lazy"
                out.append(str(fr))
            for s in scripts:
                REPORT.scripts.append((ctx.source, f'<script src="{s["src"]}">'))
                attrs = "".join(f' {k}="{htmllib.escape(v)}"' for k, v in s.attrs.items() if isinstance(v, str))
                out.append(f"<script{attrs}></script>")
            return '<div class="embed-raw">' + "".join(out) + "</div>"
        return embed_html(frames, ctx)

    if t == "code":
        box = sb.select_one(".sqs-code-container") or content
        inner = "".join(str(c) for c in box.contents).strip()
        anchor = re.fullmatch(r'<p id="([^"]+)">\s*</p>', inner)
        if anchor:
            return f'<span class="anchor" id="{anchor.group(1)}"></span>'
        if not inner:
            return ""
        frag = BeautifulSoup(inner, "html.parser")
        frames = frag.find_all("iframe")
        if frames and not frag.get_text(strip=True):
            # iframe-only code block (dashboards): treat as an embed, keep its script.
            out = embed_html(frames, ctx)
            for s in frag.find_all("script"):
                REPORT.scripts.append((ctx.source, str(s)[:200]))
                out += "\n" + str(s)
            return out
        return clean_raw_html(frag, ctx)

    return convert_other(t, sb, content, ctx)


def embed_html(frames, ctx: LinkContext) -> str:
    """Wrap iframes in a responsive .embed container (third-party embeds are kept)."""
    parts = []
    for fr in frames:
        src = _abs(htmllib.unescape(fr.get("src") or fr.get("data-src") or ""))
        if is_old_site(src):
            REPORT.unlinked.append((ctx.source, "(embed)", src, "embed pointed at old site"))
            continue
        w, h = fr.get("width", ""), fr.get("height", "")
        title = fr.get("title") or "Ingesloten inhoud"
        ratio = ""
        if str(w).isdigit() and str(h).isdigit() and int(w) > 0:
            ratio = f' style="--embed-ratio: {int(w)} / {int(h)}"'
        allow = f' allow="{fr["allow"]}"' if fr.get("allow") else ""
        provider = slugify(urllib.parse.urlsplit(src).netloc.removeprefix("www."))
        attrs = "".join(
            f' {a}="{htmllib.escape(" ".join(fr[a]) if isinstance(fr[a], list) else fr[a])}"'
            for a in ("id", "name", "class") if fr.get(a))
        parts.append(
            f'<div class="embed embed--{provider}"{ratio}><iframe src="{htmllib.escape(src)}"{attrs} '
            f'title="{htmllib.escape(title)}" loading="lazy"{allow} allowfullscreen></iframe></div>'
        )
    return "\n".join(parts)


def convert_other(t: str, sb: Tag, content: Tag, ctx: LinkContext) -> str:
    if t in ("summary", "summary-v2"):
        return summary_directive(sb, ctx)

    if t == "accordion":
        out = []
        for li in sb.select("li.accordion-item"):
            title = li.select_one(".accordion-item__title")
            desc = li.select_one(".accordion-item__description")
            body = clean_rich_text(desc, ctx) if desc else ""
            out.append(
                f'<details class="accordion" markdown="1">\n<summary>{htmllib.escape(title.get_text(" ", strip=True) if title else "")}</summary>\n\n{body}\n\n</details>'
            )
        return "\n\n".join(out)

    if t == "button":
        a = sb.find("a")
        if not a:
            return ""
        label = a.get_text(" ", strip=True)
        href = ctx.rewrite(a.get("href", ""), label)
        if not href:
            return ""
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        box = sb.select_one(".sqs-block-button-container")
        align = "left"
        for c in (box.get("class") if box else []):
            if c.startswith("sqs-block-button-container--"):
                align = c.rsplit("--", 1)[1]
        return (f'<p class="button-row align-{align}"><a class="button" href="{htmllib.escape(href)}"{ext}>'
                f'{htmllib.escape(label)}</a></p>')

    if t == "map":
        holder = sb.find(attrs={"data-context": True})
        loc = {}
        if holder:
            try:
                loc = json.loads(holder["data-context"]).get("location", {})
            except ValueError:
                pass
        query = ", ".join(x for x in (loc.get("addressLine1"), loc.get("addressLine2")) if x) or "Plein 17, Den Haag"
        query = query.replace("17 Plein", "Plein 17")
        return "{{ map(%s) }}" % json.dumps(query, ensure_ascii=False)

    if t == "horizontalrule":
        return "<hr>"
    if t in ("spacer", "search"):
        return ""
    if t == "archive":
        return "{{ archive() }}"
    if t == "socialLinks":
        return "{{ social_links() }}"
    if t == "quote":
        text = sb.get_text(" ", strip=True)
        return "> " + text

    REPORT.unknown_blocks.append((ctx.source, t, sb.get_text(" ", strip=True)[:80]))
    text = clean_rich_text(content, ctx)
    return text


SOCIAL = {"twitter.com": "X", "x.com": "X", "linkedin.com": "LinkedIn", "bsky.app": "Bluesky"}


def social_label(href: str | None, local_img: str) -> str | None:
    if not href or not href.startswith("http"):
        return None
    host = urllib.parse.urlsplit(href).netloc.lower().removeprefix("www.")
    name = local_img.rsplit("/", 1)[-1].lower()
    for h, label in SOCIAL.items():
        if host.endswith(h) and any(k in name for k in ("twitter", "linkedin", "x-", "bluesky", "logo")):
            return label
    return None


def summary_display(wrapper: Tag | None) -> dict:
    """Display settings of a summary block, read from its wrapper's setting classes."""
    if wrapper is None:
        return {}
    cls = " ".join(wrapper.get("class") or [])

    def setting(name, default):
        m = re.search(rf"summary-block-setting-{name}-([a-z-]+?)(?:\s|$)", cls + " ")
        return m.group(1) if m else default

    out = {
        "meta1": setting("primary-metadata", "date"),
        "meta2": setting("secondary-metadata", "none"),
        "meta_pos": setting("metadata-position", "below-title"),
        "thumbs": "summary-block-setting-show-thumbnail" in cls,
        "excerpt": "summary-block-setting-show-excerpt" in cls,
    }
    if wrapper.get("data-slides-per-row"):
        out["per_row"] = int(wrapper["data-slides-per-row"])
    try:
        ratio = float(wrapper.get("data-image-aspect-ratio") or 0)
        if ratio:
            out["ratio"] = ratio
    except ValueError:
        pass
    if "design-list-thumbnail-right" in cls:
        out["thumb_side"] = "right"
    return out


def summary_directive(sb: Tag, ctx: LinkContext) -> str:
    """Turn a Squarespace summary (auto-listing) block into a {{ listing() }} call.

    The block's filter is not in the HTML, so it is inferred: we look for the
    category/tag whose N most recent items are exactly the N items the block shows.
    """
    titles = [a.get_text(" ", strip=True).lower() for a in sb.select(".summary-item .summary-title-link")]
    cards = [INV.author_by_title[t] for t in titles if t in INV.author_by_title]
    if cards and len(cards) == len(titles):
        names = list(dict.fromkeys(c["name"] for c in cards))
        return "{{ authors(%s) }}" % json.dumps(names, ensure_ascii=False)

    hrefs = []
    for a in sb.select(".summary-item a[href]"):
        if not is_old_site(_abs(a["href"])):
            continue
        p = site_path(_abs(a["href"])).lower()
        if p not in hrefs and p in INV.index:
            hrefs.append(p)
    wrapper = sb.select_one(".summary-block-wrapper")
    design = wrapper.get("data-design", "list") if wrapper else "list"
    items = [INV.index[h] for h in hrefs]
    limit = max(3, min(len(items) or 6, 30 if design == "list" else 12))
    args = {"limit": limit, "layout": design}
    args.update(summary_display(wrapper))

    if items:
        coll = items[0]["_collection"]
        args["collection"] = coll
        args.update(infer_filter(items, coll))
    else:
        args["collection"] = "highlights"
    call = ", ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in args.items())
    return "{{ listing(%s) }}" % call.replace("true", "True").replace("false", "False")


def _subsets(values, max_size=2):
    from itertools import combinations
    vals = sorted(values)
    out = [()]
    for n in range(1, max_size + 1):
        out += list(combinations(vals, n))
    return out


def infer_filter(items: list[dict], coll: str) -> dict:
    """Find the (categories AND tags [AND featured]) filter whose most recent N items
    are exactly the N items a summary block shows. Within categories/tags the match is
    OR, as in Squarespace. Falls back to the closest match if nothing is exact."""
    pool = sorted((it for it in INV.index.values() if it["_collection"] == coll),
                  key=lambda it: -it["publishOn"])
    listed = {site_path(it["fullUrl"]).lower() for it in items}
    n = len(listed)
    cats_all = set().union(*(it.get("categories") or [] for it in items))
    tags_all = set().union(*(it.get("tags") or [] for it in items))
    def covers(s, key):  # the set matches at least 75% of the shown items
        return not s or sum(bool(set(s) & set(it.get(key) or [])) for it in items) >= 0.75 * n

    cat_sets = [s for s in _subsets(cats_all) if covers(s, "categories")]
    tag_sets = [s for s in _subsets(tags_all) if covers(s, "tags")]
    featured_opts = [False, True] if sum(bool(it.get("starred")) for it in items) >= 0.75 * n else [False]

    best, best_score, best_overlap = None, (-9.0, 0), 0.0
    for cs in cat_sets:
        for ts in tag_sets:
            for feat in featured_opts:
                top = []
                for it in pool:
                    if cs and not set(cs) & set(it.get("categories") or []):
                        continue
                    if ts and not set(ts) & set(it.get("tags") or []):
                        continue
                    if feat and not it.get("starred"):
                        continue
                    top.append(site_path(it["fullUrl"]).lower())
                    if len(top) == n:
                        break
                overlap = len(listed & set(top)) / max(n, 1)
                # Each extra condition costs 5%: a simple filter that matches all but
                # one hand-picked item beats a contrived combination.
                complexity = len(cs) + len(ts) + feat
                score = (round(overlap - 0.05 * complexity, 6), -complexity)
                if score > best_score:
                    best, best_score, best_overlap = (cs, ts, feat), score, overlap
    out: dict = {}
    if best:
        cs, ts, feat = best
        if cs:
            out["category"] = cs[0] if len(cs) == 1 else list(cs)
        if ts:
            out["tag"] = ts[0] if len(ts) == 1 else list(ts)
        if feat:
            out["featured"] = True
        if best_overlap < 1:
            REPORT.notes.append(f"summary filter inferred approximately ({best_overlap:.0%} of shown items match): {out}")
    return out

# ----------------------------------------------------------------------------- layouts

GRID_RE = re.compile(r"\.fe-block-([\w-]+)\s*\{\s*grid-area:\s*(\d+)/(\d+)/(\d+)/(\d+)")


def fluid_section(section: Tag, ctx: LinkContext) -> str:
    css = " ".join(s.get_text() for s in section.find_all("style"))
    areas = {}
    for m in GRID_RE.finditer(css):  # later rules (desktop media query) win
        areas[m.group(1)] = tuple(int(x) for x in m.group(2, 3, 4, 5))
    blocks = []
    for fe in section.select(".fe-block"):
        fid = next((c[len("fe-block-"):] for c in fe.get("class", []) if c.startswith("fe-block-")), None)
        sb = fe.select_one(".sqs-block")
        if not sb or not fid:
            continue
        text = convert_block(sb, ctx)
        if not text.strip():
            continue
        r1, c1, r2, c2 = areas.get(fid, (len(blocks) * 10 + 1, 2, len(blocks) * 10 + 2, 26))
        blocks.append((r1, c1, r2, c2, text))
    return grid_to_markdown(blocks)


ROW_TOLERANCE = 2  # Squarespace lets blocks overlap a row or two; that is not "side by side".


def grid_to_markdown(blocks):
    """Rebuild the old site's 24-column grid.

    Blocks whose row spans overlap (beyond ROW_TOLERANCE) form a row; within a row,
    blocks whose column spans overlap form one cell. Each cell keeps its exact desktop
    column range (`--c: start / end` on a 24-column grid, see .fe-row in site.css).
    """
    blocks.sort(key=lambda b: (b[0], b[1]))
    rows, cur, cur_end = [], [], 0
    for b in blocks:
        if cur and b[0] >= cur_end - ROW_TOLERANCE and not _same_cell(cur, b):
            rows.append(cur)
            cur, cur_end = [], 0
        cur.append(b)
        cur_end = max(cur_end, b[2])
    if cur:
        rows.append(cur)

    out = []
    for row in rows:
        cols, col, col_end = [], [], 0
        for b in sorted(row, key=lambda b: (b[1], b[0])):
            if col and b[1] >= col_end:
                cols.append(col)
                col, col_end = [], 0
            col.append(b)
            col_end = max(col_end, b[3])
        if col:
            cols.append(col)
        cells = []
        for c in cols:
            start = max(1, min(b[1] for b in c) - 1)
            end = min(25, max(b[3] for b in c) - 1)
            inner = "\n\n".join(b[4] for b in sorted(c, key=lambda b: b[0]))
            cells.append(f'<div class="fe-cell" style="--c: {start} / {end}" markdown="1">\n\n{inner}\n\n</div>')
        out.append('<div class="fe-row" markdown="1">\n\n' + "\n\n".join(cells) + "\n\n</div>")
    return "\n\n".join(out)


def _same_cell(row, b) -> bool:
    """Keep stacking `b` into the current row when it sits under one existing column
    while a neighbouring column is still running (e.g. a button under a heading
    next to a long text). Otherwise rows break normally."""
    overlapping = [x for x in row if not (b[3] <= x[1] or b[1] >= x[3])]
    others = [x for x in row if x not in overlapping]
    return bool(overlapping) and all(x[1] == b[1] for x in overlapping) \
        and any(x[2] > b[0] for x in others)


def classic_layout(el: Tag, ctx: LinkContext) -> str:
    """Squarespace 'classic' layout (.sqs-layout > .row > .col.span-N > blocks)."""
    out = []
    for child in el.children:
        if not isinstance(child, Tag):
            continue
        classes = child.get("class", [])
        if "sqs-block" in classes:
            text = convert_block(child, ctx)
            if text.strip():
                out.append(text)
        elif "row" in classes:
            cols = [c for c in child.children if isinstance(c, Tag) and "col" in c.get("class", [])]
            rendered = [(c, classic_layout(c, ctx)) for c in cols]
            rendered = [(c, t) for c, t in rendered if t.strip()]
            if len(rendered) <= 1:
                out.extend(t for _, t in rendered)
            else:  # classic 12-column grid -> same 24-column .fe-row as fluid sections
                cells, pos = [], 1
                for c, t in rendered:
                    m = re.search(r"span-(\d+)", " ".join(c.get("class", [])))
                    span = 2 * int(m.group(1)) if m else 24 // len(rendered)
                    cells.append(f'<div class="fe-cell" style="--c: {pos} / {min(25, pos + span)}" markdown="1">\n\n{t}\n\n</div>')
                    pos += span
                out.append('<div class="fe-row" markdown="1">\n\n' + "\n\n".join(cells) + "\n\n</div>")
        else:
            text = classic_layout(child, ctx)
            if text.strip():
                out.append(text)
    return "\n\n".join(out)


KNOWN_THEMES = {"white", "white-bold", "light", "light-bold", "dark", "dark-bold",
                "black", "black-bold", "bright", "bright-inverse"}


def section_settings(sec: Tag) -> dict:
    """Section design settings Squarespace stores as JSON on the <section>."""
    try:
        return json.loads(sec.get("data-current-styles") or "{}")
    except ValueError:
        return {}


def page_body(soup: BeautifulSoup, ctx: LinkContext) -> str:
    main = soup.find("main") or soup
    sections = [s for s in main.find_all("section") if "page-section" in (s.get("class") or [])]
    out = []
    for sec in sections:
        theme = sec.get("data-section-theme", "") or "white"
        if theme not in KNOWN_THEMES:
            REPORT.notes.append(f"{ctx.source}: unknown section theme '{theme}'")
        st = section_settings(sec)
        bg = None
        bg_asset = (st.get("backgroundImage") or {}).get("assetUrl") if st.get("backgroundMode", "image") == "image" else None
        if not bg_asset:
            bg_img = sec.select_one(".section-background img")
            bg_asset = img_src(bg_img) if bg_img else None
        if bg_asset:
            bg = download_asset(bg_asset)
        if sec.select_one(".fluid-engine"):
            body = fluid_section(sec, ctx)
        else:
            layout = sec.select_one(".sqs-layout")
            body = classic_layout(layout, ctx) if layout else ""
            if not layout and sec.select(".sqs-block"):
                body = "\n\n".join(convert_block(b, ctx) for b in sec.select(".sqs-block"))
        if not body.strip() and not bg:
            continue
        height = (st.get("sectionHeight") or "section-height--small").replace("section-height--", "")
        classes = ["band", f"theme-{theme}", f"height-{height}"]
        style = ""
        if bg:
            classes.append("band--image")
            overlay = st.get("imageOverlayOpacity", 0) or 0
            style = f' style="--band-image: url({bg}); --overlay: {overlay}"'
        if not body.strip():
            classes.append("band--image-only")
        out.append(f'<section class="{" ".join(classes)}"{style} markdown="1">\n\n{body}\n\n</section>')
    if not sections:
        layout = main.select_one(".sqs-layout")
        if layout:
            out.append(classic_layout(layout, ctx))
    return "\n\n".join(out)


def page_title(soup: BeautifulSoup) -> str:
    og = soup.find("meta", property="og:title")
    title = og["content"] if og and og.get("content") else (soup.title.string if soup.title else "")
    title = re.sub(r"\s*[—–|-]\s*Instituut voor Publieke Economie\s*$", "", title or "").strip()
    return title or "Instituut voor Publieke Economie"

# ----------------------------------------------------------------------------- discovery


def links_in(html: str, *, skip_listings: bool = True) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    scope = soup.find("main") or soup
    if skip_listings:
        for t in scope.select(".summary-block, .summary-v2-block, .sqs-block-archive, .sqs-block-summary-v2"):
            t.decompose()
    hrefs = [a.get("href", "") for a in scope.find_all("a")]
    return [h for h in hrefs if h and not h.startswith(("#", "mailto:", "tel:"))]


def discover(inv: Inventory):
    """Pages/articles linked from in-scope content become 'linked' entries (1 level)."""
    sources = []
    for e in list(inv.entries.values()):
        if e.html:
            sources.append((e.path, links_in(e.html)))
        elif e.item:
            sources.append((e.path, links_in(e.item.get("body") or "", skip_listings=True)))
    queued = set()
    for src, hrefs in sources:
        for h in hrefs:
            h = _abs(h) if h.startswith(("/", "//")) else h
            if not is_old_site(h):
                continue
            path = site_path(h)
            low = path.lower()
            if (low == "/" or low.startswith("/s/") or inv.has(path) or inv.ignored(path)
                    or low in ("/highlights", "/evenementen", "/auteurs") or low in inv.authors
                    or low.startswith(("/highlights/tag/", "/highlights/category/"))):
                continue
            queued.add(path)
    for path in sorted(queued):
        low = path.lower()
        if low in inv.index:
            item = inv.index[low]
            kind = "event" if item["_collection"] == "evenementen" else "article"
            inv.add(Entry(site_path(item["fullUrl"]), kind, inv.in_window(item), item=item))
            continue
        try:
            html = fetch(SITE + urllib.parse.quote(path), use_cache=FETCH_CACHE)
        except urllib.error.HTTPError as err:
            inv.missing.add(low)
            REPORT.broken.append(("(discovery)", SITE + path, f"HTTP {err.code}"))
            continue
        inv.add(Entry(path, "linked-page", html=html))
    print(f"  discovery: {len(queued)} linked pages/articles one level deep")

# ----------------------------------------------------------------------------- writers


def fix_dead_anchors(body: str, source: str) -> str:
    """Unlink [text](#x) when no element on the page has id="x" (broken on the old site too)."""
    ids = set(re.findall(r'id="([^"]+)"', body))

    def repl(m):
        if m.group(2) in ids:
            return m.group(0)
        REPORT.broken.append((source, f"#{m.group(2)}", "anchor target missing on the old site; link removed"))
        return m.group(1)
    return re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(#([^)\s]+)\)", repl, body)


def thumbnail_url(it: dict) -> str | None:
    """The item's thumbnail, as Squarespace shows it in listings.

    Items without their own thumbnail get a placeholder assetUrl that ends in '/'
    (it serves a blank tile). Squarespace then uses the first image in the post body,
    skipping images inside listing blocks such as the author cards.
    """
    asset = it.get("assetUrl") or ""
    if asset and not asset.endswith("/"):
        return asset
    soup = BeautifulSoup(it.get("body") or "", "html.parser")
    for t in soup.select(".sqs-block-summary-v2, .summary-block"):
        t.decompose()
    for img in soup.find_all("img"):
        src = img_src(img)
        if src and "squarespace-cdn.com" in src:
            return src
    return None


def article_filename(path: str, d: date) -> str:
    rest = path.split("/", 2)[2] if path.count("/") >= 2 else path
    return f"{d.isoformat()}-{'--'.join(slugify(p) for p in rest.split('/'))}.md"


def write_item(e: Entry, folder: str):
    it = e.item
    ctx = LinkContext(e.path)
    body_html = it.get("body") or ""
    soup = BeautifulSoup(body_html, "html.parser")
    layout = soup.select_one(".sqs-layout")
    body = classic_layout(layout, ctx) if layout else clean_rich_text(soup, ctx)
    body = fix_dead_anchors(body, e.path)
    d = ms_to_date(it["publishOn"])
    own = it.get("assetUrl") or ""
    image = download_asset(own) if own and not own.endswith("/") else None
    thumb = thumbnail_url(it)
    listing_image = download_asset(thumb) if thumb and thumb != own else None
    excerpt = BeautifulSoup(it.get("excerpt") or "", "html.parser").get_text(" ", strip=True)
    author = (it.get("author") or {}).get("displayName")
    front = {
        "title": htmllib.unescape(it["title"]).strip(),
        "url": page_url(e.path),
        "date": d,
        "in_window": e.in_window,
        "categories": it.get("categories") or [],
        "tags": it.get("tags") or [],
        "author": author,
        "featured": bool(it.get("starred")) or None,
        "image": image,                  # own thumbnail (blog index, social preview)
        "listing_image": listing_image,  # fallback used by summary blocks: first body image
        "excerpt": excerpt,
        "external_url": it.get("sourceUrl") or None,
        "source": SITE + e.path,
    }
    front = {k: v for k, v in front.items() if v not in (None, "", [])} | {"in_window": e.in_window}
    write_markdown(CONTENT / folder / article_filename(e.path, d), front, body)


def write_page(e: Entry, dry_run: bool = False):
    soup = BeautifulSoup(e.html, "html.parser")
    ctx = LinkContext(e.path)
    # Blog items in collections we don't index (e.g. /auteurs/x) render as articles.
    body = page_body(soup, ctx)
    if not body.strip():
        item_layout = soup.select_one("article .sqs-layout, .blog-item-content .sqs-layout")
        if item_layout:
            body = classic_layout(item_layout, ctx)
    body = fix_dead_anchors(body, e.path)
    name = "home" if e.path == "/" else "--".join(slugify(p) for p in e.path.strip("/").split("/"))
    front = {
        "title": INV.cfg["scrape"].get("titles", {}).get(e.path) or page_title(soup),
        "url": page_url(e.path),
        "layout": "home" if e.path == "/" else "page",
        "linked_only": e.kind == "linked-page",
        "source": SITE + e.path,
    }
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        front["description"] = re.sub(r"@(?:www\.)?instituut-pe\.nl\b", "@ipe.nl", desc["content"].strip())
    if not dry_run:
        write_markdown(CONTENT / "pages" / f"{name}.md", front, body)

# ----------------------------------------------------------------------------- report


def write_report(inv: Inventory):
    lines = ["# Scrape report", "",
             f"Generated by `scripts/scrape.py` on {date.today().isoformat()}. "
             f"Window start: **{inv.window_start.isoformat()}**. Do not edit by hand.", ""]
    groups = defaultdict(list)
    for e in inv.entries.values():
        groups[(e.kind, e.in_window)].append(e)
    lines += ["## Pages and articles", "",
              "| Kind | Count |", "|---|---|"]
    for (kind, win), es in sorted(groups.items()):
        label = kind + (" (in window, listed)" if win else (" (linked only)" if kind in ("article", "event") else ""))
        lines.append(f"| {label} | {len(es)} |")
    lines += ["", f"Assets downloaded: **{len(REPORT.assets)}** "
              f"({sum(1 for v in REPORT.assets.values() if '/img/' in v)} images, "
              f"{sum(1 for v in REPORT.assets.values() if '/files/' in v)} files).", ""]

    def section(title, rows, header):
        nonlocal lines
        lines += [f"## {title} ({len(rows)})", ""]
        if not rows:
            lines += ["None.", ""]
            return
        lines += ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
        for r in rows:
            lines.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
        lines.append("")

    for kind in ("article", "linked-page", "event"):
        es = sorted((e for e in inv.entries.values() if e.kind == kind), key=lambda e: e.path)
        rows = [(page_url(e.path), "yes" if e.in_window else "no") for e in es]
        section(f"{kind} entries", rows, ["Local URL", "Listed"])
    section("Links removed (text kept)", sorted(set(REPORT.unlinked)), ["On page", "Link text", "Old URL", "Reason"])
    section("Broken on the old site", sorted(set(REPORT.broken)), ["Found on", "URL", "Error"])
    section("Embedded scripts kept", REPORT.scripts, ["Page", "Script"])
    section("Unknown block types", REPORT.unknown_blocks, ["Page", "Type", "Text"])
    if REPORT.notes:
        lines += ["## Notes", ""] + [f"- {n}" for n in REPORT.notes] + [""]
    (DOCS / "SCRAPE-REPORT.md").write_text("\n".join(lines), encoding="utf-8")

# ----------------------------------------------------------------------------- main


def main():
    global INV, FETCH_CACHE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fresh", action="store_true", help="ignore the HTTP cache")
    args = ap.parse_args()
    FETCH_CACHE = not args.fresh
    sys.stdout.reconfigure(encoding="utf-8")

    cfg = load_config()
    INV = Inventory(cfg)
    print("Indexing collections ...")
    INV.load_collections()
    INV.load_authors()

    print("Fetching permanent pages ...")
    pages = list(cfg["scrape"]["pages"])
    if cfg["scrape"].get("include_sitemap_pages"):
        pages += [p for p in INV.sitemap_pages() if p.lower() not in {x.lower() for x in pages}]
    for path in pages:
        try:
            INV.add(Entry(path, "page", html=fetch(SITE + urllib.parse.quote(path), use_cache=FETCH_CACHE)))
        except urllib.error.HTTPError as err:
            REPORT.broken.append(("(sitemap)", SITE + path, f"HTTP {err.code}"))
    print(f"  {len(pages)} pages")
    for low, it in INV.index.items():
        if INV.in_window(it):
            kind = "event" if it["_collection"] == "evenementen" else "article"
            INV.add(Entry(site_path(it["fullUrl"]), kind, True, item=it))
    print(f"  {sum(1 for e in INV.entries.values() if e.in_window)} items in window")

    newest = cfg["scrape"].get("newest_of") or {}
    if newest:
        wanted = set(newest.get("categories", []))
        picks = sorted((it for it in INV.index.values()
                        if it["_collection"] == "highlights" and wanted & set(it.get("categories") or [])),
                       key=lambda it: -it["publishOn"])[: newest.get("count", 4)]
        for it in picks:
            path = site_path(it["fullUrl"])
            if not INV.has(path):
                INV.add(Entry(path, "article", INV.in_window(it), item=it))
        print(f"  newest {', '.join(sorted(wanted))}: {len(picks)} ensured")

    print("Discovering linked pages ...")
    discover(INV)

    print("Writing content ...")
    keep_local = {p.lower() for p in cfg["scrape"].get("keep_local", [])}
    for sub in ("highlights", "events"):
        shutil.rmtree(CONTENT / sub, ignore_errors=True)
    for f in (CONTENT / "pages").glob("*.md"):   # only remove what the scraper wrote
        if read_markdown(f)[0].get("source"):
            f.unlink()
    shutil.rmtree(MEDIA, ignore_errors=True)
    for e in sorted(INV.entries.values(), key=lambda e: e.path):
        if e.kind in ("page", "linked-page"):
            # Hand-maintained pages are still converted (assets, link report) but not written.
            write_page(e, dry_run=e.path.lower() in keep_local)
        elif e.kind == "article":
            write_item(e, "highlights")
        elif e.kind == "event":
            write_item(e, "events")

    # Author cards -> content/people/authors.yml (photos downloaded).
    people = []
    for card in sorted(INV.authors.values(), key=lambda c: c["name"].lower()):
        entry = {k: v for k, v in card.items() if not k.startswith("_") and v}
        if card.get("_image"):
            entry["photo"] = download_asset(card["_image"])
        people.append(entry)
    (CONTENT / "people").mkdir(parents=True, exist_ok=True)
    (CONTENT / "people" / "authors.yml").write_text(
        "# Generated by scripts/scrape.py from the old /auteurs collection.\n"
        + yaml.safe_dump(people, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8")

    # Site-wide assets under fixed names, used by the templates:
    # favicon, the header logo and the donation QR code from the footer.
    home = BeautifulSoup(INV.entries["/"].html, "html.parser")

    def keep_as(url, name):
        local = download_asset(url) if url else None
        if local:
            src = MEDIA / local.removeprefix("/media/")
            shutil.copyfile(src, MEDIA / (name + src.suffix))

    icon = home.find("link", rel="icon")
    keep_as(icon.get("href") if icon else None, "favicon")
    logo = home.select_one("header .header-title-logo img")
    keep_as(img_src(logo) if logo else None, "logo-header")
    qr = home.select_one("footer .sqs-block-image img, footer [data-definition-name$='imageFluid'] img")
    keep_as(img_src(qr) if qr else None, "qr-doneren")
    write_report(INV)
    print(f"Done: {len(INV.entries)} pages/articles, {len(REPORT.assets)} assets, "
          f"{len(REPORT.unlinked)} links removed. See docs/SCRAPE-REPORT.md")


if __name__ == "__main__":
    main()
