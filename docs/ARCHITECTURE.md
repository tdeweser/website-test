# Architecture

```
 www.ipe.nl (Squarespace)
        │  scripts/scrape.py   (one-off / occasional; cached in .cache/)
        ▼
 content/*.md + content/site.yml + static/media/      ← source of truth, edit here
        │  scripts/build.py    (Markdown + Jinja2)
        ▼
 public/                                             ← generated, committed, served
        │  scripts/check.py    (must pass before every commit)
        ▼
 Cloudflare Pages (serves public/ as-is, no build step)
```

The shared rules (which hosts count as the old site, URL and slug formats, paths) live in
`scripts/common.py`, so the three scripts cannot drift apart.

## Scope rules

The scraper enforces these; the settings are in `content/site.yml` under `scrape:`.

1. **Permanent pages** (`scrape.pages`) are always taken.
2. **Window items:** articles (`/highlights`) and events (`/evenementen`) published on or
   after `scrape.window_start` get `in_window: true`. They are the only items that appear
   in listings.
3. **Linked pages, one level deep:** any old-site page that a page from rule 1 or 2 links to
   is also taken, so the link keeps working. Such pages get `in_window: false` (articles) or
   `linked_only: true` (pages) and never appear in listings. Links *inside* them to
   anything still out of scope are removed; the text stays.
4. **Links:**
   - internal links that are in scope → local URL;
   - `/highlights/tag/<X>` → `/highlights/tag/<slug>/`; `?category=X` → `/highlights/categorie/<slug>/`;
   - author cards (`/auteurs/...`) → that author's tag page;
   - anything else on the old site → link removed, text kept, logged in `docs/SCRAPE-REPORT.md`;
   - external links and `mailto:` stay. Old `@instituut-pe.nl` addresses become `@ipe.nl`.
5. **Assets:** every image and file on a Squarespace host (`images.squarespace-cdn.com`,
   `static1.squarespace.com`, `/s/*.pdf`) is downloaded into `static/media/img|files/`.
   Images are fetched at 1500 px wide.
6. **Third-party embeds stay:** Donorbox, the Substack newsletter, YouTube, Google Maps and
   IPE's own dashboards on GitHub Pages and Cloud Run.

## How old-site layouts become Markdown

Squarespace pages are made of *sections* containing positioned *blocks*. The scraper:

- turns each section into `<section class="band …" markdown="1">`. The theme maps to
  `band--alt` (beige), `band--dark` (navy) or `band--image` (background photo);
- reads each block's desktop `grid-area` and groups blocks that sit side by side into
  `<div class="cols" style="--cols: 5fr 18fr">` with one `cols__cell` per column;
- converts each block: text → Markdown, image → `![]()`, button → `.button`,
  accordion → `<details>`, embed → `.embed` iframe, map → `{{ map() }}`;
- turns *summary* blocks (automatic lists of posts) into `{{ listing(...) }}` calls. Their
  filter isn't in the HTML, so the scraper infers it: it looks for the category/tag
  combination whose N most recent posts are exactly the N posts shown. Approximate matches
  are noted in the report.

## Build

`scripts/build.py` renders each Markdown file in three steps:

1. **Jinja pass over the body.** Content can call these shortcodes:

   | Shortcode | Output |
   |---|---|
   | `{{ listing(category=…, tag=…, featured=…, limit=6, layout="list"\|"carousel"\|"grid", title=…, collection="highlights"\|"evenementen") }}` | Window items matching the filter. `category` and `tag` take a string or a list (OR within, AND between). Renders nothing when empty, except for events. |
   | `{{ authors(["Name", …]) }}` | Author cards from `content/people/authors.yml` |
   | `{{ archive() }}` | All window items grouped by month, with a search box |
   | `{{ map("Plein 17, Den Haag") }}` | Google Maps embed |
   | `{{ social_links() }}` | Links from `site.yml → social` |

2. **Markdown → HTML** (`md_in_html`, `tables`, `sane_lists`).
3. **Layout:** the template named by `layout:` in the front matter (`page`, `home`), or
   `article.html` for highlights and events.

It also generates:

- `/highlights/`, `/highlights/categorie/<x>/` and `/highlights/tag/<x>/` (one per tag and
  author);
- `/feed.xml` (RSS of window items) and `/404.html`;
- `robots.txt` and `_headers`. While `noindex: true`, both block search engines.

## URL scheme

Old paths are kept, with a trailing slash, served from `<path>/index.html`. For example,
`https://www.ipe.nl/highlights/betaalbaarbouwen` → `/highlights/betaalbaarbouwen/`.

## Styling

`/assets/ds/styles.css` is the design system: tokens and self-hosted DM Sans and DM Mono,
copied from `design-system/` at build time. `/assets/css/site.css` holds the layout and
components and uses only design-system tokens. `/assets/js/site.js` handles the mobile
menu, dropdowns and archive search; the site works without JavaScript.

## Check

`scripts/check.py` fails (exit code 1) when:

- any file in `public/` mentions `ipe.nl` / `instituut-pe.nl` as a URL, an
  `@instituut-pe.nl` address, or `squarespace`;
- an internal `href`/`src` or `#anchor` doesn't resolve, or a CSS `url()` is missing;
- a page lacks a `<title>`, the header or the footer;
- a content file or a nav entry produced no page.
