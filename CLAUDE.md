# ipe.nl — website rebuild

Static rebuild of www.ipe.nl (Instituut voor Publieke Economie). Content lives in Markdown
(`content/`), is rendered by `scripts/build.py` into `public/`, and `public/` is committed and
served by Cloudflare Pages (`ipe-dza.pages.dev`, output directory `public`, no build command).
Read [README.md](README.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) first.

## Working on this site

- Python: always use `.venv/Scripts/python` (deps in `requirements.txt`).
- Edit sources only: `content/`, `templates/`, `static/`, `scripts/`. Never hand-edit `public/`.
- After every change: `scripts/build.py`, then `scripts/check.py`, which must print OK. Commit
  sources **and** `public/` together.
- **No links to the old site.** Nothing in `public/` may point at ipe.nl, instituut-pe.nl or
  Squarespace (mailto `@ipe.nl` excepted). Download new images/PDFs into `static/media/` and
  link them as `/media/...`. `check.py` enforces this.
- **Look of the site (2026-11-17):** the site is being upgraded section by section.
  - *Redesigned* (modelled on the reference design at ipe-eta.vercel.app): the header, the
    footer (every page), the homepage and "Onze mensen". Redesigned templates put
    `is-redesign` on `<body>`. Styles: `static/assets/css/chrome.css` (tokens, header, footer,
    buttons, blocks, portraits, people cards) and `home.css` (homepage only). DM Sans VF +
    DM Mono, colours red `#d63f44`, cream `#f4ede3`, ink `#141312`, navy `#1d3354`.
  - *Still the original ipe.nl look:* all other page bodies (`site.css`, measured from the old
    Squarespace site). Keep those faithful to the original until the user asks to redesign them.
  - The design system below applies to new designs and mock-ups.
- Hand-maintained (the scraper never overwrites them, `keep_local` in site.yml):
  the homepage `content/pages/home.md` (front matter = all texts and settings), the team page
  `content/pages/onze-mensen.md` and `content/people/people.yml` (everyone on the team page,
  grouped; `home: true` = also on the homepage). Portraits are round with a CSS-drawn red ring
  (`ui.portrait`); `ringed: true` marks photo files that already contain a ring.
- Listings show only `in_window: true` items (the 3-month window, `content/site.yml`).
  Non-article content (pages, events) is taken regardless of date.
- Shortcodes available in content: `listing()`, `authors()`, `archive()`, `map()`,
  `social_links()` (see docs/ARCHITECTURE.md).
- `scripts/scrape.py` overwrites `content/pages|highlights|events`, `content/people/authors.yml`
  and `static/media`. Don't re-run it after hand edits without the user's OK.
- Keep this site `noindex` (`content/site.yml`) until the user says it goes live.
- How to add content: [docs/CONTENT-GUIDE.md](docs/CONTENT-GUIDE.md). Deploy: [docs/DEPLOY.md](docs/DEPLOY.md).

## Lessons learned (problems hit while building this, and the fix)

**Scraping the old Squarespace site** (`scripts/scrape.py`)
- `?format=json` on a *collection* returns full post bodies, so no per-article page fetch is
  needed. On fluid-engine *pages* `mainContent` is empty: parse the HTML instead.
- Posts without a thumbnail have an `assetUrl` ending in `/`. It serves a blank tile with a
  diagonal line; never download it. Squarespace summary blocks then show the first body image
  (outside listing blocks) → `listing_image`. The blog index shows only the own `image`, and
  article pages show no thumbnail at all. (This caused "reports without a photo" and big
  empty boxes above articles.)
- Fluid-engine positions: per block, the *last* `grid-area` rule in the section's `<style>`
  is the desktop one. Blocks often overlap a row or two; treating that as "side by side"
  collapsed two-column pages into one column (donate page). Fix: `ROW_TOLERANCE` and
  `_same_cell()`. Irregular grids (the team page) are better rebuilt as data than
  reconstructed.
- Section settings (background photo, overlay, height) are JSON in `data-current-styles`.
  Sections can be photo-only; don't drop them.
- Summary-block filters aren't in the HTML: infer them. Categories can be OR'ed, and
  hand-picked items break exact matches → 75% coverage plus a complexity penalty.
- Editor text colour (`sqsrte-text-color--*`) can be per paragraph. A majority rule turned
  whole intros red; keep per-paragraph colour as raw `<p class="text-…">`.
- "Old site" means more than `ipe.nl`: `instituut-pe.nl`, `*.squarespace.com` aliases, old
  `@instituut-pe.nl` mail addresses, old URLs typed as plain text, `file:///` links to
  authors' own PCs, footnote anchors (`#_ftn1`) already broken on the original, and
  `#:~:text=` fragments.
- `og:title` is wrong on some pages → `scrape.titles` overrides in `site.yml`.
- File names on the old site can be mislabelled (`profielfoto-senna…png` is Cor). Check
  people photos visually.
- Embeds: Donorbox needs its own `widget.js` for auto-height; a fixed height caused large
  empty space. Substack's signup must be ≥480px wide (narrower shows a big logo); 150px high =
  form only, 180px = with subscriber count.
- Scraper runs wipe `static/media`. Hand-maintained pages (`keep_local`) are still converted
  in a dry run so their images keep being downloaded.

**Build and CSS**
- `site.css` (original look) styles bare `p`, `ul`, `li`, `h1–h4` globally. Those leak into
  redesigned components → reset under `body.is-redesign`. Mind specificity:
  `.is-redesign main :is(ul)` beat `.slider__track`'s padding.
- Jinja runs with `StrictUndefined`: `|first` on an empty list raises an error, and optional
  dict keys need `.get()`.
- The design system's DM Sans has only 400/500/700, so weight 600 renders as 700 (headings too
  heavy, hero on 4 lines instead of 3). Use the self-hosted variable font "DM Sans VF".
- Grid and carousel overflow: give grid items `min-width: 0` and single-column grids
  `minmax(0, 1fr)`, or a carousel widens the page.
- `check.py` matches old hosts as text. Don't write `ipe.nl` or Squarespace host names in
  comments or generated text. Image file names containing "squarespace" are fine.
- Windows: Python `write_text` writes CRLF unless `newline="\n"`. `sed` turned `\\n` into a
  real newline; do edits involving escapes in Python.

**Verifying**
- Compare with the original by measuring computed styles in headless Chrome over the DevTools
  protocol, not by eyeballing. The helper scripts lived in the session scratchpad; recreate
  them with `websocket-client` if needed.
- Headless Chrome can't go below about 500px wide: use DevTools device emulation for 390px.
  Use `--force-prefers-reduced-motion` so reveal animations don't leave elements invisible in
  screenshots. Lazy iframes need a longer `--virtual-time-budget`.
- After a push, wait for Cloudflare. Detect the new deploy by something that only exists in
  the new build; early checks against the old deploy cached 404s, so recheck with `?v=`.
- The scroll-driven wordmark animation (`animation-timeline: view()`) runs in Chrome, Edge and
  Safari 26+. Elsewhere it is static by design.

## Design: use the IPE design system for new designs

Every new HTML design, mock-up or component made in this project follows the IPE
design system in [design-system/](design-system/) (the website itself mirrors the original
ipe.nl, see above). Before designing anything:

1. Read [design-system/README.md](design-system/README.md) — content
   fundamentals (tone, Dutch copy, boilerplate), visual foundations, iconography.
2. Read [design-system/assets/notes/CLAUDE.from-standalone.md](design-system/assets/notes/CLAUDE.from-standalone.md)
   — the fixed colour rules.
3. For a component, read its `.prompt.md` (usage) and `.jsx` (exact styling) in
   [design-system/components/](design-system/components/).
4. For a website page, look at [design-system/templates/website/](design-system/templates/website/)
   (Home, Publications, Article) as the reference layout.

When the README and the official brand guide disagree, the PDF wins:
[design-system/uploads/IPE-richtlijnen-huisstijl-oktober-2025-v21.pdf](design-system/uploads/IPE-richtlijnen-huisstijl-oktober-2025-v21.pdf).
Address and domain are the exception: use **ipe.nl** and **Plein 17, 2511 CS Den Haag**
(the PDF still shows the old ones).

### How to wire it into a page

- For a standalone mock-up, link `design-system/styles.css`. It loads the self-hosted
  DM Sans / DM Mono fonts and all tokens. (The website build also publishes it at
  `/assets/ds/styles.css`, used there only for the DM Sans fonts.)
- Use the CSS custom properties, never raw hex values: `var(--brand)`,
  `var(--surface-alt)`, `var(--font-mono)`, `var(--space-6)`, `var(--type-h1)` etc.
  (see [design-system/tokens/](design-system/tokens/)).
- The site is static HTML. Reproduce components as plain HTML + CSS using the
  styling in their `.jsx` files; only use React/Babel (`_ds_bundle.js`) for
  throwaway prototypes, not for production pages.
- Logos: use the PNGs in [design-system/assets/logo/](design-system/assets/logo/)
  rather than re-typesetting the wordmark.

### Non-negotiables

- **Palette is fixed to nine colours**: white `#ffffff`, black `#000000`,
  beige `#f4ede3`, text gray `#404040`, red `#d63f44` (hero accent),
  navy `#1d3354`, gray `#9f9f9f`, aqua `#4790b1`, green `#00843b`. Charts use only
  red and navy plus their `-l80/-l60/-l40/-d25/-d50` variants. No other colours.
- **Type**: DM Sans for everything; DM Mono for logo, labels, numbers and tables.
  Never DM Serif.
- **Bullets** are the small red square (▪), not round dots.
- **Layout** is asymmetric and editorial; the logo is never centred. Flat colour
  fields (white / beige / red), no gradients or textures. Small radii (2–10px);
  pills only for tags.
- **Copy** is Dutch, sentence case, no emoji. Institutional "wij" voice.
- **Icons**: Lucide (line icons) as a stand-in.
- `Tag` supports `red | navy | aqua | green | gray` — its `.d.ts` says `blue`,
  but the implementation uses `navy` (a `blue` tag silently falls back to red).

## Source of the design system

[design-system/](design-system/) is a copy of the organisation's
"IPE Design System" artifact (https://claude.ai/artifact/LBc7RZSkfVHFvNey8azUF2),
taken 2026-11-16. Left out: Word/PowerPoint/Excel templates, slide and print
templates, and extracted PDF page images. If the artifact is updated, re-pull the
changed files into `design-system/` instead of editing them here.
