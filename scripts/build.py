"""Build the static site: content/ + templates/ + static/ -> public/.

    .venv/Scripts/python scripts/build.py

Pipeline per content file (see docs/ARCHITECTURE.md):
  1. read front matter + Markdown body
  2. render the body as a Jinja template, so content can call the shortcodes
     listing(), authors(), archive(), map() and social_links()
  3. convert Markdown -> HTML (md_in_html keeps the <section>/<div class="cols"> wrappers)
  4. wrap it in the page's layout template and write public/<url>/index.html

Listings only ever show items with `in_window: true` (see content/site.yml).
"""
from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    CONTENT, DESIGN_SYSTEM, PUBLIC, STATIC, TEMPLATES, category_url, load_config,
    read_markdown, slugify, tag_url,
)

MONTHS = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
          "september", "oktober", "november", "december"]
# Categories that describe the *kind* of publication (shown as the card label).
KINDS = ["Rapport", "Policy paper", "Artikel", "Opinie", "In de media"]


def nl_date(d: date, short: bool = False) -> str:
    month = MONTHS[d.month - 1]
    return f"{d.day} {month[:3] if short else month} {d.year}"


@dataclass
class Doc:
    path: Path
    meta: dict
    body: str
    kind: str                      # page | article | event
    html: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def url(self) -> str:
        return self.meta["url"]

    @property
    def title(self) -> str:
        return self.meta.get("title", "")

    @property
    def date(self) -> date | None:
        return self.meta.get("date")

    @property
    def label(self) -> str:
        cats = self.meta.get("categories") or []
        return next((k for k in KINDS if k in cats), cats[0] if cats else "")


class Site:
    def __init__(self):
        self.cfg = load_config()
        self.pages = self._load("pages", "page")
        self.articles = self._load("highlights", "article")
        self.events = self._load("events", "event")
        people_file = CONTENT / "people" / "authors.yml"
        self.authors = {p["name"]: p for p in (yaml.safe_load(people_file.read_text(encoding="utf-8")) or [])} \
            if people_file.exists() else {}
        self.listed = sorted((a for a in self.articles if a.meta.get("in_window")),
                             key=lambda a: (a.date, a.title), reverse=True)
        self.listed_events = sorted((e for e in self.events if e.meta.get("in_window")),
                                    key=lambda e: e.date, reverse=True)
        self.env = Environment(loader=FileSystemLoader(TEMPLATES),
                               autoescape=select_autoescape(["html", "xml"]),
                               undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
        self.env.filters["nl_date"] = nl_date
        self.env.filters["inline_md"] = lambda s: Markup(
            markdown.markdown(s or "").removeprefix("<p>").removesuffix("</p>"))
        self.env.filters["slug"] = slugify
        # People (team page + homepage): content/people/people.yml, groups in display order.
        people_file = CONTENT / "people" / "people.yml"
        self.people_groups = yaml.safe_load(people_file.read_text(encoding="utf-8")) if people_file.exists() else []
        self.team = []
        for group in self.people_groups:
            for p in group["people"]:
                if p.get("home"):
                    own = next((l["url"] for l in p.get("links", []) if l["url"].startswith("/")), None)
                    self.team.append({**p, "url": own or f"/onze-mensen/#{slugify(p['name'])}"})
        self.env.globals["people_groups"] = self.people_groups
        def media(name):  # site-wide assets the scraper stores under fixed names
            f = next(iter(sorted((STATIC / "media").glob(f"{name}.*"))), None)
            return f"/media/{f.name}" if f else None

        self.env.globals.update(site=self.cfg, nav=self.cfg["nav"], tag_url=tag_url,
                                category_url=category_url, now=datetime.now(timezone.utc),
                                today=date.today(), favicon=media("favicon"),
                                logo=media("logo-header") or "/assets/ds/assets/logo/ipe-logo-inverted.png",
                                qr=media("qr-doneren"))
        self.content_env = Environment(autoescape=False, undefined=StrictUndefined)
        self.content_env.globals.update(listing=self.sc_listing, authors=self.sc_authors,
                                        archive=self.sc_archive, map=self.sc_map,
                                        social_links=self.sc_social_links)

    def _load(self, folder: str, kind: str) -> list[Doc]:
        docs = []
        for p in sorted((CONTENT / folder).glob("*.md")):
            meta, body = read_markdown(p)
            docs.append(Doc(p, meta, body, kind))
        return docs

    # ------------------------------------------------------------------ shortcodes
    # Called from inside content Markdown, e.g. {{ listing(category="Rapport", limit=4) }}

    def _partial(self, name: str, **ctx) -> Markup:
        html = self.env.get_template(f"partials/{name}.html").render(**ctx)
        # Collapse to one line so Markdown treats it as a single raw-HTML block.
        return Markup(" ".join(line.strip() for line in html.splitlines() if line.strip()))

    def select(self, collection="highlights", category=None, tag=None, featured=False,
               exclude=None) -> list[Doc]:
        pool = self.listed_events if collection == "evenementen" else self.listed
        cats = [category] if isinstance(category, str) else (category or [])
        tags = [tag] if isinstance(tag, str) else (tag or [])
        out = []
        for d in pool:
            if cats and not set(cats) & set(d.meta.get("categories") or []):
                continue
            if tags and not set(tags) & set(d.meta.get("tags") or []):
                continue
            if featured and not d.meta.get("featured"):
                continue
            if exclude is not None and d is exclude:
                continue
            out.append(d)
        return out

    def sc_listing(self, collection="highlights", category=None, tag=None, featured=False,
                   limit=6, layout="list", title=None, meta1="date", meta2="none",
                   meta_pos="below-title", thumbs=True, excerpt=False, per_row=4,
                   ratio=1.5, thumb_side="left") -> Markup:
        items = self.select(collection, category, tag, featured)[:limit]
        if not items and featured:  # few starred items in the window: fall back to latest
            items = self.select(collection, category, tag)[:limit]
        if not items and collection != "evenementen":
            # Topic pages pair several listings per subject; an empty one just disappears.
            return Markup("")
        empty = "Er zijn op dit moment geen evenementen gepland."
        return self._partial("listing", items=items, layout=layout, title=title, empty=empty,
                             meta1=meta1, meta2=meta2, meta_pos=meta_pos, thumbs=thumbs,
                             excerpt=excerpt, per_row=per_row, ratio=ratio, thumb_side=thumb_side)

    def sc_authors(self, names) -> Markup:
        people = [self.authors.get(n) or {"name": n, "url": tag_url(n)} for n in names]
        return self._partial("authors", people=people)

    def sc_archive(self) -> Markup:
        groups: dict[tuple, list] = {}
        for d in self.listed:
            groups.setdefault((d.date.year, d.date.month), []).append(d)
        months = [(f"{MONTHS[m - 1].capitalize()} {y}", items) for (y, m), items in groups.items()]
        return self._partial("archive", months=months)

    def sc_map(self, query: str) -> Markup:
        return self._partial("map", query=query)

    def sc_social_links(self) -> Markup:
        return self._partial("social", links=self.cfg["social"])

    # ------------------------------------------------------------------ rendering

    def to_html(self, doc: Doc) -> str:
        source = self.content_env.from_string(doc.body).render()
        return markdown.markdown(source, extensions=["md_in_html", "tables", "sane_lists", "fenced_code"],
                                 output_format="html")

    def render(self, template: str, out_url: str, **ctx):
        html = self.env.get_template(template).render(**ctx)
        target = PUBLIC / out_url.strip("/") / "index.html" if out_url.endswith("/") else PUBLIC / out_url.lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8", newline="\n")

    def build(self):
        if PUBLIC.exists():
            shutil.rmtree(PUBLIC)
        PUBLIC.mkdir()
        self.copy_assets()

        for doc in self.pages:
            doc.html = self.to_html(doc)
            layout = doc.meta.get("layout", "page")
            extra = self.home_data(doc) if layout == "home" else {}
            self.render(f"{layout}.html", doc.url, page=doc, content=Markup(doc.html), **extra)

        for doc in self.articles + self.events:
            doc.html = self.to_html(doc)
            self.render("article.html", doc.url, page=doc, content=Markup(doc.html))

        self.build_listings()
        self.build_feed()
        self.render("404.html", "/404.html", page=Doc(Path(), {"title": "Pagina niet gevonden", "url": "/404.html"}, "", "page"))
        self.write_meta_files()
        print(f"Built {len(self.pages)} pages, {len(self.articles)} articles "
              f"({len(self.listed)} listed), {len(self.events)} events -> {PUBLIC.relative_to(PUBLIC.parent)}/")

    def home_data(self, doc: Doc) -> dict:
        """Lists the homepage fills automatically (settings in content/pages/home.md)."""
        m = doc.meta
        pub = m.get("publications", {})
        cats = set(pub.get("categories", []))
        everything = sorted(self.articles, key=lambda a: (a.date, a.title), reverse=True)
        publications = [a for a in everything if cats & set(a.meta.get("categories") or [])][: pub.get("count", 4)]
        art = pub.get("articles") or {}
        articles = [a for a in self.select(category=art.get("category")) if a not in publications][: art.get("count", 3)] if art else []
        med = m.get("media", {})
        media = []
        if med:
            pool = self.select(tag=med.get("tag"))
            with_img = [d for d in pool if d.meta.get("image") or d.meta.get("listing_image")]
            # A photo slider: prefer items with a picture, top up with the rest if needed.
            media = (with_img if len(with_img) >= 4 else pool)[: med.get("count", 10)]
        return {"home": {"publications": publications, "articles": articles, "media": media},
                "team": self.team, "kinds": KINDS}

    def build_listings(self):
        """/highlights/, /highlights/categorie/<x>/ and /highlights/tag/<x>/ pages."""
        def page(title, url, items, heading=None):
            doc = Doc(Path(), {"title": title, "url": url}, "", "page")
            self.render("listing.html", url, page=doc, items=items, heading=heading, filters=None)

        categories = sorted({c for a in self.articles for c in a.meta.get("categories") or []})
        page("Alle publicaties", "/highlights/", self.listed)
        for c in categories:
            page(c, category_url(c), self.select(category=c), heading=c)
        tags = {t for a in self.articles for t in a.meta.get("tags") or []} | set(self.authors)
        for t in sorted(tags):
            page(t, tag_url(t), self.select(tag=t), heading=t)

    def build_feed(self):
        base = self.cfg.get("base_url", "").rstrip("/")
        items = []
        for d in self.listed[:30]:
            pub = datetime(d.date.year, d.date.month, d.date.day, 12, tzinfo=timezone.utc)
            items.append(
                f"<item><title>{xml_escape(d.title)}</title><link>{base}{d.url}</link>"
                f"<guid>{base}{d.url}</guid><pubDate>{format_datetime(pub)}</pubDate>"
                f"<description>{xml_escape(d.meta.get('excerpt', ''))}</description></item>")
        xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
               f"<title>{xml_escape(self.cfg['title'])}</title><link>{base}/</link>"
               f"<description>{xml_escape(self.cfg['description'].strip())}</description>"
               f"<language>nl</language>{''.join(items)}</channel></rss>\n")
        (PUBLIC / "feed.xml").write_text(xml, encoding="utf-8", newline="\n")

    def copy_assets(self):
        shutil.copytree(STATIC, PUBLIC, dirs_exist_ok=True)
        # Only the design system's tokens, fonts and logos are published, not the
        # whole design-system/ folder (its brand-guide PDF stays out of the site).
        ds = PUBLIC / "assets" / "ds"
        ds.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DESIGN_SYSTEM / "styles.css", ds / "styles.css")
        shutil.copytree(DESIGN_SYSTEM / "tokens", ds / "tokens", dirs_exist_ok=True)
        shutil.copytree(DESIGN_SYSTEM / "assets" / "fonts", ds / "assets" / "fonts", dirs_exist_ok=True)
        shutil.copytree(DESIGN_SYSTEM / "assets" / "logo", ds / "assets" / "logo", dirs_exist_ok=True)

    def write_meta_files(self):
        if self.cfg.get("noindex"):
            (PUBLIC / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8", newline="\n")
            (PUBLIC / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8", newline="\n")
        else:
            (PUBLIC / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    Site().build()
