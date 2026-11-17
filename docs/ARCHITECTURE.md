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

1. **Permanent pages** (`scrape.pages`) are always taken, plus every other plain page in the
   old `sitemap.xml` (`include_sitemap_pages: true`), whatever its age.
2. **Window items:** articles (`/highlights`) published on or after `scrape.window_start`
   get `in_window: true`. They are the only articles that appear in listings. Collections
   that aren't articles (`always_listed`, e.g. events) are listed regardless of date.
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

- turns each section into `<section class="band theme-<theme> height-<size>" markdown="1">`,
  keeping the Squarespace section theme (`white`, `white-bold`, `light`, `light-bold`,
  `dark`, `bright`, …) and height. The background photo and overlay come from the section's
  `data-current-styles` JSON. Sections with only a photo become `band--image-only`;
- reads each block's desktop `grid-area` and rebuilds the 24-column grid: blocks side by
  side become `<div class="fe-row">` with one `<div class="fe-cell" style="--c: 5 / 22">`
  per column, keeping the exact column range. Small row overlaps (≤ 2 rows) don't merge
  rows, and blocks stacked under one column of a running row stay in that column;
- converts each block: text → Markdown, image → `![]()`, button → `.button` (with its
  alignment), accordion → `<details>`, embed → `.embed` iframe, map → `{{ map() }}`.
  Provider widgets that size themselves (Donorbox `widget.js`) keep their own iframe and
  script (`.embed-raw`);
- keeps editor styling: blocks with a background → `.block-bg`; centred/right-aligned text
  → `.align-center`/`.align-right`; large/small text → `.text-large`/`.text-small`; text
  colour → `.text-white`/`.text-accent` (on the block, or per paragraph as raw HTML);
- turns *summary* blocks (automatic lists of posts) into `{{ listing(...) }}` calls, with
  their display settings (layout, thumbnails, excerpt, which metadata where, items per row,
  image ratio). Their filter isn't in the HTML, so the scraper infers it: it looks for the
  category/tag combination whose N most recent posts are exactly the N posts shown.
  Approximate matches are noted in the report.

**Thumbnails.** A post's own thumbnail is `image`. Posts without one have a placeholder
`assetUrl` ending in `/`. For those, Squarespace's summary blocks show the first image in
the post body, so the scraper stores that as `listing_image`. The blog index shows only
`image`, and article pages show no thumbnail, as on the original.

## Build

`scripts/build.py` renders each Markdown file in three steps:

1. **Jinja pass over the body.** Content can call these shortcodes:

   | Shortcode | Output |
   |---|---|
   | `{{ listing(category=…, tag=…, featured=…, limit=6, layout="list"\|"carousel"\|"grid", collection="highlights"\|"evenementen", meta1=…, meta2=…, meta_pos=…, thumbs=…, excerpt=…, per_row=…, ratio=…) }}` | Listed items matching the filter. `category` and `tag` take a string or a list (OR within, AND between). `meta1`/`meta2`: `date`, `cats`, `tags`, `author` or `none`. `meta_pos`: `above-title`, `below-title` or `below-content`. Renders nothing when empty, except for events. |
   | `{{ authors(["Name", …]) }}` | Author cards ("Name - Role", e-mail, round photo) from `content/people/authors.yml` |
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

The site is being upgraded section by section.

**Redesigned: header, footer and homepage.** These are modelled on the reference design at
https://ipe-eta.vercel.app/ and written from scratch:

- `/assets/css/chrome.css`: tokens (`--red`, `--cream`, `--ink`, `--navy`, `--shell`,
  `--edge`), the sticky header (white once scrolled; dropdown folders; NL/EN picker; mobile
  drawer), the dark footer, the arrow buttons (`.btn`, `.btn--line`, `.btn--small`; on
  hover the arrow block's colour sweeps over the label), headings with a red underline
  that draws in (`.title-line`), and reveal-on-scroll (`[data-reveal]` → `.is-visible`).
- `/assets/css/home.css`: the homepage sections. The hero photo is revealed by a "curtain".
  Topic photos get a red duotone (grayscale + `mix-blend-mode: color`). The media slider has
  arrow buttons. The "Publieke Economie" wordmark is DM Mono with the photo clipped to the
  text, and slides in on scroll (CSS scroll timelines; static in browsers without them).
- Fonts: DM Sans VF (variable, weights 300–800, `fonts-dm-sans.css`) and DM Mono (design system).
- All motion is disabled with `prefers-reduced-motion`, and nothing is hidden without JavaScript.

**Still the original look: every other page body.** The values below were measured from the
live Squarespace site's computed styles in Chrome (`/assets/css/site.css`):

| Element | Value |
|---|---|
| Header | beige `#f4ede3`, 70px high; logo 178×140 hanging below the bar; nav Work Sans 500 17.6px; "STEUN ONS" button 14.4px uppercase |
| Text | DM Sans 17.6px / 1.6 (p, li); Work Sans 500 for nav, meta, buttons, list titles |
| Headings | DM Sans 700: h1 40px, h2 32px, h3 22.4px, h4 19.2px; red in `*-bold` themes and in articles |
| Article | date uppercase 14.4px; title Work Sans 700 40px red (events: black); column 607px, text 85% |
| Colours | accent `#d63f44`, light `#f4ede3`, dark `#1d3354` |
| Page width | max 1284px, side padding 5vw; 24-column grid with an 11px gap |
| Footer | red band "Bevalt onze inhoud?" (share button, newsletter, QR code), then a beige bar |

Files:

- `/assets/css/site.css`: everything visual (themes, grid, header, footer, summaries).
- `/assets/css/fonts-work-sans.css` and `/assets/fonts/`: self-hosted Work Sans (OFL).
- `/assets/ds/styles.css`: the design-system file, used here for the self-hosted DM Sans.
- `/assets/js/site.js`: mobile menu, dropdowns, carousel arrows, the "Deel deze pagina"
  share button and archive search. The site works without JavaScript.
- Logo, favicon and the donation QR code are taken from the old site by the scraper and
  stored as `static/media/logo-header.png`, `favicon.ico` and `qr-doneren.png`.

Not copied on purpose: the newsletter pop-up that the old site shows on every page.

## Check

`scripts/check.py` fails (exit code 1) when:

- any file in `public/` mentions `ipe.nl` / `instituut-pe.nl` as a URL, an
  `@instituut-pe.nl` address, or `squarespace`;
- an internal `href`/`src` or `#anchor` doesn't resolve, or a CSS `url()` is missing;
- a page lacks a `<title>`, the header or the footer;
- a content file or a nav entry produced no page.
