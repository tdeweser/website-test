# ipe.nl — website (static rebuild)

A static rebuild of [www.ipe.nl](https://www.ipe.nl) for the Instituut voor Publieke Economie,
in the IPE house style. It holds the permanent pages plus the publications of the last three
months. Nothing links back to the old Squarespace site: every page, image and PDF is in this
repository.

Live preview: **https://ipe-dza.pages.dev** (Cloudflare Pages, marked `noindex`).

## Quick start

Requires Python 3.12 (Windows: `py`).

```bash
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # macOS/Linux: .venv/bin/python

.venv/Scripts/python scripts/build.py     # content/ + templates/ + static/  ->  public/
.venv/Scripts/python scripts/check.py     # must print "OK" before you commit
.venv/Scripts/python -m http.server 8000 -d public        # preview on http://localhost:8000
```

To pull content from the old site again (overwrites `content/pages`, `content/highlights`,
`content/events`, `content/people/authors.yml` and `static/media`):

```bash
.venv/Scripts/python scripts/scrape.py            # uses the HTTP cache in .cache/
.venv/Scripts/python scripts/scrape.py --fresh    # re-download everything
```

## Repository layout

| Path | What it is |
|---|---|
| `content/site.yml` | Site settings: navigation, footer, contact details, scrape scope (the 3-month window). |
| `content/pages/` | Permanent pages (home, topics, over ons, contact, …) as Markdown. |
| `content/highlights/` | Articles, reports and media appearances as Markdown. |
| `content/events/` | Events (none in the current window). |
| `content/people/authors.yml` | Author cards (name, role, photo, e-mail). |
| `templates/` | Jinja2 layouts and partials (header, footer, listings, author cards). |
| `static/` | CSS, JS and media (images, PDFs) copied as-is into the site. |
| `scripts/` | `scrape.py` (old site → content), `build.py` (content → `public/`), `check.py` (verification), `common.py` (shared rules). |
| `design-system/` | The IPE design system (tokens, fonts, logos, guidelines). Only tokens, fonts and logos are published. |
| `docs/` | Architecture, content guide, deployment, and the generated scrape report. |
| `public/` | **Generated** site, committed and served by Cloudflare Pages. Never edit by hand. |

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): how scrape → build → check fits together, URL scheme, scope rules
- [docs/CONTENT-GUIDE.md](docs/CONTENT-GUIDE.md): how to add or edit an article, page or person
- [docs/DEPLOY.md](docs/DEPLOY.md): Cloudflare Pages settings and publishing
- [docs/SCRAPE-REPORT.md](docs/SCRAPE-REPORT.md): what the last scrape took and which links it removed
- [CLAUDE.md](CLAUDE.md): rules for Claude (design system, site conventions)
